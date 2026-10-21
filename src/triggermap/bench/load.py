"""HTTP load test: N extraction requests at fixed concurrency against a running service."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from typing import Any


def _post(url: str, body: bytes, timeout: float) -> tuple[int, float]:
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
            status = resp.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except (urllib.error.URLError, TimeoutError):
        status = 0
    return status, time.perf_counter() - started


def load_test(
    base_url: str,
    texts: Sequence[str],
    requests: int = 1000,
    concurrency: int = 4,
    timeout: float = 60.0,
    unique: bool = True,
) -> dict[str, Any]:
    """With ``unique``, each request appends an HTML comment: the raw-text hash changes, so
    the prediction cache misses, but the comment is dropped from the canonical text, so the
    extraction work is identical. Without it, repeated texts measure cache hits."""
    url = base_url.rstrip("/") + "/v1/extractions"
    bodies = [
        json.dumps(
            {"text": texts[i % len(texts)] + (f"\n\n<!-- load-test {i} -->" if unique else "")}
        ).encode()
        for i in range(requests)
    ]
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        results = list(pool.map(lambda b: _post(url, b, timeout), bodies))
    elapsed = time.perf_counter() - started
    statuses = Counter(status for status, _ in results)
    ok = [latency for status, latency in results if status == 200]
    ordered = sorted(ok)
    last = len(ordered) - 1

    def pct(q: float) -> float | None:
        return round(ordered[round(q * last)], 4) if ordered else None

    return {
        "requests": requests,
        "concurrency": concurrency,
        "distinct_texts": min(len(texts), requests),
        "cache": "bypassed (unique raw text per request)" if unique else "repeated texts may hit",
        "succeeded": len(ok),
        "success_rate": round(len(ok) / requests, 5),
        "status_counts": {str(k): v for k, v in sorted(statuses.items())},
        "latency_s": {"p50": pct(0.5), "p95": pct(0.95), "p99": pct(0.99)},
        "throughput_rps": round(requests / elapsed, 2),
        "elapsed_s": round(elapsed, 2),
    }
