"""The declared benchmark workload: real advisories bucketed by subword length.

Documents come only from the train and dev pools (test text is never used). Lengths are
counted with a fixed reference tokenizer, so the workload is the same whichever model is
benchmarked:
- ``~512``: 448 to 576 tokens;
- ``~2000``: 1,750 to 2,250 tokens;
- ``natural``: a uniform sample, for throughput and the length distribution.
"""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from typing import Any

from triggermap.ingest.records import AdvisoryDocument
from triggermap.text.preprocessing import compose_raw, preprocess

WORKLOAD_VERSION = "workload-v1"
REFERENCE_TOKENIZER = "distilbert/distilbert-base-cased"
REFERENCE_REVISION = "6ea81172465e8b0ad3fddeed32b986cdcdcffcf0"
BUCKETS = {"~512": (448, 576), "~2000": (1750, 2250)}


def _percentiles(values: Sequence[int]) -> dict[str, int]:
    ordered = sorted(values)
    if not ordered:
        return {}
    last = len(ordered) - 1
    return {f"p{q}": ordered[round(q / 100 * last)] for q in (10, 50, 90, 99)} | {
        "max": ordered[-1]
    }


def build_workload(
    docs: Sequence[AdvisoryDocument],
    split: Mapping[str, Any],
    tokenizer: Any,
    per_bucket: int = 20,
    natural: int = 100,
    seed: int = 0,
) -> dict[str, Any]:
    pool = sorted(
        (d for d in docs if split["assignment"].get(d.advisory_id) in ("train", "dev")),
        key=lambda d: d.advisory_id,
    )
    rng = random.Random(seed)
    rng.shuffle(pool)
    tokens: dict[str, int] = {}

    def count(doc: AdvisoryDocument) -> int:
        if doc.advisory_id not in tokens:
            text = preprocess(compose_raw(doc.summary, doc.details)).text
            ids = tokenizer(text, add_special_tokens=False, verbose=False)["input_ids"]
            tokens[doc.advisory_id] = len(ids)
        return tokens[doc.advisory_id]

    buckets: dict[str, list[dict[str, Any]]] = {name: [] for name in BUCKETS}
    for doc in pool:
        if all(len(v) >= per_bucket for v in buckets.values()):
            break
        n = count(doc)
        for name, (low, high) in BUCKETS.items():
            if low <= n <= high and len(buckets[name]) < per_bucket:
                buckets[name].append({"advisory_id": doc.advisory_id, "tokens": n})
    natural_items: list[dict[str, Any]] = [
        {"advisory_id": d.advisory_id, "tokens": count(d)} for d in pool[:natural]
    ]
    return {
        "version": WORKLOAD_VERSION,
        "tokenizer": {"name": REFERENCE_TOKENIZER, "revision": REFERENCE_REVISION},
        "source": "train and dev pools of splits/pool-v1.json",
        "seed": seed,
        "buckets": buckets | {"natural": natural_items},
        "natural_token_distribution": _percentiles([i["tokens"] for i in natural_items]),
    }
