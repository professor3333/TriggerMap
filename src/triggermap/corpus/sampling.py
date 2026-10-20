"""Pilot sample selection.

Two strata, interleaved in a shuffled order so the annotator cannot tell them apart:
- ``random``: a natural sample (uniform over advisories, with a per-project cap so one
  templated project cannot dominate a 100-document pilot). These documents are
  evaluation candidates.
- ``enriched``: drawn from the top of the condition-cue distribution to make sure the
  label scheme meets enough conditions. These documents are training-only.

At most one advisory per duplicate group enters the pilot.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from triggermap.corpus.cues import condition_score
from triggermap.corpus.groups import Groups
from triggermap.ingest.records import AdvisoryDocument
from triggermap.text.preprocessing import compose_raw

SAMPLE_VERSION = "pilot-1"
Stratum = Literal["random", "enriched"]


class PilotItem(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    order: int
    advisory_id: str
    stratum: Stratum
    intended_use: Literal["evaluation_candidate", "training"]
    project_group: str
    content_hash: str
    condition_score: int
    words: int


class PilotParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    seed: int = 20261020
    n_random: int = 50
    n_enriched: int = 50
    per_project_cap: int = 2
    enriched_quantile: float = 0.75  # enriched candidates score at or above this quantile
    enriched_max_words: int = 800  # keeps enriched annotation effort bounded


def sample_pilot(
    docs: Sequence[AdvisoryDocument], groups: Groups, params: PilotParams
) -> list[PilotItem]:
    rng = random.Random(params.seed)
    by_id = {d.advisory_id: d for d in docs}
    texts = {d.advisory_id: compose_raw(d.summary, d.details) for d in docs}
    scores = {aid: condition_score(text) for aid, text in texts.items()}
    words = {aid: len(text.split()) for aid, text in texts.items()}

    per_project: Counter[str] = Counter()
    used_duplicates: set[str] = set()
    chosen: list[tuple[str, Stratum]] = []

    def take(candidates: list[str], n: int, stratum: Stratum) -> None:
        taken = 0
        for aid in candidates:
            if taken == n:
                return
            project, duplicate = groups.project[aid], groups.duplicate[aid]
            if duplicate in used_duplicates or per_project[project] >= params.per_project_cap:
                continue
            used_duplicates.add(duplicate)
            per_project[project] += 1
            chosen.append((aid, stratum))
            taken += 1
        if taken < n:
            raise ValueError(f"only {taken} of {n} {stratum} documents available")

    ids = sorted(d.advisory_id for d in docs)
    random_order = ids.copy()
    rng.shuffle(random_order)
    take(random_order, params.n_random, "random")

    ordered_scores = sorted(scores.values())
    threshold = ordered_scores[int(params.enriched_quantile * (len(ordered_scores) - 1))]
    enriched = [
        aid for aid in ids if scores[aid] >= threshold and words[aid] <= params.enriched_max_words
    ]
    rng.shuffle(enriched)
    take(enriched, params.n_enriched, "enriched")

    rng.shuffle(chosen)
    return [
        PilotItem(
            order=index,
            advisory_id=aid,
            stratum=stratum,
            intended_use="evaluation_candidate" if stratum == "random" else "training",
            project_group=groups.project[aid],
            content_hash=by_id[aid].content_hash,
            condition_score=scores[aid],
            words=words[aid],
        )
        for index, (aid, stratum) in enumerate(chosen)
    ]


def pilot_manifest(
    items: Sequence[PilotItem],
    params: PilotParams,
    snapshot_manifest: dict[str, Any],
    preprocessing_version: str,
) -> dict[str, Any]:
    return {
        "sample_version": SAMPLE_VERSION,
        "source_commit": snapshot_manifest["source"]["commit"],
        "corpus_sha256": snapshot_manifest["outputs"]["advisories.jsonl"],
        "preprocessing_version": preprocessing_version,
        "params": params.model_dump(),
        "counts": dict(Counter(item.stratum for item in items)),
        "items": [item.model_dump() for item in items],
    }
