"""Error catalogue: every disagreement between gold and prediction, classified.

Error types, most severe first (the project's two worst failures lead):
- reversed_meaning: overlapping spans whose roles have opposite polarity;
- invented_prerequisite: a predicted REQUIRED condition that overlaps no gold condition;
- missed_condition: a gold condition no prediction overlaps;
- boundary_error: overlapping spans of the same polarity that are not identical;
- category_error / role_error: identical span, different category / non-reversing role;
- group_error: a gold group not reproduced (members or operator), or a spurious group;
- spurious_condition: a predicted non-REQUIRED condition that overlaps nothing.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from triggermap.eval.metrics import POLARITY, Labelled
from triggermap.schema.models import Condition, Group
from triggermap.text.preprocessing import PreprocessedDocument

SEVERITY = [
    "reversed_meaning",
    "invented_prerequisite",
    "missed_condition",
    "boundary_error",
    "category_error",
    "role_error",
    "group_error",
    "spurious_condition",
]

REMEDIES = {
    "reversed_meaning": "Add a minimal pair for this cue to the challenge set; check the role rule "
    "(guidelines §5) and add training examples with the opposite polarity.",
    "invented_prerequisite": "Add hard negatives of this kind (impact, mechanism, workaround, "
    "background mention) to training; consider a stricter accept threshold.",
    "missed_condition": "Check whether the wording is covered by any cue or feature; target it "
    "with uncertainty sampling.",
    "boundary_error": "Clarify the span-boundary rule (guidelines §6) with this example; check "
    "tokenisation of the identifiers involved.",
    "category_error": "Add this case to the category tie-breakers (guidelines §4).",
    "role_error": "Add this case to the role table (guidelines §5).",
    "group_error": "Check the lead-in / connective that sets the logic; add list examples.",
    "spurious_condition": "Check why a non-requirement was predicted here; add hard negatives.",
}


@dataclass(frozen=True)
class ErrorEntry:
    advisory_id: str
    kind: str
    excerpt: str
    gold: str
    predicted: str


def _overlap(a: tuple[int, int], b: tuple[int, int]) -> int:
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def _label(text: str, cond: Condition | None) -> str:
    if cond is None:
        return "-"
    surface = " ".join(text[cond.span[0] : cond.span[1]].split())
    return f'{cond.category.value}/{cond.role.value} "{surface}"'


def _excerpt(doc: PreprocessedDocument, spans: Sequence[tuple[int, int]], width: int = 220) -> str:
    start = min(s[0] for s in spans)
    end = max(s[1] for s in spans)
    sentence = next(
        ((s.start, s.end) for s in doc.sentences if s.start <= start < s.end), (start, end)
    )
    lo, hi = min(sentence[0], start), max(sentence[1], end)
    text = doc.text
    marked = text[lo:start] + "«" + text[start:end] + "»" + text[end:hi]
    marked = " ".join(marked.split())
    return marked if len(marked) <= width else marked[: width - 1] + "\u2026"


def _group_key(group: Group, spans: Mapping[str, tuple[int, int]]) -> frozenset[tuple[int, int]]:
    return frozenset(spans[m] for m in group.members if m in spans)


def classify(
    advisory_id: str, doc: PreprocessedDocument, gold: Labelled, pred: Labelled | None
) -> list[ErrorEntry]:
    text = doc.text
    gold_conds = list(gold.conditions)
    pred_conds = list(pred.conditions) if pred is not None else []
    out: list[ErrorEntry] = []

    def add(
        kind: str, spans: Sequence[tuple[int, int]], g: Condition | None, p: Condition | None
    ) -> None:
        out.append(
            ErrorEntry(advisory_id, kind, _excerpt(doc, spans), _label(text, g), _label(text, p))
        )

    for p in pred_conds:
        overlaps = sorted(gold_conds, key=lambda g: -_overlap(g.span, p.span))
        best = overlaps[0] if overlaps and _overlap(overlaps[0].span, p.span) > 0 else None
        if best is None:
            kind = "invented_prerequisite" if p.role.value == "REQUIRED" else "spurious_condition"
            add(kind, [p.span], None, p)
            continue
        reversed_ = POLARITY[best.role] * POLARITY[p.role] == -1
        if reversed_:
            add("reversed_meaning", [best.span, p.span], best, p)
        elif best.span != p.span:
            add("boundary_error", [best.span, p.span], best, p)
        else:
            if best.category is not p.category:
                add("category_error", [p.span], best, p)
            if best.role is not p.role:
                add("role_error", [p.span], best, p)
    for g in gold_conds:
        if not any(_overlap(g.span, p.span) for p in pred_conds):
            add("missed_condition", [g.span], g, None)

    gold_spans = {c.id: c.span for c in gold_conds}
    pred_spans = {c.id: c.span for c in pred_conds}
    pred_groups = {_group_key(g, pred_spans): g for g in (pred.groups if pred is not None else ())}
    gold_groups = {_group_key(g, gold_spans): g for g in gold.groups}
    for key, group in gold_groups.items():
        match = pred_groups.get(key)
        if key and (match is None or match.operator is not group.operator):
            found = match.operator.value if match else "no group"
            out.append(
                ErrorEntry(
                    advisory_id,
                    "group_error",
                    _excerpt(doc, sorted(key)) if key else "",
                    f"{group.operator.value} of {len(key)}",
                    found,
                )
            )
    for key, group in pred_groups.items():
        if key and key not in gold_groups:
            out.append(
                ErrorEntry(
                    advisory_id,
                    "group_error",
                    _excerpt(doc, sorted(key)),
                    "no group",
                    f"{group.operator.value} of {len(key)}",
                )
            )
    return out


def render(
    title: str,
    entries: Sequence[ErrorEntry],
    documents: int,
    context: Mapping[str, str],
    per_kind: int = 15,
) -> str:
    counts = Counter(e.kind for e in entries)
    lines = [
        f"# {title}",
        "",
        *(f"- {k}: {v}" for k, v in context.items()),
        f"- Documents: {documents}; disagreements: {len(entries)}",
        "",
        "Spans are marked «like this» in their sentence. Excerpts are advisory text from the "
        "GitHub Advisory Database (CC BY 4.0).",
        "",
        "| Error type | Count | Proposed remedy |",
        "|---|---:|---|",
    ]
    lines += [f"| {kind} | {counts.get(kind, 0)} | {REMEDIES[kind]} |" for kind in SEVERITY]
    for kind in SEVERITY:
        examples = [e for e in entries if e.kind == kind]
        if not examples:
            continue
        lines += [
            "",
            f"## {kind} ({len(examples)})",
            "",
            "| Advisory | Excerpt | Gold | Predicted |",
        ]
        lines.append("|---|---|---|---|")
        for e in examples[:per_kind]:
            cells = [e.excerpt, e.gold, e.predicted]
            safe = [c.replace("|", "\\|") for c in cells]
            lines.append(f"| {e.advisory_id} | " + " | ".join(safe) + " |")
        if len(examples) > per_kind:
            lines.append(f"| \u2026 | {len(examples) - per_kind} more | | |")
    lines.append("")
    return "\n".join(lines)
