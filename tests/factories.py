"""Small builders shared by tests."""

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
