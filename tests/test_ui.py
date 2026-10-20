import json
import re
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from tests.test_app import FLASK, db, make_client  # noqa: F401
from triggermap.serve.storage import Store


@pytest.fixture
def client(db: Path) -> Any:  # noqa: F811
    with make_client(db) as c:
        yield c


def payload(html: str) -> dict[str, Any]:
    m = re.search(r'<script id="payload" type="application/json">(.*?)</script>', html, re.S)
    assert m is not None
    return json.loads(m.group(1))  # type: ignore[no-any-return]


def test_home_and_static_assets(client: TestClient) -> None:
    home = client.get("/")
    assert home.status_code == 200
    assert "script-src 'self'" in home.headers["content-security-policy"]
    assert "Look up an advisory" in home.text and "Sign in to save reviews" in home.text
    assert client.get("/static/review.js").status_code == 200
    assert client.get("/static/app.css").status_code == 200


def test_review_page_for_an_advisory(client: TestClient) -> None:
    page = client.get(f"/ui/extract?id={FLASK}")
    assert page.status_code == 200
    html = page.text
    assert "<script>" not in html.replace('<script id="payload"', "")  # no inline code
    assert 'src="/static/review.js"' in html
    data = payload(html)
    assert data["mode"] == "new" and data["source"]["advisory_id"] == FLASK
    assert len(data["state"]["conditions"]) == 6
    segments = re.findall(r'class="seg[^"]*" data-start="(\d+)" data-end="(\d+)"', html)
    assert segments and all(int(a) < int(b) for a, b in segments)
    for c in data["state"]["conditions"]:  # every condition lies inside one rendered segment
        assert any(int(a) <= c["span"][0] and c["span"][1] <= int(b) for a, b in segments)
    assert "<ol>" in html  # list structure kept
    missing = client.get("/ui/extract?id=GHSA-2222-2222-2222")
    assert missing.status_code == 404 and "not in the served snapshot" in missing.text


def test_hostile_pasted_text_is_escaped(client: TestClient) -> None:
    hostile = 'Only affects deployments using <script>alert(1)</script> and "</script><b>x</b>".'
    page = client.post("/ui/extract", data={"text": hostile, "title": "<i>t</i>"})
    assert page.status_code == 200
    assert "<script>alert(1)" not in page.text and "<b>x</b>" not in page.text
    assert "&lt;i&gt;t&lt;/i&gt;" in page.text
    data = payload(page.text)
    assert data["source"]["text"] == hostile and data["title"] == "<i>t</i>"


def test_login_cookie_save_and_reopen(client: TestClient, db: Path) -> None:  # noqa: F811
    token = Store(db).create_user("ui-user")
    bad = client.post("/ui/login", data={"token": "nope"})
    assert bad.status_code == 401 and "not valid" in bad.text
    ok = client.post("/ui/login", data={"token": token}, follow_redirects=False)
    assert ok.status_code == 303
    cookie = ok.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    assert "Signed in as ui-user" in client.get("/").text

    data = payload(client.get(f"/ui/extract?id={FLASK}").text)
    assert data["logged_in"] is True
    body = {"advisory_id": FLASK, "title": data["title"], **data["meta"], "state": data["state"]}
    # The session cookie alone is not enough: state changes need an Idempotency-Key header.
    assert client.post("/v1/reviews", json=body).status_code == 400
    saved = client.post("/v1/reviews", json=body, headers={"Idempotency-Key": "ui-1"})
    assert saved.status_code == 201
    review_id = saved.json()["review_id"]
    reopened = client.get(f"/ui/reviews/{review_id}")
    assert reopened.status_code == 200
    again = payload(reopened.text)
    assert again["mode"] == "saved" and again["review_id"] == review_id
    assert again["history"][0]["seq"] == 1
    assert review_id in client.get("/").text  # listed on the home page

    client.post("/ui/logout")
    assert client.get(f"/ui/reviews/{review_id}", follow_redirects=False).status_code == 303


def test_osv_upload_page(client: TestClient) -> None:
    report = {
        "results": [
            {
                "packages": [
                    {
                        "package": {"name": "flask", "version": "2.3.1", "ecosystem": "PyPI"},
                        "vulnerabilities": [{"id": "CVE-2023-30861"}],
                    }
                ]
            }
        ]
    }
    files = {"report": ("report.json", json.dumps(report), "application/json")}
    page = client.post("/ui/osv", files=files)
    assert page.status_code == 200
    assert f"/ui/extract?id={FLASK}" in page.text and "extracted: <b>1</b>" in page.text
    bad = client.post("/ui/osv", files={"report": ("x.json", b"\xff\xfe", "application/json")})
    assert bad.status_code == 422 and "OSV-Scanner" in bad.text
