"""Deploy verification: the running service matches its release and works end to end.

Checks, in order:
1. ``/readyz`` reports ready, and its model id, weights digest, preprocessing version,
   review-policy version, release id and label inventory match ``release.json``;
2. a bundled sample advisory goes through extraction -> review -> export, and the saved
   review can be read back.
Any mismatch is a failed deployment.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import uuid
from importlib import resources
from typing import Any

from triggermap.schema.models import Category, DocumentStatus, GroupOperator, Role


class VerificationError(Exception):
    pass


def _request(
    url: str, method: str = "GET", body: Any = None, headers: dict[str, str] | None = None
) -> tuple[int, Any, str]:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw, status = exc.read().decode(), exc.code
    try:
        return status, json.loads(raw), raw
    except json.JSONDecodeError:
        return status, None, raw


def sample_text() -> str:
    return resources.files("triggermap.serve.samples").joinpath("sample_advisory.md").read_text()


def verify(base_url: str, release: dict[str, Any], token: str) -> list[str]:
    """Return the checks performed; raise VerificationError on the first failure."""
    base = base_url.rstrip("/")
    done: list[str] = []
    status, ready, _ = _request(f"{base}/readyz")
    if status != 200 or ready.get("status") != "ready":
        raise VerificationError(f"/readyz returned {status}")
    expected = {
        "release": release["release_id"],
        "model_id": release["model_id"],
        "weights_sha256": release["weights_sha256"],
        "preprocessing_version": release["preprocessing_version"],
        "review_policy_version": release["review_policy_version"],
        "accept_threshold": release["accept_threshold"],
    }
    for key, value in expected.items():
        if ready.get(key) != value:
            raise VerificationError(f"/readyz {key}={ready.get(key)!r}, release has {value!r}")
    inventory = {
        "categories": [c.value for c in Category],
        "roles": [r.value for r in Role],
        "group_operators": [g.value for g in GroupOperator],
        "document_statuses": [s.value for s in DocumentStatus],
    }
    if ready.get("label_inventory") != inventory:
        raise VerificationError("label inventory differs from this build's schema")
    done.append("readyz matches release")

    status, extraction, _ = _request(
        f"{base}/v1/extractions", "POST", {"text": sample_text(), "title": "Deploy check"}
    )
    if status != 200 or not extraction.get("conditions"):
        raise VerificationError(f"sample extraction failed ({status})")
    if extraction["model_id"] != release["model_id"]:
        raise VerificationError("extraction came from a different model")
    done.append(f"extraction: {len(extraction['conditions'])} conditions")

    auth = {"Authorization": f"Bearer {token}", "Idempotency-Key": f"deploy-{uuid.uuid4()}"}
    state = {
        "document_status": extraction["document_status"],
        "conditions": [
            {k: c[k] for k in ("id", "span", "category", "role", "source")} | {"answer": "UNKNOWN"}
            for c in extraction["conditions"]
        ],
        "groups": extraction["groups"],
        "notes": "deploy verification",
    }
    body = {
        "text": sample_text(),
        "title": "Deploy check",
        "model_id": extraction["model_id"],
        "content_hash": extraction["content_hash"],
        "preprocessing_version": extraction["preprocessing_version"],
        "review_policy_version": extraction["review_policy_version"],
        "state": state,
    }
    status, created, raw = _request(f"{base}/v1/reviews", "POST", body, auth)
    if status != 201:
        raise VerificationError(f"saving the review failed ({status}): {raw[:200]}")
    review_id = created["review_id"]
    status, retry, _ = _request(f"{base}/v1/reviews", "POST", body, auth)
    if status != 200 or retry.get("review_id") != review_id:
        raise VerificationError("a retried save did not return the same review")
    done.append("review saved; retry idempotent")

    read_auth = {"Authorization": auth["Authorization"]}
    status, review, _ = _request(f"{base}/v1/reviews/{review_id}", headers=read_auth)
    if status != 200 or len(review["history"]) != 1:
        raise VerificationError("the saved review could not be read back intact")
    status, _, markdown = _request(
        f"{base}/v1/reviews/{review_id}/export?format=markdown", headers=read_auth
    )
    if status != 200 or "Exposure review" not in markdown:
        raise VerificationError("markdown export failed")
    done.append("review retrievable; export works")
    return done
