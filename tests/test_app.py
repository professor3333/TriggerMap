import json
import logging
import sqlite3
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from triggermap.serve.app import Service, Settings, create_app
from triggermap.serve.storage import AdvisoryRecord, Store
from triggermap.text.preprocessing import compose_raw, content_hash

ROOT = Path(__file__).resolve().parents[1]
AIOHTTP, FLASK = "GHSA-5h86-8mv2-jq9f", "GHSA-m2qf-hxjv-5gpq"


def fixture_record(advisory_id: str) -> tuple[AdvisoryRecord, list[str]]:
    data = json.loads((ROOT / f"tests/fixtures/advisories/{advisory_id}.json").read_text())
    raw = compose_raw(data["summary"], data["details"])
    record = AdvisoryRecord(
        advisory_id, content_hash(raw), raw, data["summary"], ("pkg",), data["published"], "c" * 40
    )
    return record, data["aliases"]


@pytest.fixture
def db(tmp_path: Path) -> Path:
    store = Store(tmp_path / "app.db")
    store.upsert_advisories([fixture_record(AIOHTTP), fixture_record(FLASK)])
    store.set_meta("snapshot_commit", "c" * 40)
    return tmp_path / "app.db"


def make_client(db: Path, **overrides: Any) -> TestClient:
    settings = Settings(database=db, review_policy=ROOT / "configs/review_policy.yaml", **overrides)
    return TestClient(create_app(settings, lambda: Service(settings)))


@pytest.fixture
def client(db: Path) -> Any:
    with make_client(db) as c:
        yield c


@pytest.fixture
def token(db: Path) -> str:
    return Store(db).create_user("reviewer")


def test_health_and_version_info(client: TestClient) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}
    ready = client.get("/readyz").json()
    assert ready["status"] == "ready"
    assert ready["model_id"] == "rules-2" and len(ready["weights_sha256"]) == 64
    assert ready["preprocessing_version"] == "1"
    assert ready["review_policy_version"] == "review-policy-0"
    assert ready["accept_threshold"] is None and ready["calibration"] == {"method": "identity"}
    assert ready["label_inventory"]["roles"] == [
        "REQUIRED",
        "EXCEPTION",
        "NOT_REQUIRED",
        "UNCERTAIN",
    ]
    assert ready["advisories"] == 2 and ready["snapshot_commit"] == "c" * 40


def test_extraction_by_id_alias_and_text(client: TestClient) -> None:
    by_id = client.post("/v1/extractions", json={"advisory_id": FLASK}).json()
    assert by_id["advisory_id"] == FLASK and by_id["cached"] is False
    assert by_id["source_url"] == f"https://github.com/advisories/{FLASK}"
    assert len(by_id["conditions"]) == 6 and by_id["groups"][0]["operator"] == "ALL"
    first = by_id["conditions"][1]
    assert by_id["text"][first["span"][0] : first["span"][1]] == first["surface"]
    assert all(c["review_reasons"] for c in by_id["conditions"])  # uncalibrated policy
    assert "review_policy:review-policy-0" in by_id["review_flags"]
    by_alias = client.post("/v1/extractions", json={"advisory_id": "CVE-2023-30861"}).json()
    assert by_alias["advisory_id"] == FLASK and by_alias["cached"] is True
    pasted = client.post(
        "/v1/extractions", json={"text": "Only affects deployments using the legacy API."}
    ).json()
    assert pasted["advisory_id"] is None and pasted["title"] == "Pasted advisory"
    assert pasted["conditions"][0]["surface"] == "using the legacy API"


@pytest.mark.parametrize(
    "body, status, code",
    [
        ({"advisory_id": FLASK, "text": "x"}, 422, "invalid_request"),
        ({}, 422, "invalid_request"),
        ({"advisory_id": "GHSA-2222-2222-2222"}, 404, "unknown_advisory"),
        ({"text": "x", "extra": 1}, 422, "invalid_request"),
    ],
)
def test_extraction_errors(
    client: TestClient, body: dict[str, Any], status: int, code: str
) -> None:
    response = client.post("/v1/extractions", json=body)
    assert response.status_code == status
    assert response.json()["error"]["code"] == code


def test_body_encoding_and_size_errors(db: Path) -> None:
    with make_client(db, max_body_bytes=200, max_text_chars=50) as c:
        bad_utf8 = c.post("/v1/extractions", content=b'{"text": "\xff\xfe"}')
        assert (bad_utf8.status_code, bad_utf8.json()["error"]["code"]) == (400, "invalid_utf8")
        not_json = c.post("/v1/extractions", content=b"{not json")
        assert not_json.json()["error"]["code"] == "invalid_json"
        big = c.post("/v1/extractions", json={"text": "a" * 500})
        assert (big.status_code, big.json()["error"]["code"]) == (413, "payload_too_large")
        long = c.post("/v1/extractions", json={"text": "word " * 20})
        assert (long.status_code, long.json()["error"]["code"]) == (413, "text_too_long")


def test_condition_limit_and_overload(db: Path) -> None:
    with make_client(db, max_conditions=2) as c:
        r = c.post("/v1/extractions", json={"advisory_id": FLASK})
        assert (r.status_code, r.json()["error"]["code"]) == (422, "too_many_conditions")
    with make_client(db, max_concurrency=0, queue_timeout_seconds=0.05) as c:
        r = c.post("/v1/extractions", json={"advisory_id": FLASK})
        assert (r.status_code, r.json()["error"]["code"]) == (503, "overloaded")
        assert r.headers["retry-after"] == "5"


def test_osv_scanner_import(client: TestClient) -> None:
    report = {
        "results": [
            {
                "source": {"path": "requirements.txt", "type": "lockfile"},
                "packages": [
                    {
                        "package": {"name": "flask", "version": "2.3.1", "ecosystem": "PyPI"},
                        "vulnerabilities": [{"id": FLASK, "aliases": ["CVE-2023-30861"]}],
                    },
                    {
                        "package": {"name": "aiohttp", "version": "3.9.1", "ecosystem": "PyPI"},
                        "vulnerabilities": [{"id": "PYSEC-2024-24", "aliases": ["CVE-2024-23334"]}],
                    },
                    {
                        "package": {"name": "requests", "version": "2.0", "ecosystem": "PyPI"},
                        "vulnerabilities": [{"id": "GHSA-2222-2222-2222"}],
                    },
                    {
                        "package": {"name": "left-pad", "version": "1.0", "ecosystem": "npm"},
                        "vulnerabilities": [{"id": "GHSA-3333-3333-3333"}],
                    },
                ],
            }
        ]
    }
    out = client.post("/v1/imports/osv", json=report).json()
    assert out["counts"] == {"extracted": 2, "not_in_snapshot": 1, "unsupported_ecosystem": 1}
    aiohttp = next(i for i in out["items"] if i["package"] == "aiohttp")
    assert aiohttp["advisory_id"] == AIOHTTP and aiohttp["conditions"] > 0
    for malformed in ({"packages": []}, {"results": [{"packages": [{"vulnerabilities": [{}]}]}]}):
        r = client.post("/v1/imports/osv", json=malformed)
        assert (r.status_code, r.json()["error"]["code"]) == (422, "unsupported_osv_format")


def review_body(client: TestClient, answer: str = "PRESENT") -> dict[str, Any]:
    ex = client.post("/v1/extractions", json={"advisory_id": FLASK}).json()
    conditions = [
        {
            "id": c["id"],
            "span": c["span"],
            "category": c["category"],
            "role": c["role"],
            "source": c["source"],
            "answer": answer,
        }
        for c in ex["conditions"]
    ]
    return {
        "advisory_id": FLASK,
        "model_id": ex["model_id"],
        "content_hash": ex["content_hash"],
        "preprocessing_version": ex["preprocessing_version"],
        "review_policy_version": ex["review_policy_version"],
        "state": {
            "document_status": ex["document_status"],
            "conditions": conditions,
            "groups": ex["groups"],
            "notes": "checked against our deployment",
        },
    }


def test_review_lifecycle_idempotency_and_history(client: TestClient, token: str, db: Path) -> None:
    auth = {"Authorization": f"Bearer {token}"}
    body = review_body(client)
    assert client.post("/v1/reviews", json=body).status_code == 401
    missing = client.post("/v1/reviews", json=body, headers=auth)
    assert missing.json()["error"]["code"] == "missing_idempotency_key"

    headers = {**auth, "Idempotency-Key": "create-1"}
    first = client.post("/v1/reviews", json=body, headers=headers)
    assert first.status_code == 201
    review_id = first.json()["review_id"]
    retry = client.post("/v1/reviews", json=body, headers=headers)
    assert retry.status_code == 200 and retry.json() == {"review_id": review_id, "created": False}
    changed = client.post("/v1/reviews", json=review_body(client, "ABSENT"), headers=headers)
    assert changed.status_code == 409

    revised = body["state"] | {"notes": "proxy confirmed"}
    revised["conditions"] = [c | {"answer": "ABSENT"} for c in body["state"]["conditions"]]
    rev_headers = {**auth, "Idempotency-Key": "rev-1"}
    url = f"/v1/reviews/{review_id}/revisions"
    assert client.post(
        url, json={"state": revised, "note": "second pass"}, headers=rev_headers
    ).json() == {
        "review_id": review_id,
        "seq": 2,
        "created": True,
    }
    again = client.post(url, json={"state": revised, "note": "second pass"}, headers=rev_headers)
    assert again.status_code == 200 and again.json()["seq"] == 2

    review = client.get(f"/v1/reviews/{review_id}", headers=auth).json()
    assert [h["seq"] for h in review["history"]] == [1, 2]
    assert review["state"]["notes"] == "proxy confirmed"
    assert review["states"][0]["conditions"][0]["answer"] == "PRESENT"  # history kept
    assert review["advisory_changed"] is False

    with sqlite3.connect(db) as raw:  # the database itself refuses to rewrite history
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            raw.execute("UPDATE review_events SET note='x'")
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            raw.execute("DELETE FROM review_events")

    md = client.get(f"/v1/reviews/{review_id}/export?format=markdown", headers=auth)
    assert md.headers["content-disposition"].endswith('.md"')
    assert "## ALL group (all must hold)" in md.text and "| ABSENT |" in md.text
    exported = client.get(f"/v1/reviews/{review_id}/export", headers=auth).json()
    surfaces = [c["surface"] for c in exported["conditions"]]
    assert "sets session.permanent = True" in surfaces
    assert exported["content_hash"] == body["content_hash"]

    other = Store(db).create_user("someone-else")
    assert (
        client.get(
            f"/v1/reviews/{review_id}", headers={"Authorization": f"Bearer {other}"}
        ).status_code
        == 404
    )


def test_invalid_review_states_and_stale_text(client: TestClient, token: str) -> None:
    auth = {"Authorization": f"Bearer {token}"}
    body = review_body(client)
    bad = json.loads(json.dumps(body))
    bad["state"]["conditions"][0]["span"] = [0, 10_000]
    r = client.post("/v1/reviews", json=bad, headers={**auth, "Idempotency-Key": "k1"})
    assert (r.status_code, r.json()["error"]["code"]) == (422, "invalid_review_state")
    stale = body | {"content_hash": "0" * 64}
    r = client.post("/v1/reviews", json=stale, headers={**auth, "Idempotency-Key": "k2"})
    assert (r.status_code, r.json()["error"]["code"]) == (409, "advisory_changed")
    human = json.loads(json.dumps(body))
    human["state"]["conditions"].append(
        {"id": "h1", "span": [0, 5], "category": "USAGE", "role": "UNCERTAIN", "source": "human"}
    )
    r = client.post("/v1/reviews", json=human, headers={**auth, "Idempotency-Key": "k3"})
    assert r.status_code == 201


def test_reviews_survive_restart_and_detect_advisory_change(db: Path, token: str) -> None:
    auth = {"Authorization": f"Bearer {token}"}
    with make_client(db) as c:
        review_id = c.post(
            "/v1/reviews", json=review_body(c), headers={**auth, "Idempotency-Key": "r1"}
        ).json()["review_id"]
    record, aliases = fixture_record(FLASK)
    changed_text = record.raw_text + "\n\nUpdated: also affects 2.3.3."
    updated = replace(record, raw_text=changed_text, content_hash=content_hash(changed_text))
    Store(db).upsert_advisories([(updated, aliases)])
    with make_client(db) as c:  # a fresh app instance: the review is still there
        review = c.get(f"/v1/reviews/{review_id}", headers=auth).json()
        assert review["advisory_changed"] is True
        assert review["current_content_hash"] != review["content_hash"]
        assert len(c.get("/v1/reviews", headers=auth).json()) == 1


def test_metrics_and_logs_never_contain_submitted_text(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    secret = "Only affects deployments using the internal-codename-zebra cluster."
    with caplog.at_level(logging.INFO, logger="triggermap.access"):
        client.post("/v1/extractions", json={"text": secret})
    assert "zebra" not in caplog.text and caplog.records
    metrics = client.get("/metrics").text
    assert "triggermap_requests_total" in metrics and "zebra" not in metrics
    assert 'route="/v1/extractions"' in metrics
