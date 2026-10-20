"""Markdown evaluation reports: every number with its support or interval."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from triggermap.eval.bootstrap import Interval
from triggermap.eval.metrics import DocCounts, micro, precision_coverage
from triggermap.schema.models import Category, Role

HEADLINE = [
    ("typed_f1", "Typed condition micro-F1 (span + category + role)"),
    ("span_f1", "Exact span F1"),
    ("span_precision", "Exact span precision"),
    ("span_recall", "Exact span recall"),
    ("role_macro_f1", "Role macro-F1 (roles with gold support)"),
    ("category_macro_f1", "Category macro-F1"),
    ("group_f1", "Group exact-match F1"),
    ("doc_exact_with_conditions", "Complete-document exact match, documents with conditions"),
    ("doc_exact_without_conditions", "Complete-document exact match, documents without conditions"),
    ("false_prerequisite_rate", "False prerequisite rate (lower is better)"),
    ("reversed_meaning_rate", "Reversed meaning rate (lower is better)"),
    ("category_acc_on_matched_spans", "Category accuracy on exactly matched spans"),
    ("role_acc_on_matched_spans", "Role accuracy on exactly matched spans"),
]


def render(
    title: str,
    docs: Sequence[DocCounts],
    intervals: Mapping[str, Interval],
    context: Mapping[str, str],
) -> str:
    with_conditions = sum(d.gold_has_conditions for d in docs)
    lines = [
        f"# {title}",
        "",
        *(f"- {key}: {value}" for key, value in context.items()),
        f"- Documents: {len(docs)} ({with_conditions} with gold conditions, "
        f"{len(docs) - with_conditions} without)",
        "",
        "## Headline metrics (95% bootstrap intervals)",
        "",
        "| Metric | Estimate | 95% CI |",
        "|---|---:|:---:|",
    ]
    for key, label in HEADLINE:
        if key in intervals:
            iv = intervals[key]
            lines.append(f"| {label} | {iv.estimate:.3f} | [{iv.low:.3f}, {iv.high:.3f}] |")

    for title_, prefix, labels in (
        ("Per-role results (exact span + role)", "role", [r.value for r in Role]),
        ("Per-category results (exact span + category)", "category", [c.value for c in Category]),
    ):
        lines += ["", f"## {title_}", "", "| Label | Precision | Recall | F1 | Gold support |"]
        lines.append("|---|---:|---:|---:|---:|")
        for label in labels:
            score = micro(docs, f"{prefix}:{label}")
            lines.append(
                f"| {label} | {score.precision:.3f} | {score.recall:.3f} | {score.f1:.3f} "
                f"| {score.support} |"
            )

    curve = precision_coverage(docs)
    if curve:
        lines += [
            "",
            "## Precision versus coverage",
            "",
            "| Coverage | Confidence ≥ | Typed precision | Retained recall |",
            "|---:|---:|---:|---:|",
        ]
        lines += [
            f"| {p.coverage:.0%} | {p.threshold:.3f} | {p.precision:.3f} "
            f"| {p.retained_recall:.3f} |"
            for p in curve
        ]
    lines.append("")
    return "\n".join(lines)
