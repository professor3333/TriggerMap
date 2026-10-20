"""Deterministic validation of annotations and predictions against their text.

Pydantic handles field-level shape; this module checks everything that needs the
whole record or the canonical text: offsets, references, grouping and status.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from triggermap.schema.models import (
    AdvisoryAnnotation,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    ref: str | None = None


def validate_conditions(conditions: tuple[Condition, ...], text: str) -> list[Issue]:
    issues: list[Issue] = []
    for cid, count in Counter(c.id for c in conditions).items():
        if count > 1:
            issues.append(Issue("duplicate_condition_id", f"id used {count} times", cid))

    for cond in conditions:
        start, end = cond.span
        if end > len(text):
            issues.append(
                Issue("span_out_of_bounds", f"{cond.span} exceeds text length {len(text)}", cond.id)
            )
            continue
        surface = text[start:end]
        if surface != surface.strip():
            issues.append(
                Issue("span_whitespace_boundary", f"span {cond.span} = {surface!r}", cond.id)
            )
        # Canonical text keeps one line per paragraph, list item, heading, table row or
        # code line, so a condition span never contains a newline.
        if "\n" in surface:
            issues.append(Issue("span_crosses_line", f"span {cond.span} spans lines", cond.id))

    # BIO tagging cannot represent overlapping spans, so any overlap is invalid.
    furthest: Condition | None = None
    for cur in sorted(conditions, key=lambda c: c.span):
        if furthest is not None and cur.span[0] < furthest.span[1]:
            issues.append(Issue("span_overlap", f"overlaps {furthest.id} {furthest.span}", cur.id))
        if furthest is None or cur.span[1] > furthest.span[1]:
            furthest = cur
    return issues


def validate_groups(groups: tuple[Group, ...], condition_ids: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    seen: dict[str, int] = {}
    for index, group in enumerate(groups):
        ref = f"group[{index}]"
        if len(group.members) < 2:
            issues.append(Issue("group_too_small", "a group needs at least 2 members", ref))
        for member, count in Counter(group.members).items():
            if count > 1:
                issues.append(Issue("group_duplicate_member", f"{member} listed twice", ref))
        for member in dict.fromkeys(group.members):
            if member not in condition_ids:
                issues.append(Issue("group_unknown_member", f"{member} is not a condition", ref))
            elif member in seen:
                issues.append(
                    Issue(
                        "condition_in_multiple_groups",
                        f"{member} already in group[{seen[member]}]",
                        ref,
                    )
                )
            else:
                seen[member] = index
    return issues


def validate_annotation(record: AdvisoryAnnotation | Extraction, text: str) -> list[Issue]:
    """Return every problem with a gold record or a prediction against its canonical `text`.

    An empty list means valid.
    """
    issues = validate_conditions(record.conditions, text)
    issues += validate_groups(record.groups, {c.id for c in record.conditions})

    status = record.document_status
    if status is DocumentStatus.NO_EXPLICIT_CONDITION and (record.conditions or record.groups):
        issues.append(
            Issue("status_mismatch", "NO_EXPLICIT_CONDITION record has conditions or groups")
        )
    if status is DocumentStatus.HAS_CONDITIONS and not record.conditions:
        issues.append(Issue("status_mismatch", "HAS_CONDITIONS record has no conditions"))
    return issues
