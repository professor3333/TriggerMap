"""Leakage-safe split pools over the whole corpus, frozen before scaled annotation.

Every advisory is assigned to the train, dev or test *pool* by leakage group, so later
annotation batches are drawn from a pool and can never leak across splits:

1. Leakage groups union shared packages, shared upstream repositories, exact duplicates,
   shared aliases and near-duplicate text.
2. Pilot constraints: a group containing a random-stratum (evaluation candidate) pilot
   document goes to an evaluation pool; a group containing only training-stratum pilot
   documents goes to train. When one group holds both, evaluation wins (natural samples
   are the scarcer resource) and its training-stratum documents are listed under
   ``excluded_documents``: annotated, but used neither for training nor for scoring.
3. Test takes the *newest* eligible project groups (by first publication) up to its share
   of documents, so test measures temporal and project shift. Very large groups are not
   eligible for evaluation pools, so no single project dominates them.
4. Dev holds every remaining evaluation-candidate group (including large ones, so big
   projects stay represented) plus a seeded random sample of small and medium groups;
   only the latter count toward dev's share, so dev spans many projects. Annotation
   batches drawn from evaluation pools cap documents per group. Train gets the rest.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from triggermap.corpus.groups import Groups
from triggermap.ingest.records import AdvisoryDocument

Split = Literal["train", "dev", "test"]
SPLITS: tuple[Split, ...] = ("train", "dev", "test")


class SplitParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    version: str = "pool-v1"
    seed: int = 20261020
    dev_fraction: float = 0.1875  # 150 of 800 planned gold documents
    test_fraction: float = 0.1875
    max_eval_group_docs: int = 25  # larger groups always train
    near_duplicate_threshold: float = 0.6


def assignment_hash(assignment: Mapping[str, str]) -> str:
    lines = "\n".join(f"{aid}\t{split}" for aid, split in sorted(assignment.items()))
    return hashlib.sha256(lines.encode()).hexdigest()


def build_split(
    docs: Sequence[AdvisoryDocument],
    groups: Groups,
    params: SplitParams,
    pilot_items: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    members: dict[str, list[AdvisoryDocument]] = {}
    for doc in docs:
        members.setdefault(groups.leakage[doc.advisory_id], []).append(doc)

    want_eval = {groups.leakage[i["advisory_id"]] for i in pilot_items if i["stratum"] == "random"}
    enriched = [i["advisory_id"] for i in pilot_items if i["stratum"] == "enriched"]
    force_train = {groups.leakage[aid] for aid in enriched} - want_eval
    excluded = sorted(aid for aid in enriched if groups.leakage[aid] in want_eval)
    total = len(docs)
    first_published = {key: min(d.published for d in group) for key, group in members.items()}
    eligible = {
        key
        for key, group in members.items()
        if key not in force_train and (len(group) <= params.max_eval_group_docs or key in want_eval)
    }

    split_of: dict[str, Split] = {}
    sizes: Counter[str] = Counter()

    def place(key: str, split: Split) -> None:
        split_of[key] = split
        sizes[split] += len(members[key])

    # Test: newest eligible groups within the size cap (ties broken by key for determinism).
    small = {k for k in eligible if len(members[k]) <= params.max_eval_group_docs}
    for key in sorted(small, key=lambda k: (first_published[k], k), reverse=True):
        if sizes["test"] >= params.test_fraction * total:
            break
        place(key, "test")
    # Dev: evaluation-candidate groups not in test come first, then a seeded random draw.
    rng = random.Random(params.seed)
    rest = sorted(k for k in eligible if k not in split_of)
    rng.shuffle(rest)
    rest.sort(key=lambda k: k not in want_eval)  # stable: wanted-eval groups first
    capped = 0  # dev documents in groups within the size cap
    for key in rest:
        if key not in want_eval and capped >= params.dev_fraction * total:
            continue
        place(key, "dev")
        capped += len(members[key]) if key in small else 0
    for key in members:
        if key not in split_of:
            place(key, "train")

    assignment = {d.advisory_id: split_of[groups.leakage[d.advisory_id]] for d in docs}
    per_split: dict[str, dict[str, Any]] = {}
    for split in SPLITS:
        keys = [k for k, s in split_of.items() if s == split]
        dates = sorted(d.published for k in keys for d in members[k])
        per_split[split] = {
            "documents": sum(len(members[k]) for k in keys),
            "leakage_groups": len(keys),
            "groups_over_cap": sum(len(members[k]) > params.max_eval_group_docs for k in keys),
            "published_from": dates[0][:10] if dates else None,
            "published_to": dates[-1][:10] if dates else None,
            "pilot_random": sum(
                1
                for i in pilot_items
                if i["stratum"] == "random" and assignment[i["advisory_id"]] == split
            ),
            "pilot_enriched": sum(
                1
                for i in pilot_items
                if i["stratum"] == "enriched" and assignment[i["advisory_id"]] == split
            ),
        }
    largest = max((len(g) for g in members.values()), default=0)
    return {
        "params": params.model_dump(),
        "frozen": True,
        "splits": per_split,
        "leakage_groups": len(members),
        "largest_group_documents": largest,
        "excluded_documents": {
            aid: "training-stratum pilot document in an evaluation group" for aid in excluded
        },
        "assignment_sha256": assignment_hash(assignment),
        "assignment": dict(sorted(assignment.items())),
        "group_of": {
            d.advisory_id: groups.leakage[d.advisory_id]
            for d in sorted(docs, key=lambda d: d.advisory_id)
        },
    }


def check_split_manifest(manifest: Mapping[str, Any]) -> list[str]:
    """Problems with a split manifest; empty means it is internally consistent."""
    problems: list[str] = []
    assignment: Mapping[str, str] = manifest["assignment"]
    group_of: Mapping[str, str] = manifest["group_of"]
    for aid in manifest.get("excluded_documents", {}):
        if assignment.get(aid) == "train":
            problems.append(f"{aid}: excluded document assigned to train")
    if assignment_hash(assignment) != manifest["assignment_sha256"]:
        problems.append("assignment does not match assignment_sha256")
    if set(assignment) != set(group_of):
        problems.append("assignment and group_of cover different documents")
    split_of_group: dict[str, set[str]] = {}
    for aid, split in assignment.items():
        if split not in SPLITS:
            problems.append(f"{aid}: unknown split {split}")
        split_of_group.setdefault(group_of.get(aid, aid), set()).add(split)
    crossing = [g for g, s in split_of_group.items() if len(s) > 1]
    if crossing:
        problems.append(f"{len(crossing)} leakage groups span several splits, e.g. {crossing[0]}")
    counts = Counter(assignment.values())
    for split in SPLITS:
        if manifest["splits"][split]["documents"] != counts.get(split, 0):
            problems.append(f"{split}: document count does not match assignment")
    return problems


def load_split(path: Any) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        manifest: dict[str, Any] = json.load(fh)
    problems = check_split_manifest(manifest)
    if problems:
        raise ValueError(f"invalid split manifest {path}: {problems}")
    return manifest


def select(advisory_ids: Sequence[str], manifest: Mapping[str, Any], split: Split) -> list[str]:
    """Ids in ``split``, minus excluded documents; unknown ids are an error, not a skip."""
    assignment: Mapping[str, str] = manifest["assignment"]
    unknown = [aid for aid in advisory_ids if aid not in assignment]
    if unknown:
        raise ValueError(f"{len(unknown)} documents are not in the split manifest: {unknown[:3]}")
    excluded = manifest.get("excluded_documents", {})
    return [aid for aid in advisory_ids if assignment[aid] == split and aid not in excluded]
