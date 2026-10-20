from typing import Any

import pytest
from pydantic import ValidationError

from triggermap.schema import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Group,
    GroupOperator,
    Role,
    validate_annotation,
)

SENTENCE = (
    "When using aiohttp as a web server and enabling static resource resolution with "
    "follow_symlinks set to True, it can lead to this vulnerability."
)


def record(**overrides: Any) -> AdvisoryAnnotation:
    base: dict[str, Any] = {
        "advisory_id": "GHSA-5h86-8mv2-jq9f",
        "source_commit": "a" * 40,
        "content_hash": "b" * 64,
        "preprocessing_version": "1",
        "annotation_version": "pilot-1",
        "document_status": DocumentStatus.HAS_CONDITIONS,
        "conditions": (
            Condition(id="c1", span=(5, 34), category=Category.USAGE, role=Role.REQUIRED),
            Condition(id="c2", span=(39, 74), category=Category.USAGE, role=Role.REQUIRED),
            Condition(id="c3", span=(80, 107), category=Category.CONFIGURATION, role=Role.REQUIRED),
        ),
        "groups": (Group(operator=GroupOperator.ALL, members=("c1", "c2", "c3")),),
    }
    base.update(overrides)
    return AdvisoryAnnotation(**base)


def codes(rec: AdvisoryAnnotation, text: str = SENTENCE) -> list[str]:
    return [issue.code for issue in validate_annotation(rec, text)]


def test_reference_example_is_valid() -> None:
    assert codes(record()) == []


def test_round_trips_through_json() -> None:
    rec = record()
    assert AdvisoryAnnotation.model_validate_json(rec.model_dump_json()) == rec


@pytest.mark.parametrize(
    "field, value",
    [
        ("advisory_id", "CVE-2024-23334"),
        ("advisory_id", "GHSA-aaaa-bbbb-cccc"),  # letters outside the GHSA alphabet
        ("source_commit", "abc"),
        ("content_hash", "B" * 64),
        ("document_status", "MAYBE"),
    ],
)
def test_field_shapes_are_enforced(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        record(**{field: value})


@pytest.mark.parametrize("span", [(5, 5), (7, 3), (-1, 4)])
def test_condition_span_must_be_ordered(span: tuple[int, int]) -> None:
    with pytest.raises(ValidationError):
        Condition(id="c1", span=span, category=Category.USAGE, role=Role.REQUIRED)


def test_unknown_labels_are_rejected() -> None:
    with pytest.raises(ValidationError):
        Condition.model_validate(
            {"id": "c1", "span": (0, 1), "category": "VERSION", "role": "REQUIRED"}
        )
    with pytest.raises(ValidationError):
        Condition.model_validate({"id": "c1", "span": (0, 1), "category": "USAGE", "role": "MAY"})


def cond(cid: str, span: tuple[int, int]) -> Condition:
    return Condition(id=cid, span=span, category=Category.USAGE, role=Role.REQUIRED)


@pytest.mark.parametrize(
    "spans, expected",
    [
        ([(0, 6)], ["span_whitespace_boundary"]),  # "alpha "
        ([(6, 13)], ["span_crosses_line"]),
        ([(10, 99)], ["span_out_of_bounds"]),
        ([(0, 5), (3, 8)], ["span_overlap"]),
        ([(0, 10), (1, 3), (6, 8)], ["span_overlap", "span_overlap"]),  # nested in a long span
        ([(0, 5), (6, 10)], []),
    ],
)
def test_span_problems_are_reported(spans: list[tuple[int, int]], expected: list[str]) -> None:
    text = "alpha beta\ngamma"
    conditions = tuple(cond(f"c{i}", span) for i, span in enumerate(spans))
    assert codes(record(conditions=conditions, groups=()), text) == expected


def test_duplicate_condition_ids_are_reported() -> None:
    rec = record(conditions=(cond("c1", (0, 5)), cond("c1", (6, 10))), groups=())
    assert codes(rec, "alpha beta") == ["duplicate_condition_id"]


def test_group_problems_are_reported() -> None:
    rec = record(
        groups=(
            Group(operator=GroupOperator.ALL, members=("c1",)),
            Group(operator=GroupOperator.ANY, members=("c1", "c2", "c2", "c9")),
        )
    )
    assert sorted(codes(rec)) == [
        "condition_in_multiple_groups",
        "group_duplicate_member",
        "group_too_small",
        "group_unknown_member",
    ]


def test_document_status_must_match_conditions() -> None:
    assert codes(record(document_status=DocumentStatus.NO_EXPLICIT_CONDITION)) == [
        "status_mismatch"
    ]
    assert codes(record(conditions=(), groups=())) == ["status_mismatch"]
    assert codes(record(document_status=DocumentStatus.UNSUPPORTED_STRUCTURE)) == []
