"""Scoring against two references for the same documents (for example two model drafts).

When the reference labels are themselves unstable, one reference can make a system look
better or worse than another one would. Scoring against both shows whether a conclusion
depends on the choice of reference:

- typed / span F1 against each reference separately;
- consensus recall: typed recall on the conditions both references mark identically
  (span, category and role);
- support: the share of a system's typed predictions that both references, or at least
  one, contain;
- invented prerequisites against the union: predicted REQUIRED conditions that overlap no
  condition in either reference.

Exact matching throughout, as in :mod:`triggermap.eval.metrics`. Scores against model drafts
measure agreement with those drafts, not accuracy.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from triggermap.eval.bootstrap import Comparison, Interval, bootstrap, paired_bootstrap
from triggermap.eval.metrics import DocCounts, Labelled, _add, _overlap, _sum, prf
from triggermap.schema.models import Condition, Extraction, Role

METRICS: tuple[tuple[str, str], ...] = (
    ("typed_f1_a", "Typed F1 vs reference A"),
    ("typed_f1_b", "Typed F1 vs reference B"),
    ("span_f1_a", "Span F1 vs reference A"),
    ("span_f1_b", "Span F1 vs reference B"),
    ("consensus_recall", "Recall on consensus conditions"),
    ("supported_both", "Predictions in both references"),
    ("supported_either", "Predictions in at least one reference"),
    ("invented_a", "Invented prerequisites vs A (lower is better)"),
    ("invented_b", "Invented prerequisites vs B (lower is better)"),
    ("invented_union", "Invented prerequisites vs both (lower is better)"),
)
LOWER_IS_BETTER = frozenset({"invented_a", "invented_b", "invented_union"})


def _typed(conditions: Sequence[Condition]) -> set[object]:
    return {(c.span, c.category.value, c.role.value) for c in conditions}


def _touches(span: tuple[int, int], others: Sequence[Condition]) -> bool:
    return any(_overlap(span, o.span) > 0 for o in others)


def two_reference_counts(
    advisory_id: str, ref_a: Labelled, ref_b: Labelled, pred: Labelled | None
) -> DocCounts:
    """Per-document counts for one system against two references."""
    out = DocCounts(advisory_id)
    conds_a, conds_b = list(ref_a.conditions), list(ref_b.conditions)
    pred_conds = list(pred.conditions) if pred is not None else []
    typed_a, typed_b, typed_p = _typed(conds_a), _typed(conds_b), _typed(pred_conds)
    _add(out.counts, "a", typed_a, typed_p)
    _add(out.counts, "b", typed_b, typed_p)
    _add(out.counts, "span_a", {c.span for c in conds_a}, {c.span for c in pred_conds})
    _add(out.counts, "span_b", {c.span for c in conds_b}, {c.span for c in pred_conds})
    _add(out.counts, "consensus", typed_a & typed_b, typed_p)
    out.counts["pred"] += len(typed_p)
    out.counts["pred_both"] += len(typed_p & typed_a & typed_b)
    out.counts["pred_either"] += len(typed_p & (typed_a | typed_b))
    for cond in pred_conds:
        if cond.role is not Role.REQUIRED:
            continue
        out.counts["required"] += 1
        in_a, in_b = _touches(cond.span, conds_a), _touches(cond.span, conds_b)
        out.counts["invented_a"] += not in_a
        out.counts["invented_b"] += not in_b
        out.counts["invented_union"] += not (in_a or in_b)
    out.gold_has_conditions = bool(conds_a or conds_b)
    return out


def collect_two(
    ref_a: Mapping[str, Labelled], ref_b: Mapping[str, Labelled], pred: Mapping[str, Extraction]
) -> list[DocCounts]:
    """Counts for every document both references cover; a missing prediction is empty."""
    if set(ref_a) != set(ref_b):
        raise ValueError("both references must cover the same documents")
    for aid in ref_a:
        if ref_a[aid].content_hash != ref_b[aid].content_hash:
            raise ValueError(f"{aid}: the two references label different texts")
        p = pred.get(aid)
        if p is not None and p.content_hash != ref_a[aid].content_hash:
            raise ValueError(f"{aid}: prediction was made on a different text")
    return [
        two_reference_counts(aid, ref_a[aid], ref_b[aid], pred.get(aid)) for aid in sorted(ref_a)
    ]


def consensus_size(ref_a: Mapping[str, Labelled], ref_b: Mapping[str, Labelled]) -> int:
    """Conditions that both references mark identically (span, category and role)."""
    return sum(
        len(_typed(ref_a[aid].conditions) & _typed(ref_b[aid].conditions))
        for aid in ref_a
        if aid in ref_b
    )


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def two_reference_summary(docs: Sequence[DocCounts]) -> dict[str, float]:
    total = _sum(docs)

    def f1(key: str) -> float:
        return prf(total[f"{key}:tp"], total[f"{key}:fp"], total[f"{key}:fn"]).f1

    return {
        "typed_f1_a": f1("a"),
        "typed_f1_b": f1("b"),
        "span_f1_a": f1("span_a"),
        "span_f1_b": f1("span_b"),
        "consensus_recall": _rate(
            total["consensus:tp"], total["consensus:tp"] + total["consensus:fn"]
        ),
        "supported_both": _rate(total["pred_both"], total["pred"]),
        "supported_either": _rate(total["pred_either"], total["pred"]),
        "invented_a": _rate(total["invented_a"], total["required"]),
        "invented_b": _rate(total["invented_b"], total["required"]),
        "invented_union": _rate(total["invented_union"], total["required"]),
    }


def score(
    docs: Sequence[DocCounts], cluster_of: Mapping[str, str] | None, samples: int, seed: int
) -> dict[str, Interval]:
    return bootstrap(docs, two_reference_summary, cluster_of, samples, seed)


def compare(
    docs_a: Sequence[DocCounts],
    docs_b: Sequence[DocCounts],
    cluster_of: Mapping[str, str] | None,
    samples: int,
    seed: int,
) -> dict[str, Comparison]:
    return paired_bootstrap(docs_a, docs_b, two_reference_summary, cluster_of, samples, seed)


def verdict(key: str, comparison: Comparison) -> str:
    """'better' / 'worse' when the whole 95% interval is on one side of zero, else 'unclear'."""
    above, below = comparison.low > 0, comparison.high < 0
    if key in LOWER_IS_BETTER:
        above, below = below, above
    return "better" if above else "worse" if below else "unclear"


def render(
    title: str,
    context: Mapping[str, str],
    systems: Sequence[str],
    intervals: Mapping[str, Mapping[str, Interval]],
    comparisons: Mapping[str, Mapping[str, Comparison]],
    totals: Mapping[str, int],
) -> str:
    """Per-system scores, then each system's paired difference from the first one."""
    lines = [f"# {title}", "", *(f"- {key}: {value}" for key, value in context.items())]
    lines += [f"- {key}: {value}" for key, value in totals.items()]
    lines += [
        "",
        "Scores against model drafts measure agreement with the drafts, not accuracy. 95% "
        "bootstrap intervals.",
        "",
        "## Scores",
        "",
        "| Metric | " + " | ".join(f"`{s}`" for s in systems) + " |",
        "|---|" + "---:|" * len(systems),
    ]
    for key, label in METRICS:
        cells = [
            f"{i.estimate:.3f} [{i.low:.3f}, {i.high:.3f}]"
            for i in (intervals[s][key] for s in systems)
        ]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    baseline = systems[0]
    for system in systems[1:]:
        lines += [
            "",
            f"## `{system}` minus `{baseline}` (paired)",
            "",
            "*Better* / *worse* means the whole 95% interval lies on one side of zero.",
            "",
            "| Metric | Difference | 95% CI | Verdict |",
            "|---|---:|:---:|---|",
        ]
        for key, label in METRICS:
            c = comparisons[system][key]
            lines.append(
                f"| {label} | {c.difference:+.3f} | [{c.low:+.3f}, {c.high:+.3f}] "
                f"| {verdict(key, c)} |"
            )
        for pair in (("typed_f1_a", "typed_f1_b"), ("span_f1_a", "span_f1_b")):
            found = [verdict(k, comparisons[system][k]) for k in pair]
            signs = {comparisons[system][k].difference > 0 for k in pair}
            name = "Typed" if pair[0].startswith("typed") else "Span"
            if len(signs) > 1:
                note = "the direction differs between the references"
            elif found[0] == found[1] != "unclear":
                note = f"clearly {found[0]} under both references"
            else:
                note = "same direction under both references; " + (
                    "clear under one only"
                    if "unclear" in found and set(found) != {"unclear"}
                    else "clear under neither"
                )
            lines.append(f"\n{name} F1: {note}.")
    lines.append("")
    return "\n".join(lines)
