"""Annotation batches drawn from a frozen split pool.

Strategies:
- ``natural``: uniform over the pool's documents. The only strategy allowed for dev and
  test, which must keep realistic class proportions.
- ``enriched``: from the top quartile of the condition-cue score (training only).
- ``uncertainty``: documents whose current predictions are least certain, mixed with a
  natural slice so training never concentrates only on unusual cases (training only).

Every strategy caps documents per leakage group and never repeats a document that is
already in any committed sample manifest.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from triggermap.corpus.cues import condition_score
from triggermap.ingest.records import AdvisoryDocument
from triggermap.schema.models import Extraction
from triggermap.text.preprocessing import compose_raw

Strategy = Literal["natural", "enriched", "uncertainty"]


class BatchParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    pool: Literal["train", "dev", "test"]
    n: int
    strategy: Strategy = "natural"
    per_group_cap: int = 3
    seed: int = 20261020
    natural_share: float = 0.3  # share of an uncertainty batch drawn naturally
    max_words: int | None = None


class BatchItem(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    order: int
    advisory_id: str
    pool: str
    stratum: str
    intended_use: Literal["training", "evaluation"]
    leakage_group: str
    content_hash: str
    condition_score: int
    words: int


def already_sampled(paths: Iterable[Path]) -> set[str]:
    """Advisory ids listed in existing sample manifests (pilot and batches)."""
    seen: set[str] = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        seen.update(item["advisory_id"] for item in data.get("items", []))
    return seen


def uncertainty(extraction: Extraction) -> float:
    """Higher when predictions sit near 0.5 confidence; 0 when there are none."""
    scores = [c.confidence for c in extraction.conditions if c.confidence is not None]
    if not scores:
        return 0.0
    return max(1 - abs(2 * s - 1) for s in scores)


def sample_batch(
    docs: Sequence[AdvisoryDocument],
    split_manifest: Mapping[str, Any],
    params: BatchParams,
    exclude: set[str],
    predictions: Mapping[str, Extraction] | None = None,
) -> list[BatchItem]:
    if params.pool != "train" and params.strategy != "natural":
        raise ValueError("dev and test batches must be natural samples")
    if params.strategy == "uncertainty" and predictions is None:
        raise ValueError("uncertainty sampling needs predictions")
    assignment = split_manifest["assignment"]
    group_of = split_manifest["group_of"]
    excluded = set(split_manifest.get("excluded_documents", {})) | exclude
    texts = {d.advisory_id: compose_raw(d.summary, d.details) for d in docs}
    words = {aid: len(t.split()) for aid, t in texts.items()}
    pool = sorted(
        d.advisory_id
        for d in docs
        if assignment.get(d.advisory_id) == params.pool
        and d.advisory_id not in excluded
        and (params.max_words is None or words[d.advisory_id] <= params.max_words)
    )
    scores = {aid: condition_score(texts[aid]) for aid in pool}
    rng = random.Random(f"{params.seed}:{params.name}")
    per_group: Counter[str] = Counter()
    chosen: list[tuple[str, str]] = []
    chosen_ids: set[str] = set()

    def take(candidates: Sequence[str], n: int, stratum: str) -> None:
        taken = 0
        for aid in candidates:
            if taken == n:
                break
            if aid in chosen_ids or per_group[group_of[aid]] >= params.per_group_cap:
                continue
            per_group[group_of[aid]] += 1
            chosen.append((aid, stratum))
            chosen_ids.add(aid)
            taken += 1
        if taken < n:
            raise ValueError(f"only {taken} of {n} {stratum} documents available in {params.pool}")

    natural = pool.copy()
    rng.shuffle(natural)
    if params.strategy == "natural":
        take(natural, params.n, "natural")
    elif params.strategy == "enriched":
        ordered = sorted(scores.values())
        # Top quartile, but never below 1: in a pool where most documents have no cue at
        # all, the quantile would be 0 and "enriched" would silently become "natural".
        threshold = max(1, ordered[int(0.75 * (len(ordered) - 1))] if ordered else 1)
        candidates = [aid for aid in natural if scores[aid] >= threshold]
        take(candidates, params.n, "enriched")
    else:
        assert predictions is not None
        n_natural = round(params.n * params.natural_share)
        ranked = sorted(
            (aid for aid in natural if aid in predictions),
            key=lambda aid: -uncertainty(predictions[aid]),
        )
        take(ranked, params.n - n_natural, "uncertainty")
        take(natural, n_natural, "natural")

    rng.shuffle(chosen)
    by_id = {d.advisory_id: d for d in docs}
    return [
        BatchItem(
            order=index,
            advisory_id=aid,
            pool=params.pool,
            stratum=stratum,
            intended_use="training" if params.pool == "train" else "evaluation",
            leakage_group=group_of[aid],
            content_hash=by_id[aid].content_hash,
            condition_score=scores[aid],
            words=words[aid],
        )
        for index, (aid, stratum) in enumerate(chosen)
    ]


def batch_manifest(
    items: Sequence[BatchItem], params: BatchParams, split_manifest: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "sample_version": params.name,
        "split_version": split_manifest["params"]["version"],
        "split_assignment_sha256": split_manifest["assignment_sha256"],
        "source_commit": split_manifest.get("source_commit"),
        "params": params.model_dump(),
        "counts": dict(Counter(item.stratum for item in items)),
        "items": [item.model_dump() for item in items],
    }
