"""Document-level counts and the metrics built from them.

Every metric is computed from per-document counts, so the same counts feed point
estimates, cluster bootstrap intervals and paired system comparisons.

Definitions (exact match throughout, offsets in canonical text):
- span: a predicted span equals a gold span.
- typed: span, category and role all match.
- role:<R> / category:<C>: (span, label) tuples restricted to one label; role macro-F1
  averages roles that have gold support.
- group: operator and the set of member spans match.
- document exact: typed conditions and groups match exactly; reported separately for
  documents whose gold has conditions and for those without.
- invented prerequisite: a predicted REQUIRED condition that overlaps no gold condition.
- reversed meaning: a predicted condition whose best-overlapping gold condition has the
  opposite polarity (REQUIRED vs EXCEPTION / NOT_REQUIRED).
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from triggermap.schema.models import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    Role,
)

Labelled = AdvisoryAnnotation | Extraction
Span = tuple[int, int]

POLARITY = {Role.REQUIRED: 1, Role.EXCEPTION: -1, Role.NOT_REQUIRED: -1, Role.UNCERTAIN: 0}


@dataclass
class DocCounts:
    advisory_id: str
    counts: Counter[str] = field(default_factory=Counter)  # "<metric>:tp|fp|fn" -> n
    exact: bool = False
    gold_has_conditions: bool = False
    pred_required: int = 0
    invented_required: int = 0
    overlapping: int = 0
    reversed: int = 0
    matched_spans: int = 0
    category_correct: int = 0
    role_correct: int = 0
    scored: list[tuple[float, bool]] = field(default_factory=list)  # (confidence, typed-correct)


def _add(counts: Counter[str], key: str, gold: set[object], pred: set[object]) -> None:
    counts[f"{key}:tp"] += len(gold & pred)
    counts[f"{key}:fp"] += len(pred - gold)
    counts[f"{key}:fn"] += len(gold - pred)


def _group_signatures(conditions: Sequence[Condition], groups: Sequence[Group]) -> set[object]:
    spans = {c.id: c.span for c in conditions}
    return {
        (g.operator.value, frozenset(spans[m] for m in g.members if m in spans)) for g in groups
    }


def _overlap(a: Span, b: Span) -> int:
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def doc_counts(advisory_id: str, gold: Labelled, pred: Labelled | None) -> DocCounts:
    out = DocCounts(advisory_id)
    gold_conds = list(gold.conditions)
    pred_conds = list(pred.conditions) if pred is not None else []
    pred_groups = list(pred.groups) if pred is not None else []
    out.gold_has_conditions = gold.document_status is not DocumentStatus.NO_EXPLICIT_CONDITION

    def typed(c: Condition) -> tuple[Span, str, str]:
        return c.span, c.category.value, c.role.value

    gold_typed = {typed(c) for c in gold_conds}
    pred_typed = {typed(c) for c in pred_conds}
    _add(out.counts, "span", {c.span for c in gold_conds}, {c.span for c in pred_conds})
    _add(out.counts, "typed", set(gold_typed), set(pred_typed))
    for role in Role:
        _add(
            out.counts,
            f"role:{role.value}",
            {c.span for c in gold_conds if c.role is role},
            {c.span for c in pred_conds if c.role is role},
        )
    for category in Category:
        _add(
            out.counts,
            f"category:{category.value}",
            {c.span for c in gold_conds if c.category is category},
            {c.span for c in pred_conds if c.category is category},
        )
    gold_groups = _group_signatures(gold_conds, gold.groups)
    predicted_groups = _group_signatures(pred_conds, pred_groups)
    _add(out.counts, "group", gold_groups, predicted_groups)
    out.exact = gold_typed == pred_typed and gold_groups == predicted_groups

    gold_by_span = {c.span: c for c in gold_conds}
    for cond in pred_conds:
        out.scored.append(
            (cond.confidence if cond.confidence is not None else 1.0, typed(cond) in gold_typed)
        )
        if cond.span in gold_by_span:
            match = gold_by_span[cond.span]
            out.matched_spans += 1
            out.category_correct += match.category is cond.category
            out.role_correct += match.role is cond.role
        overlaps = [(g, _overlap(g.span, cond.span)) for g in gold_conds]
        best = max(overlaps, key=lambda pair: pair[1], default=None)
        if cond.role is Role.REQUIRED:
            out.pred_required += 1
            if best is None or best[1] == 0:
                out.invented_required += 1
        if best is not None and best[1] > 0:
            out.overlapping += 1
            out.reversed += POLARITY[best[0].role] * POLARITY[cond.role] == -1
    return out


def collect(gold: dict[str, Labelled], pred: dict[str, Extraction]) -> list[DocCounts]:
    """Counts for every gold document; a missing prediction counts as an empty one."""
    return [doc_counts(aid, gold[aid], pred.get(aid)) for aid in sorted(gold)]


# ---------------------------------------------------------------------------
# Aggregation


@dataclass(frozen=True)
class PRF:
    precision: float
    recall: float
    f1: float
    support: int  # gold items


def prf(tp: int, fp: int, fn: int) -> PRF:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return PRF(precision, recall, f1, tp + fn)


def _sum(docs: Iterable[DocCounts]) -> Counter[str]:
    total: Counter[str] = Counter()
    for doc in docs:
        total.update(doc.counts)
    return total


def micro(docs: Sequence[DocCounts], key: str) -> PRF:
    total = _sum(docs)
    return prf(total[f"{key}:tp"], total[f"{key}:fp"], total[f"{key}:fn"])


def macro(docs: Sequence[DocCounts], prefix: str, labels: Iterable[str]) -> float:
    """Macro-F1 over labels with gold support; 0.0 when no label has support."""
    scores = [micro(docs, f"{prefix}:{label}") for label in labels]
    supported = [s.f1 for s in scores if s.support > 0]
    return sum(supported) / len(supported) if supported else 0.0


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def summary(docs: Sequence[DocCounts]) -> dict[str, float]:
    """Headline numbers; every value is a statistic the bootstrap can resample."""
    with_conditions = [d for d in docs if d.gold_has_conditions]
    without_conditions = [d for d in docs if not d.gold_has_conditions]
    return {
        "span_f1": micro(docs, "span").f1,
        "span_precision": micro(docs, "span").precision,
        "span_recall": micro(docs, "span").recall,
        "typed_f1": micro(docs, "typed").f1,
        "role_macro_f1": macro(docs, "role", [r.value for r in Role]),
        "category_macro_f1": macro(docs, "category", [c.value for c in Category]),
        "group_f1": micro(docs, "group").f1,
        "doc_exact_with_conditions": _rate(
            sum(d.exact for d in with_conditions), len(with_conditions)
        ),
        "doc_exact_without_conditions": _rate(
            sum(d.exact for d in without_conditions), len(without_conditions)
        ),
        "false_prerequisite_rate": _rate(
            sum(d.invented_required for d in docs), sum(d.pred_required for d in docs)
        ),
        "reversed_meaning_rate": _rate(
            sum(d.reversed for d in docs), sum(d.overlapping for d in docs)
        ),
        "category_acc_on_matched_spans": _rate(
            sum(d.category_correct for d in docs), sum(d.matched_spans for d in docs)
        ),
        "role_acc_on_matched_spans": _rate(
            sum(d.role_correct for d in docs), sum(d.matched_spans for d in docs)
        ),
    }


@dataclass(frozen=True)
class CoveragePoint:
    threshold: float
    coverage: float  # share of predictions kept
    precision: float  # typed precision of kept predictions
    retained_recall: float  # kept correct / gold typed conditions


def precision_coverage(docs: Sequence[DocCounts], points: int = 10) -> list[CoveragePoint]:
    scored = sorted((s for d in docs for s in d.scored), key=lambda s: -s[0])
    gold_total = sum(d.counts["typed:tp"] + d.counts["typed:fn"] for d in docs)
    if not scored:
        return []
    curve: list[CoveragePoint] = []
    for i in range(1, points + 1):
        keep = max(1, round(len(scored) * i / points))
        kept = scored[:keep]
        correct = sum(ok for _, ok in kept)
        curve.append(
            CoveragePoint(
                threshold=kept[-1][0],
                coverage=keep / len(scored),
                precision=correct / keep,
                retained_recall=_rate(correct, gold_total),
            )
        )
    return curve
