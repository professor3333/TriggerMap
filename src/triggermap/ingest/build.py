"""Filter a snapshot to PyPI advisories and write the processed corpus with a manifest.

Every scanned file ends in exactly one bucket: kept, excluded (not PyPI, withdrawn,
no text) or quarantined (unreadable or malformed, with a reason). Nothing is dropped
silently, and the outputs are byte-for-byte deterministic for a given snapshot.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from triggermap.ingest.records import AdvisoryDocument, OsvRecord, normalize_package_name
from triggermap.ingest.snapshot import REPO_URL, REVIEWED_DIR
from triggermap.text.preprocessing import PREPROCESSING_VERSION, compose_raw, content_hash

ECOSYSTEM = "PyPI"
CORPUS_FILE = "advisories.jsonl"


@dataclass(frozen=True)
class Quarantined:
    path: str
    reason: str
    detail: str


@dataclass
class IngestResult:
    documents: list[AdvisoryDocument] = field(default_factory=list)
    quarantined: list[Quarantined] = field(default_factory=list)
    counts: Counter[str] = field(default_factory=Counter)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def iter_advisory_files(repo_root: Path) -> Iterator[Path]:
    yield from sorted((repo_root / REVIEWED_DIR).rglob("*.json"))


def ingest(repo_root: Path, source_commit: str) -> IngestResult:
    result = IngestResult()
    for path in iter_advisory_files(repo_root):
        result.counts["scanned"] += 1
        rel = path.relative_to(repo_root).as_posix()
        data = path.read_bytes()
        outcome = _classify(rel, data, source_commit)
        if isinstance(outcome, AdvisoryDocument):
            result.documents.append(outcome)
            result.counts["kept"] += 1
        elif isinstance(outcome, Quarantined):
            result.quarantined.append(outcome)
            result.counts[f"quarantined:{outcome.reason}"] += 1
        else:
            result.counts[f"excluded:{outcome}"] += 1
    result.documents.sort(key=lambda d: d.advisory_id)
    return result


def _classify(rel: str, data: bytes, source_commit: str) -> AdvisoryDocument | Quarantined | str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return Quarantined(rel, "invalid_utf8", str(exc))
    try:
        obj: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        return Quarantined(rel, "invalid_json", str(exc))
    if not isinstance(obj, dict):
        return Quarantined(rel, "not_an_object", type(obj).__name__)
    try:
        record = OsvRecord.model_validate(obj)
    except ValidationError as exc:
        return Quarantined(rel, "schema_invalid", _first_error(exc))

    ecosystems = sorted({a.package.ecosystem for a in record.affected})
    if ECOSYSTEM not in ecosystems:
        return "not_pypi"
    if Path(rel).stem != record.id:
        return Quarantined(rel, "id_mismatch", f"file name does not match id {record.id}")
    if record.withdrawn:
        return "withdrawn"
    raw = compose_raw(record.summary, record.details)
    if not raw.strip():
        return "no_text"

    packages = {
        normalize_package_name(a.package.name)
        for a in record.affected
        if a.package.ecosystem == ECOSYSTEM
    }
    cwe_ids = record.database_specific.get("cwe_ids") or []
    return AdvisoryDocument(
        advisory_id=record.id,
        aliases=tuple(sorted(record.aliases)),
        published=record.published,
        modified=record.modified,
        summary=record.summary,
        details=record.details,
        pypi_packages=tuple(sorted(packages)),
        ecosystems=tuple(ecosystems),
        references=tuple(r.url for r in record.references),
        cwe_ids=tuple(sorted(str(c) for c in cwe_ids)),
        source_commit=source_commit,
        source_path=rel,
        file_sha256=sha256_bytes(data),
        content_hash=content_hash(raw),
    )


def _first_error(exc: ValidationError) -> str:
    err = exc.errors()[0]
    loc = ".".join(str(part) for part in err["loc"])
    return f"{loc}: {err['msg']}"


def write_corpus(
    result: IngestResult,
    out_dir: Path,
    source_commit: str,
    commit_date: str,
) -> dict[str, Any]:
    """Write the corpus JSONL and return the manifest describing it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = out_dir / CORPUS_FILE
    with corpus_path.open("w", encoding="utf-8", newline="\n") as fh:
        for doc in result.documents:
            fh.write(json.dumps(doc.model_dump(mode="json"), ensure_ascii=False, sort_keys=True))
            fh.write("\n")
    return {
        "source": {
            "repository": REPO_URL,
            "commit": source_commit,
            "commit_date": commit_date,
            "path": REVIEWED_DIR,
            "license": "CC-BY-4.0",
        },
        "filter": {"ecosystem": ECOSYSTEM, "exclude_withdrawn": True},
        "preprocessing_version": PREPROCESSING_VERSION,
        "counts": dict(sorted(result.counts.items())),
        "outputs": {CORPUS_FILE: sha256_file(corpus_path)},
        "quarantined": [q.__dict__ for q in result.quarantined],
    }


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_corpus(path: Path) -> list[AdvisoryDocument]:
    with path.open(encoding="utf-8") as fh:
        return [AdvisoryDocument.model_validate_json(line) for line in fh if line.strip()]
