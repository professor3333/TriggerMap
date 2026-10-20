"""FastAPI application: extraction, OSV-Scanner import, reviews, health and metrics.

Privacy: request bodies (pasted advisories, reviewer answers) are never logged. Access logs
carry only method, route, status, duration and byte counts.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, ValidationError

from triggermap import __version__
from triggermap.models.registry import load_extractor
from triggermap.schema.models import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    GroupOperator,
    Role,
)
from triggermap.schema.validate import validate_annotation
from triggermap.serve.export import review_json, review_markdown
from triggermap.serve.policy import ReviewPolicy, apply_policy, load_policy
from triggermap.serve.schemas import (
    ConditionOut,
    ExtractionOut,
    ExtractionRequest,
    OsvImportOut,
    OsvItem,
    ReviewCreate,
    ReviewCreated,
    ReviewState,
    RevisionCreate,
    RevisionCreated,
    Source,
)
from triggermap.serve.storage import AdvisoryRecord, IdempotencyConflict, Store, User
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument, preprocess

log = logging.getLogger("triggermap.access")
ADVISORY_URL = "https://github.com/advisories/{}"


class Settings(BaseModel):
    database: Path = Path("data/app/triggermap.db")
    model: str = "rules"
    model_dir: Path | None = None
    review_policy: Path = Path("configs/review_policy.yaml")
    release: str = "dev"
    max_body_bytes: int = 262_144
    max_text_chars: int = 100_000
    max_conditions: int = 300
    max_osv_vulnerabilities: int = 200
    max_concurrency: int = 4
    queue_timeout_seconds: float = 5.0

    @classmethod
    def from_env(cls) -> Settings:
        values: dict[str, Any] = {}
        for name in cls.model_fields:
            env = os.environ.get(f"TRIGGERMAP_{name.upper()}")
            if env is not None:
                values[name] = env
        return cls.model_validate(values)


class ApiError(Exception):
    def __init__(
        self, status: int, code: str, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(message)
        self.status, self.code, self.message, self.headers = status, code, message, headers


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def weights_digest(kind: str, model_dir: Path | None) -> str:
    """SHA-256 of the model's weights file (rules: of the rules source)."""
    if kind == "rules":
        from triggermap.models.rules import extractor

        return _digest(Path(extractor.__file__))
    assert model_dir is not None
    for name in ("model.safetensors", "tagger.crfsuite"):
        if (model_dir / name).exists():
            return _digest(model_dir / name)
    raise FileNotFoundError(f"no weights file in {model_dir}")


class Metrics:
    def __init__(self) -> None:
        self.registry = CollectorRegistry()
        r = self.registry
        self.requests = Counter(
            "triggermap_requests", "HTTP requests", ["route", "method", "status"], registry=r
        )
        self.latency = Histogram(
            "triggermap_request_seconds", "Request latency", ["route"], registry=r
        )
        self.input_chars = Histogram(
            "triggermap_input_chars",
            "Canonical characters per extraction",
            buckets=(250, 1000, 2500, 5000, 10000, 25000, 50000, 100000),
            registry=r,
        )
        self.conditions = Histogram(
            "triggermap_conditions",
            "Conditions per extraction",
            buckets=(0, 1, 2, 3, 5, 8, 13, 21, 50),
            registry=r,
        )
        self.empty = Counter("triggermap_empty_extractions", "No conditions found", registry=r)
        self.roles = Counter("triggermap_predicted_roles", "Predicted roles", ["role"], registry=r)
        self.review_required = Counter(
            "triggermap_review_required", "Conditions routed to review", registry=r
        )
        self.cache = Counter("triggermap_cache", "Prediction cache", ["result"], registry=r)
        self.errors = Counter("triggermap_errors", "API errors", ["code"], registry=r)


class Service:
    def __init__(self, settings: Settings, store: Store | None = None) -> None:
        self.settings = settings
        self.store = store or Store(settings.database)
        self.extractor = load_extractor(settings.model, settings.model_dir, device="cpu")
        self.policy: ReviewPolicy = (
            load_policy(settings.review_policy)
            if settings.review_policy.exists()
            else ReviewPolicy(version="review-policy-none", model_id=self.extractor.model_id)
        )
        self.weights_sha256 = weights_digest(settings.model, settings.model_dir)
        self.semaphore = asyncio.Semaphore(settings.max_concurrency)
        self.metrics = Metrics()

    # -- status

    def version_info(self) -> dict[str, Any]:
        return {
            "release": self.settings.release,
            "app_version": __version__,
            "model_id": self.extractor.model_id,
            "model_kind": self.settings.model,
            "weights_sha256": self.weights_sha256,
            "preprocessing_version": PREPROCESSING_VERSION,
            "review_policy_version": self.policy.version,
            "calibration": self.policy.calibration,
            "accept_threshold": self.policy.accept_threshold,
            "label_inventory": {
                "categories": [c.value for c in Category],
                "roles": [r.value for r in Role],
                "group_operators": [g.value for g in GroupOperator],
                "document_statuses": [s.value for s in DocumentStatus],
            },
            "advisories": self.store.advisory_count(),
            "snapshot_commit": self.store.get_meta("snapshot_commit"),
        }

    def ready(self) -> bool:
        return self.store.ping()

    # -- extraction

    def resolve(self, source: Source) -> tuple[str, AdvisoryRecord | None, str]:
        if source.advisory_id is not None:
            record = self.store.advisory(source.advisory_id.strip())
            if record is None:
                raise ApiError(404, "unknown_advisory", "advisory not in the served snapshot")
            return record.raw_text, record, source.title or record.title
        assert source.text is not None
        if len(source.text) > self.settings.max_text_chars:
            raise ApiError(413, "text_too_long", "advisory text exceeds the size limit")
        return source.text, None, source.title or "Pasted advisory"

    async def extract(self, source: Source) -> ExtractionOut:
        raw, record, title = self.resolve(source)
        try:
            await asyncio.wait_for(
                self.semaphore.acquire(), timeout=self.settings.queue_timeout_seconds
            )
        except TimeoutError as exc:
            raise ApiError(
                503, "overloaded", "server busy; retry shortly", {"Retry-After": "5"}
            ) from exc
        try:
            return await run_in_threadpool(self._extract, raw, record, title)
        finally:
            self.semaphore.release()

    def _extract(self, raw: str, record: AdvisoryRecord | None, title: str) -> ExtractionOut:
        doc = preprocess(raw)
        if len(doc.text) > self.settings.max_text_chars:
            raise ApiError(413, "text_too_long", "advisory text exceeds the size limit")
        key = Store.cache_key(
            doc.content_hash, self.extractor.model_id, doc.version, self.policy.version
        )
        cached = self.store.cached_prediction(key)
        if cached is not None:
            self.metrics.cache.labels("hit").inc()
            out = ExtractionOut.model_validate_json(cached)
            return out.model_copy(update={"cached": True, "title": title})
        self.metrics.cache.labels("miss").inc()
        extraction = apply_policy(
            self.extractor.extract(doc, record.advisory_id if record else None), doc, self.policy
        )
        if len(extraction.conditions) > self.settings.max_conditions:
            raise ApiError(422, "too_many_conditions", "extraction exceeds the condition limit")
        issues = validate_annotation(extraction, doc.text)
        if issues:  # never show a checklist item without valid evidence
            raise ApiError(
                500, "invalid_prediction", f"prediction failed validation: {issues[0].code}"
            )
        out = self._render(doc, extraction, record, title)
        self._observe(doc, out)
        self.store.store_prediction(
            key,
            doc.content_hash,
            self.extractor.model_id,
            doc.version,
            self.policy.version,
            out.model_dump_json(),
        )
        return out

    def _render(
        self,
        doc: PreprocessedDocument,
        extraction: Extraction,
        record: AdvisoryRecord | None,
        title: str,
    ) -> ExtractionOut:
        reasons: dict[str, list[str]] = {}
        for flag in extraction.review_flags:
            parts = flag.split(":")
            if parts[0] == "review_required" and len(parts) == 3:
                reasons.setdefault(parts[1], []).append(parts[2])
        return ExtractionOut(
            advisory_id=record.advisory_id if record else None,
            title=title,
            source_url=ADVISORY_URL.format(record.advisory_id) if record else None,
            packages=list(record.packages) if record else [],
            source_commit=record.source_commit if record else None,
            content_hash=doc.content_hash,
            preprocessing_version=doc.version,
            model_id=extraction.model_id,
            review_policy_version=self.policy.version,
            document_status=extraction.document_status,
            text=doc.text,
            conditions=[
                ConditionOut(
                    id=c.id,
                    span=c.span,
                    raw_span=doc.canonical.to_raw(*c.span),
                    surface=doc.text[c.span[0] : c.span[1]],
                    category=c.category,
                    role=c.role,
                    source=c.source,
                    confidence=c.confidence,
                    review_reasons=reasons.get(c.id, []),
                )
                for c in extraction.conditions
            ],
            groups=list(extraction.groups),
            review_flags=list(extraction.review_flags),
            cached=False,
        )

    def _observe(self, doc: PreprocessedDocument, out: ExtractionOut) -> None:
        self.metrics.input_chars.observe(len(doc.text))
        self.metrics.conditions.observe(len(out.conditions))
        if not out.conditions:
            self.metrics.empty.inc()
        for c in out.conditions:
            self.metrics.roles.labels(c.role.value).inc()
            if c.review_reasons:
                self.metrics.review_required.inc()

    # -- OSV-Scanner import

    async def import_osv(self, report: Any) -> OsvImportOut:
        if not isinstance(report, dict) or not isinstance(report.get("results"), list):
            raise ApiError(422, "unsupported_osv_format", "expected OSV-Scanner JSON output")
        found: list[tuple[str, str, str | None, str, list[str]]] = []
        try:
            for result in report["results"]:
                for entry in result.get("packages", []):
                    package = entry["package"]
                    for vuln in entry.get("vulnerabilities", []):
                        found.append(
                            (
                                str(vuln["id"]),
                                str(package["name"]),
                                package.get("version"),
                                str(package.get("ecosystem", "")),
                                [str(a) for a in vuln.get("aliases", [])],
                            )
                        )
        except (KeyError, TypeError, AttributeError) as exc:
            raise ApiError(
                422, "unsupported_osv_format", "unexpected OSV-Scanner structure"
            ) from exc
        if len(found) > self.settings.max_osv_vulnerabilities:
            raise ApiError(
                413, "too_many_vulnerabilities", "import exceeds the vulnerability limit"
            )
        items: list[OsvItem] = []
        for vuln_id, name, version, ecosystem, aliases in found:
            base = {
                "vulnerability_id": vuln_id,
                "package": name,
                "version": version,
                "ecosystem": ecosystem,
            }
            if ecosystem.lower() not in ("pypi", "pip"):
                items.append(OsvItem(**base, status="unsupported_ecosystem"))
                continue
            record = next(
                (r for r in (self.store.advisory(i) for i in (vuln_id, *aliases)) if r), None
            )
            if record is None:
                items.append(OsvItem(**base, status="not_in_snapshot"))
                continue
            out = await self.extract(Source(advisory_id=record.advisory_id))
            items.append(
                OsvItem(
                    **base,
                    status="extracted",
                    advisory_id=record.advisory_id,
                    document_status=out.document_status,
                    conditions=len(out.conditions),
                    review_required=sum(bool(c.review_reasons) for c in out.conditions),
                )
            )
        counts: dict[str, int] = {}
        for item in items:
            counts[item.status] = counts.get(item.status, 0) + 1
        return OsvImportOut(items=items, counts=counts)

    # -- reviews

    def create_review(
        self, user: User, key: str, body: ReviewCreate, payload: dict[str, Any]
    ) -> ReviewCreated:
        raw, record, title = self.resolve(body)
        doc = preprocess(raw)
        if body.content_hash != doc.content_hash:
            raise ApiError(409, "advisory_changed", "the advisory text changed; extract it again")
        self.validate_state(body.state, doc)
        meta = {
            "advisory_id": record.advisory_id if record else None,
            "title": title,
            "raw_text": raw,
            "content_hash": doc.content_hash,
            "model_id": body.model_id,
            "preprocessing_version": body.preprocessing_version,
            "review_policy_version": body.review_policy_version,
        }
        try:
            review_id, created = self.store.create_review(
                user, key, payload, meta, body.state.model_dump(mode="json")
            )
        except IdempotencyConflict as exc:
            raise ApiError(
                409, "idempotency_conflict", "key reused with a different request"
            ) from exc
        return ReviewCreated(review_id=review_id, created=created)

    def revise_review(
        self, user: User, review_id: str, key: str, body: RevisionCreate, payload: dict[str, Any]
    ) -> RevisionCreated:
        review = self.store.review(review_id, user)
        if review is None:
            raise ApiError(404, "not_found", "review not found")
        self.validate_state(body.state, preprocess(review["raw_text"]))
        try:
            seq, created = self.store.append_revision(
                review_id, key, payload, body.state.model_dump(mode="json"), body.note
            )
        except IdempotencyConflict as exc:
            raise ApiError(
                409, "idempotency_conflict", "key reused with a different request"
            ) from exc
        return RevisionCreated(review_id=review_id, seq=seq, created=created)

    def get_review(self, user: User, review_id: str) -> dict[str, Any]:
        review = self.store.review(review_id, user)
        if review is None:
            raise ApiError(404, "not_found", "review not found")
        current = self.store.advisory(review["advisory_id"]) if review["advisory_id"] else None
        doc = preprocess(review["raw_text"])
        review["text"] = doc.text
        review["current_content_hash"] = current.content_hash if current else None
        review["advisory_changed"] = (
            current.content_hash != review["content_hash"] if current else None
        )
        review["source_url"] = (
            ADVISORY_URL.format(review["advisory_id"]) if review["advisory_id"] else None
        )
        del review["raw_text"]
        return review

    @staticmethod
    def validate_state(state: ReviewState, doc: PreprocessedDocument) -> None:
        conditions = tuple(
            Condition(
                id=c.id,
                span=c.span,
                category=c.category,
                role=c.role,
                source="human" if c.source == "human" else "model",
            )
            for c in state.conditions
        )
        check = Extraction(
            content_hash=doc.content_hash,
            preprocessing_version=doc.version,
            model_id="review",
            document_status=state.document_status,
            conditions=conditions,
            groups=tuple(state.groups),
        )
        issues = validate_annotation(check, doc.text)
        if issues:
            raise ApiError(
                422, "invalid_review_state", f"{issues[0].code}: {issues[0].message}"[:300]
            )


# ---------------------------------------------------------------------------
# HTTP layer


async def read_model[M: BaseModel](request: Request, model: type[M], limit: int) -> tuple[M, Any]:
    body = await request.body()
    if len(body) > limit:
        raise ApiError(413, "payload_too_large", f"request body exceeds {limit} bytes")
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ApiError(400, "invalid_utf8", "request body is not valid UTF-8") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ApiError(422, "invalid_json", "request body is not valid JSON") from exc
    try:
        return model.model_validate(data), data
    except ValidationError as exc:
        first = exc.errors(include_input=False, include_url=False)[0]
        where = ".".join(str(p) for p in first["loc"]) or "body"
        raise ApiError(422, "invalid_request", f"{where}: {first['msg']}") from exc


async def read_json(request: Request, limit: int) -> Any:
    body = await request.body()
    if len(body) > limit:
        raise ApiError(413, "payload_too_large", f"request body exceeds {limit} bytes")
    try:
        return json.loads(body.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ApiError(400, "invalid_utf8", "request body is not valid UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ApiError(422, "invalid_json", "request body is not valid JSON") from exc


def create_app(
    settings: Settings | None = None, service_factory: Callable[[], Service] | None = None
) -> FastAPI:
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.service = service_factory() if service_factory else Service(settings)
        yield

    app = FastAPI(
        title="TriggerMap",
        version=__version__,
        description="Evidence-linked exposure checklists from security advisories.",
        lifespan=lifespan,
    )

    def service(request: Request) -> Service:
        svc = getattr(request.app.state, "service", None)
        if svc is None:
            raise ApiError(503, "not_ready", "service is starting")
        return svc  # type: ignore[no-any-return]

    def user(request: Request) -> User:
        header = request.headers.get("authorization", "")
        token = header[7:].strip() if header.lower().startswith("bearer ") else ""
        found = service(request).store.user_for_token(token) if token else None
        if found is None:
            raise ApiError(401, "unauthorized", "a valid API token is required")
        return found

    def idempotency_key(request: Request) -> str:
        key = request.headers.get("idempotency-key", "").strip()
        if not 1 <= len(key) <= 200:
            raise ApiError(400, "missing_idempotency_key", "send an Idempotency-Key header")
        return key

    @app.exception_handler(ApiError)
    async def api_error(request: Request, exc: ApiError) -> JSONResponse:
        svc = getattr(request.app.state, "service", None)
        if svc is not None:
            svc.metrics.errors.labels(exc.code).inc()
        return JSONResponse(
            {"error": {"code": exc.code, "message": exc.message}},
            status_code=exc.status,
            headers=exc.headers,
        )

    @app.middleware("http")
    async def observe(request: Request, call_next: Any) -> Response:
        started = time.perf_counter()
        response: Response = await call_next(request)
        route = getattr(request.scope.get("route"), "path", "unmatched")
        elapsed = time.perf_counter() - started
        svc = getattr(request.app.state, "service", None)
        if svc is not None and route != "/metrics":
            svc.metrics.requests.labels(route, request.method, str(response.status_code)).inc()
            svc.metrics.latency.labels(route).observe(elapsed)
        log.info(
            json.dumps(
                {
                    "method": request.method,
                    "route": route,
                    "status": response.status_code,
                    "ms": round(elapsed * 1000, 1),
                    "bytes_in": int(request.headers.get("content-length") or 0),
                }
            )
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    async def readyz(request: Request) -> JSONResponse:
        svc = getattr(request.app.state, "service", None)
        if svc is None or not svc.ready():
            return JSONResponse({"status": "not_ready"}, status_code=503)
        return JSONResponse({"status": "ready", **svc.version_info()})

    @app.get("/metrics")
    async def metrics(request: Request) -> Response:
        return Response(
            generate_latest(service(request).metrics.registry), media_type=CONTENT_TYPE_LATEST
        )

    @app.post("/v1/extractions", response_model=ExtractionOut)
    async def extractions(request: Request) -> ExtractionOut:
        svc = service(request)
        body, _ = await read_model(request, ExtractionRequest, svc.settings.max_body_bytes)
        return await svc.extract(body)

    @app.post("/v1/imports/osv", response_model=OsvImportOut)
    async def import_osv(request: Request) -> OsvImportOut:
        svc = service(request)
        return await svc.import_osv(await read_json(request, svc.settings.max_body_bytes))

    @app.post("/v1/reviews", response_model=ReviewCreated)
    async def create_review(request: Request, response: Response) -> ReviewCreated:
        svc = service(request)
        who, key = user(request), idempotency_key(request)
        body, payload = await read_model(request, ReviewCreate, svc.settings.max_body_bytes)
        result = await run_in_threadpool(svc.create_review, who, key, body, payload)
        response.status_code = 201 if result.created else 200
        return result

    @app.post("/v1/reviews/{review_id}/revisions", response_model=RevisionCreated)
    async def revise(review_id: str, request: Request, response: Response) -> RevisionCreated:
        svc = service(request)
        who, key = user(request), idempotency_key(request)
        body, payload = await read_model(request, RevisionCreate, svc.settings.max_body_bytes)
        result = await run_in_threadpool(svc.revise_review, who, review_id, key, body, payload)
        response.status_code = 201 if result.created else 200
        return result

    @app.get("/v1/reviews")
    async def list_reviews(request: Request) -> list[dict[str, Any]]:
        return service(request).store.reviews(user(request))

    @app.get("/v1/reviews/{review_id}")
    async def get_review(review_id: str, request: Request) -> dict[str, Any]:
        return service(request).get_review(user(request), review_id)

    @app.get("/v1/reviews/{review_id}/export")
    async def export(review_id: str, request: Request, format: str = "json") -> Response:
        review = service(request).get_review(user(request), review_id)
        name = (review["advisory_id"] or "advisory") + "-review"
        if format == "markdown":
            content, media, ext = review_markdown(review), "text/markdown; charset=utf-8", "md"
        elif format == "json":
            content, media, ext = review_json(review), "application/json", "json"
        else:
            raise ApiError(422, "invalid_request", "format must be json or markdown")
        return Response(
            content,
            media_type=media,
            headers={"Content-Disposition": f'attachment; filename="{name}.{ext}"'},
        )

    return app
