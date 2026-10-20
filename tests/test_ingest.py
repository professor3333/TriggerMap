import json
from pathlib import Path
from typing import Any

import pytest

from triggermap.ingest.build import (
    CORPUS_FILE,
    ingest,
    load_corpus,
    sha256_file,
    write_corpus,
    write_manifest,
)
from triggermap.ingest.records import normalize_package_name
from triggermap.text.preprocessing import compose_raw, content_hash

COMMIT = "c" * 40


def osv(advisory_id: str, *packages: tuple[str, str], **extra: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": "1.4.0",
        "id": advisory_id,
        "modified": "2024-01-02T00:00:00Z",
        "published": "2024-01-01T00:00:00Z",
        "aliases": ["CVE-2024-0001"],
        "summary": "Example is vulnerable",
        "details": "When `debug` is enabled, attackers can read files.",
        "affected": [{"package": {"ecosystem": e, "name": n}} for e, n in packages],
        "references": [{"type": "WEB", "url": "https://example.test"}],
        "database_specific": {"cwe_ids": ["CWE-22"], "github_reviewed": True},
    }
    record.update(extra)
    return record


def put(root: Path, name: str, content: bytes | dict[str, Any] | list[Any]) -> None:
    path = root / "advisories" / "github-reviewed" / "2024" / "01" / name / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content if isinstance(content, bytes) else json.dumps(content).encode()
    path.write_bytes(data)


@pytest.fixture
def snapshot(tmp_path: Path) -> Path:
    root = tmp_path / "advisory-database"
    put(root, "GHSA-2222-2222-2222", osv("GHSA-2222-2222-2222", ("PyPI", "Flask_Login")))
    put(
        root,
        "GHSA-3333-3333-3333",
        osv("GHSA-3333-3333-3333", ("npm", "left-pad"), ("PyPI", "Pkg.Two"), ("PyPI", "pkg-two")),
    )
    put(root, "GHSA-4444-4444-4444", osv("GHSA-4444-4444-4444", ("npm", "left-pad")))
    put(
        root,
        "GHSA-5555-5555-5555",
        osv("GHSA-5555-5555-5555", ("PyPI", "x"), withdrawn="2024-02-01T00:00:00Z"),
    )
    put(root, "GHSA-6666-6666-6666", b"{not json")
    put(root, "GHSA-7777-7777-7777", [1, 2])
    put(root, "GHSA-8888-8888-8888", osv("GHSA-8888-8888-8888", ("PyPI", "x"), affected=[]))
    put(root, "GHSA-9999-9999-9999", osv("GHSA-cccc-cccc-cccc", ("PyPI", "x")))
    put(root, "GHSA-cccc-2222-2222", b"\xff\xfe")
    put(
        root,
        "GHSA-fff2-2222-2222",
        osv("GHSA-fff2-2222-2222", ("PyPI", "x"), summary="", details="  "),
    )
    return root


def test_every_file_lands_in_exactly_one_bucket(snapshot: Path) -> None:
    result = ingest(snapshot, COMMIT)
    assert dict(result.counts) == {
        "scanned": 10,
        "kept": 2,
        "excluded:not_pypi": 1,
        "excluded:withdrawn": 1,
        "excluded:no_text": 1,
        "quarantined:invalid_json": 1,
        "quarantined:not_an_object": 1,
        "quarantined:schema_invalid": 1,
        "quarantined:id_mismatch": 1,
        "quarantined:invalid_utf8": 1,
    }
    assert sum(v for k, v in result.counts.items() if k != "scanned") == 10
    reasons = {q.path.split("/")[-2]: q.reason for q in result.quarantined}
    assert reasons["GHSA-8888-8888-8888"] == "schema_invalid"
    assert reasons["GHSA-9999-9999-9999"] == "id_mismatch"


def test_kept_documents_carry_provenance(snapshot: Path) -> None:
    docs = ingest(snapshot, COMMIT).documents
    assert [d.advisory_id for d in docs] == ["GHSA-2222-2222-2222", "GHSA-3333-3333-3333"]
    first, second = docs
    assert first.pypi_packages == ("flask-login",)
    assert second.pypi_packages == ("pkg-two",)
    assert second.ecosystems == ("PyPI", "npm")
    assert first.content_hash == content_hash(compose_raw(first.summary, first.details))
    assert first.source_commit == COMMIT
    assert first.source_path.startswith("advisories/github-reviewed/")
    assert first.file_sha256 == sha256_file(snapshot / first.source_path)


def test_outputs_are_deterministic_and_round_trip(snapshot: Path, tmp_path: Path) -> None:
    manifests = []
    for run in ("a", "b"):
        out = tmp_path / run
        manifest = write_corpus(ingest(snapshot, COMMIT), out, COMMIT, "2024-01-03T00:00:00Z")
        write_manifest(manifest, out / "manifest.json")
        manifests.append((out / "manifest.json").read_bytes())
    assert manifests[0] == manifests[1]
    manifest = json.loads(manifests[0])
    assert manifest["source"]["commit"] == COMMIT
    assert manifest["outputs"][CORPUS_FILE] == sha256_file(tmp_path / "a" / CORPUS_FILE)
    assert {q["reason"] for q in manifest["quarantined"]} == {
        "invalid_json",
        "not_an_object",
        "schema_invalid",
        "id_mismatch",
        "invalid_utf8",
    }
    assert len(load_corpus(tmp_path / "a" / CORPUS_FILE)) == 2


@pytest.mark.parametrize(
    "name, expected",
    [("Flask", "flask"), ("Flask_Login", "flask-login"), ("zope.interface", "zope-interface")],
)
def test_pep503_normalisation(name: str, expected: str) -> None:
    assert normalize_package_name(name) == expected
