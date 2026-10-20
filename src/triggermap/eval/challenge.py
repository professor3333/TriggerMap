"""Constructed challenge set: minimal pairs that probe negation, scope and roles.

Kept separate from the real-advisory test set and always reported separately. Items are
authored as surface strings (not offsets); loading resolves each surface to canonical
offsets and fails loudly on a missing or ambiguous surface. Only ``verified`` items are
scored; drafts are reported apart and never mixed in.

JSONL item:
    {"id": "neg-01a", "family": "negation_flip", "pair": "neg-01", "status": "verified",
     "text": "...markdown...",
     "conditions": [{"surface": "...", "occurrence": 1, "category": "USAGE",
                     "role": "REQUIRED"}],
     "groups": [{"operator": "ALL", "members": [0, 1]}],
     "note": "..."}
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from triggermap.eval.metrics import DocCounts, doc_counts, summary
from triggermap.schema.models import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import PreprocessedDocument, preprocess

Family = Literal[
    "negation_flip",
    "required_vs_unnecessary",
    "conjunction_flip",
    "prerequisite_vs_workaround",
    "paraphrase_no_cue",
    "formatting",
]


class ChallengeCondition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: str = Field(min_length=1)
    occurrence: int = Field(default=1, ge=1)
    category: Category
    role: Role


class ChallengeGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operator: GroupOperator
    members: list[int]


class ChallengeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    family: Family
    pair: str | None = None
    status: Literal["draft", "verified"] = "draft"
    text: str
    conditions: list[ChallengeCondition] = []
    groups: list[ChallengeGroup] = []
    note: str | None = None


@dataclass(frozen=True)
class Resolved:
    item: ChallengeItem
    doc: PreprocessedDocument
    gold: Extraction


def resolve(item: ChallengeItem) -> Resolved:
    doc = preprocess(item.text)
    conditions = []
    for index, cond in enumerate(item.conditions):
        start = -1
        for _ in range(cond.occurrence):
            start = doc.text.find(cond.surface, start + 1)
            if start < 0:
                raise ValueError(f"{item.id}: surface {cond.surface!r} not found")
        conditions.append(
            Condition(
                id=f"c{index + 1}",
                span=(start, start + len(cond.surface)),
                category=cond.category,
                role=cond.role,
            )
        )
    groups = tuple(
        Group(operator=g.operator, members=tuple(f"c{m + 1}" for m in g.members))
        for g in item.groups
    )
    gold = Extraction(
        content_hash=doc.content_hash,
        preprocessing_version=doc.version,
        model_id="challenge-gold",
        document_status=(
            DocumentStatus.HAS_CONDITIONS if conditions else DocumentStatus.NO_EXPLICIT_CONDITION
        ),
        conditions=tuple(conditions),
        groups=groups,
    )
    return Resolved(item, doc, gold)


def load(path: Path) -> list[Resolved]:
    items = []
    seen: set[str] = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        item = ChallengeItem.model_validate(json.loads(line))
        if item.id in seen:
            raise ValueError(f"line {line_no}: duplicate id {item.id}")
        seen.add(item.id)
        items.append(resolve(item))
    return items


@dataclass(frozen=True)
class FamilyScore:
    family: str
    items: int
    typed_f1: float
    doc_exact: float
    pairs: int
    pairs_both_exact: int


def score(items: Sequence[Resolved], extractor: Any) -> tuple[list[FamilyScore], list[DocCounts]]:
    counts: list[DocCounts] = []
    by_family: dict[str, list[DocCounts]] = {}
    exact_by_pair: dict[str, list[bool]] = {}
    for resolved in items:
        prediction = extractor.extract(resolved.doc, None)
        dc = doc_counts(resolved.item.id, resolved.gold, prediction)
        counts.append(dc)
        by_family.setdefault(resolved.item.family, []).append(dc)
        if resolved.item.pair:
            exact_by_pair.setdefault(resolved.item.pair, []).append(dc.exact)
    pair_family = {r.item.pair: r.item.family for r in items if r.item.pair}
    scores = []
    for family, docs in sorted(by_family.items()):
        pairs = [v for k, v in exact_by_pair.items() if pair_family[k] == family and len(v) > 1]
        scores.append(
            FamilyScore(
                family,
                len(docs),
                summary(docs)["typed_f1"],
                sum(d.exact for d in docs) / len(docs),
                len(pairs),
                sum(all(v) for v in pairs),
            )
        )
    return scores, counts


def render(
    title: str,
    verified: Sequence[FamilyScore],
    drafts: Sequence[FamilyScore],
    context: Mapping[str, str],
) -> str:
    lines = [f"# {title}", "", *(f"- {k}: {v}" for k, v in context.items()), ""]
    for heading, scores in (("Verified items", verified), ("Draft items (unverified)", drafts)):
        lines += [f"## {heading}", ""]
        if not scores:
            lines += ["None.", ""]
            continue
        lines += [
            "| Family | Items | Typed F1 | Exact items | Minimal pairs | Both exact |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for s in scores:
            lines.append(
                f"| {s.family} | {s.items} | {s.typed_f1:.3f} | {s.doc_exact:.1%} | {s.pairs} "
                f"| {s.pairs_both_exact} |"
            )
        lines.append("")
    return "\n".join(lines)


def family_counts(items: Sequence[Resolved]) -> Counter[str]:
    return Counter(f"{r.item.family}/{r.item.status}" for r in items)
