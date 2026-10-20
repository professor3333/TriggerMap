"""Meaning-preserving formatting perturbations and prediction consistency.

Each perturbation rewrites the raw advisory Markdown without changing its meaning. A
system is consistent on a document when the perturbed prediction has the same conditions
(normalised surface text, category, role) and the same groups. No labels are needed, so
this measures robustness on any sample of real advisories.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from triggermap.schema.models import Extraction
from triggermap.text.preprocessing import PreprocessedDocument, preprocess

Perturbation = Callable[[str], str]

_FENCE = re.compile(r"^\s*(```|~~~)")
_LIST = re.compile(r"^(\s*)- ")
_IDENTIFIER = re.compile(r"(?<![`\w])([A-Za-z]\w*_\w+)(?![`\w])")


def _outside_code(raw: str, transform: Callable[[str], str]) -> str:
    """Apply ``transform`` to every line outside fenced code blocks and inline code."""
    out = []
    in_fence = False
    for line in raw.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
        elif in_fence or line.startswith("    ") or line.lstrip().startswith("|"):
            out.append(line)
        else:
            parts = re.split(r"(`+[^`]*`+)", line)
            out.append("".join(p if p.startswith("`") else transform(p) for p in parts))
    return "\n".join(out)


def crlf(raw: str) -> str:
    return raw.replace("\r\n", "\n").replace("\n", "\r\n")


def bullet_style(raw: str) -> str:
    out, in_fence = [], False
    for line in raw.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
        out.append(line if in_fence else _LIST.sub(r"\1* ", line))
    return "\n".join(out)


def extra_blank_lines(raw: str) -> str:
    out, in_fence = [], False
    for line in raw.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
        out.append(line)
        if not in_fence and not line.strip():
            out.append("")
    return "\n".join(out)


def rewrap(raw: str, width: int = 60) -> str:
    """Hard-wrap long plain paragraph lines; Markdown joins them back with spaces."""
    out, in_fence = [], False
    for line in raw.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
        plain = line and not re.match(r"\s*([#>|*+-]|\d+[.)]|    )", line)
        if in_fence or not plain or len(line) <= width or "`" in line:
            out.append(line)
            continue
        current = ""
        for word in line.split(" "):
            if current and len(current) + 1 + len(word) > width:
                out.append(current)
                current = word
            else:
                current = f"{current} {word}" if current else word
        out.append(current)
    return "\n".join(out)


def backtick_identifiers(raw: str) -> str:
    return _outside_code(raw, lambda s: _IDENTIFIER.sub(r"`\1`", s))


def double_spaces(raw: str) -> str:
    return _outside_code(raw, lambda s: re.sub(r"(?<=\w) (?=\w)", "  ", s))


def curly_quotes(raw: str) -> str:
    def swap(s: str) -> str:
        s = re.sub(r"(?<=\w)'(?=\w)", "\u2019", s)
        return re.sub(r'"([^"\n]*)"', "\u201c\\1\u201d", s)

    return _outside_code(raw, swap)


PERTURBATIONS: dict[str, Perturbation] = {
    "crlf": crlf,
    "bullet_style": bullet_style,
    "extra_blank_lines": extra_blank_lines,
    "rewrap": rewrap,
    "backtick_identifiers": backtick_identifiers,
    "double_spaces": double_spaces,
    "curly_quotes": curly_quotes,
}


def _norm(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(text.split())


def signature(extraction: Extraction, doc: PreprocessedDocument) -> tuple[object, object]:
    surface = {c.id: _norm(doc.text[c.span[0] : c.span[1]]) for c in extraction.conditions}
    conditions = Counter(
        (surface[c.id], c.category.value, c.role.value) for c in extraction.conditions
    )
    groups = Counter(
        (g.operator.value, tuple(sorted(surface[m] for m in g.members if m in surface)))
        for g in extraction.groups
    )
    return conditions, groups


@dataclass
class PerturbationResult:
    name: str
    documents: int = 0
    changed_input: int = 0  # documents whose raw text the perturbation actually changed
    consistent: int = 0
    examples: list[str] = field(default_factory=list)


def measure(
    extractor: object,
    raws: Mapping[str, str],
    perturbations: Iterable[str] = PERTURBATIONS,
    max_examples: int = 5,
) -> list[PerturbationResult]:
    extract = extractor.extract  # type: ignore[attr-defined]
    baseline = {}
    for aid, raw in raws.items():
        doc = preprocess(raw)
        baseline[aid] = signature(extract(doc, aid), doc)
    results = []
    for name in perturbations:
        result = PerturbationResult(name)
        for aid, raw in raws.items():
            perturbed = PERTURBATIONS[name](raw)
            result.documents += 1
            result.changed_input += perturbed != raw
            doc = preprocess(perturbed)
            if signature(extract(doc, aid), doc) == baseline[aid]:
                result.consistent += 1
            elif len(result.examples) < max_examples:
                result.examples.append(aid)
        results.append(result)
    return results


def render(title: str, results: Sequence[PerturbationResult], context: Mapping[str, str]) -> str:
    total = sum(r.documents for r in results)
    consistent = sum(r.consistent for r in results)
    lines = [
        f"# {title}",
        "",
        *(f"- {k}: {v}" for k, v in context.items()),
        f"- Overall consistency: {consistent / total:.1%} ({consistent:,} of {total:,} "
        "document-perturbation pairs)"
        if total
        else "- No documents",
        "",
        "| Perturbation | Documents | Input changed | Consistent | Rate | Inconsistent examples |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in results:
        rate = r.consistent / r.documents if r.documents else 0.0
        examples = ", ".join(f"`{aid}`" for aid in r.examples) or "none"
        lines.append(
            f"| {r.name} | {r.documents} | {r.changed_input} | {r.consistent} | {rate:.1%} "
            f"| {examples} |"
        )
    lines.append("")
    return "\n".join(lines)
