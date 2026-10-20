"""Small builders shared by tests."""

from pathlib import Path

from triggermap.ingest.records import AdvisoryDocument
from triggermap.text.preprocessing import compose_raw, content_hash


def make_doc(
    advisory_id: str,
    details: str = "Plain text.",
    packages: tuple[str, ...] = ("pkg",),
    aliases: tuple[str, ...] = (),
    summary: str = "Summary",
) -> AdvisoryDocument:
    return AdvisoryDocument(
        advisory_id=advisory_id,
        aliases=aliases,
        published="2024-05-01T00:00:00Z",
        modified="2024-05-01T00:00:00Z",
        summary=summary,
        details=details,
        pypi_packages=packages,
        ecosystems=("PyPI",),
        references=(),
        cwe_ids=(),
        source_commit="c" * 40,
        source_path=f"advisories/github-reviewed/{advisory_id}.json",
        file_sha256="0" * 64,
        content_hash=content_hash(compose_raw(summary, details)),
    )


def write_split_manifest(path: Path, assignment: dict[str, str]) -> Path:
    """A minimal, internally consistent split manifest for CLI tests."""
    import json
    from collections import Counter

    from triggermap.corpus.splits import assignment_hash

    counts = Counter(assignment.values())
    manifest = {
        "params": {"version": "test"},
        "splits": {s: {"documents": counts.get(s, 0)} for s in ("train", "dev", "test")},
        "excluded_documents": {},
        "assignment_sha256": assignment_hash(assignment),
        "assignment": assignment,
        "group_of": {aid: aid for aid in assignment},
    }
    path.write_text(json.dumps(manifest))
    return path
