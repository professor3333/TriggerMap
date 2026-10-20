"""Server-rendered review UI.

Pages render the advisory structure server-side; a static script (no inline JavaScript,
strict CSP) draws highlights and the editable checklist from an embedded JSON payload,
using DOM APIs only (no innerHTML), and saves through the JSON API.
"""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from jinja2 import Environment, PackageLoader, select_autoescape

from triggermap.schema.models import Category, DocumentStatus, Role
from triggermap.serve.app import (
    SESSION_COOKIE,
    ApiError,
    get_service,
    optional_user,
    require_user,
)
from triggermap.serve.render import _script_json
from triggermap.serve.schemas import ExtractionOut, Source
from triggermap.text.preprocessing import PreprocessedDocument, preprocess

CSP = (
    "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; "
    "img-src 'self' data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
)
MAX_UPLOAD_BYTES = 2_000_000

_ENV = Environment(
    loader=PackageLoader("triggermap.serve", "templates/app"),
    autoescape=select_autoescape(["html", "j2"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

router = APIRouter(include_in_schema=False)


def page(request: Request, template: str, status: int = 200, **context: Any) -> HTMLResponse:
    html = _ENV.get_template(template).render(user=optional_user(request), **context)
    return HTMLResponse(html, status_code=status, headers={"Content-Security-Policy": CSP})


def structure(doc: PreprocessedDocument) -> list[dict[str, Any]]:
    """Advisory blocks as plain text segments with canonical offsets (lists grouped)."""
    nodes: list[dict[str, Any]] = []
    for block in doc.canonical.blocks:
        segment = {
            "kind": block.kind.value,
            "level": block.level,
            "start": block.start,
            "end": block.end,
            "text": doc.text[block.start : block.end],
        }
        if block.list_id is None:
            nodes.append({"kind": "block", "items": [segment]})
        elif nodes and nodes[-1].get("list_id") == block.list_id:
            nodes[-1]["items"].append(segment)
        else:
            nodes.append(
                {
                    "kind": "list",
                    "list_id": block.list_id,
                    "ordered": block.ordered,
                    "items": [segment],
                }
            )
    return nodes


def _labels() -> dict[str, list[str]]:
    return {
        "categories": [c.value for c in Category],
        "roles": [r.value for r in Role],
        "statuses": [s.value for s in DocumentStatus],
    }


def review_page(
    request: Request,
    extraction: ExtractionOut,
    raw_text: str | None,
) -> HTMLResponse:
    doc = preprocess(raw_text) if raw_text is not None else None
    if doc is None:
        record = get_service(request).store.advisory(extraction.advisory_id or "")
        assert record is not None
        doc = preprocess(record.raw_text)
    state = {
        "document_status": extraction.document_status.value,
        "conditions": [
            {
                "id": c.id,
                "span": list(c.span),
                "category": c.category.value,
                "role": c.role.value,
                "source": c.source if c.source in ("model", "rules") else "model",
                "answer": "UNANSWERED",
                "confidence": c.confidence,
            }
            for c in extraction.conditions
        ],
        "groups": [g.model_dump(mode="json") for g in extraction.groups],
        "notes": None,
    }
    payload: dict[str, Any] = {
        "mode": "new",
        "review_id": None,
        "logged_in": optional_user(request) is not None,
        "source": {"advisory_id": extraction.advisory_id, "text": raw_text},
        "title": extraction.title,
        "meta": {
            "model_id": extraction.model_id,
            "content_hash": extraction.content_hash,
            "preprocessing_version": extraction.preprocessing_version,
            "review_policy_version": extraction.review_policy_version,
        },
        "text": doc.text,
        "state": state,
        "reasons": {c.id: c.review_reasons for c in extraction.conditions},
        "labels": _labels(),
        "history": [],
        "advisory_changed": False,
    }
    return page(
        request,
        "review.html.j2",
        title=extraction.title,
        advisory_id=extraction.advisory_id,
        source_url=extraction.source_url,
        packages=extraction.packages,
        meta=payload["meta"],
        nodes=structure(doc),
        advisory_changed=False,
        payload=_script_json(payload),
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    user = optional_user(request)
    reviews = get_service(request).store.reviews(user) if user else []
    return page(request, "home.html.j2", reviews=reviews)


@router.get("/ui/login", response_class=HTMLResponse)
async def login_form(request: Request) -> HTMLResponse:
    return page(request, "login.html.j2", error=None)


@router.post("/ui/login")
async def login(request: Request, token: str = Form(...)) -> Response:
    if get_service(request).store.user_for_token(token.strip()) is None:
        return page(request, "login.html.j2", status=401, error="That token is not valid.")
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        token.strip(),
        httponly=True,
        samesite="strict",
        secure=request.url.scheme == "https",
        max_age=60 * 60 * 12,
    )
    return response


@router.post("/ui/logout")
async def logout() -> Response:
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


@router.get("/ui/extract", response_class=HTMLResponse)
async def extract_by_id(request: Request, id: str) -> HTMLResponse:
    try:
        extraction = await get_service(request).extract(Source(advisory_id=id.strip()))
    except ApiError as exc:
        return page(request, "home.html.j2", status=exc.status, reviews=[], error=exc.message)
    return review_page(request, extraction, None)


@router.post("/ui/extract", response_class=HTMLResponse)
async def extract_text(
    request: Request, text: str = Form(...), title: str = Form("")
) -> HTMLResponse:
    try:
        source = Source(text=text, title=title.strip() or None)
        extraction = await get_service(request).extract(source)
    except (ApiError, ValueError) as exc:
        message = exc.message if isinstance(exc, ApiError) else "Paste some advisory text."
        return page(request, "home.html.j2", status=422, reviews=[], error=message)
    return review_page(request, extraction, text)


@router.post("/ui/osv", response_class=HTMLResponse)
async def import_osv(request: Request, report: UploadFile) -> HTMLResponse:
    data = await report.read(MAX_UPLOAD_BYTES + 1)
    try:
        if len(data) > MAX_UPLOAD_BYTES:
            raise ApiError(413, "payload_too_large", "the file is too large")
        try:
            parsed = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiError(422, "unsupported_osv_format", "not an OSV-Scanner JSON file") from exc
        result = await get_service(request).import_osv(parsed)
    except ApiError as exc:
        return page(request, "home.html.j2", status=exc.status, reviews=[], error=exc.message)
    return page(request, "osv.html.j2", result=result, filename=report.filename or "report")


@router.get("/ui/reviews/{review_id}", response_class=HTMLResponse)
async def saved_review(request: Request, review_id: str) -> Response:
    try:
        user = require_user(request)
        review = get_service(request).get_review(user, review_id)
    except ApiError as exc:
        if exc.status == 401:
            return RedirectResponse("/ui/login", status_code=303)
        return page(request, "home.html.j2", status=exc.status, reviews=[], error=exc.message)
    raw = get_service(request).store.review_raw_text(review_id, user)
    assert raw is not None  # ownership was checked by get_review
    doc = preprocess(raw)
    payload = {
        "mode": "saved",
        "review_id": review_id,
        "logged_in": True,
        "source": {"advisory_id": review["advisory_id"], "text": None},
        "title": review["title"],
        "meta": {
            k: review[k]
            for k in ("model_id", "content_hash", "preprocessing_version", "review_policy_version")
        },
        "text": doc.text,
        "state": review["state"],
        "reasons": {},
        "labels": _labels(),
        "history": review["history"],
        "advisory_changed": bool(review["advisory_changed"]),
    }
    return page(
        request,
        "review.html.j2",
        title=review["title"],
        advisory_id=review["advisory_id"],
        source_url=review["source_url"],
        packages=[],
        meta=payload["meta"],
        nodes=structure(doc),
        advisory_changed=payload["advisory_changed"],
        payload=_script_json(payload),
    )
