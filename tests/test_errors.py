from collections import Counter
from pathlib import Path

from triggermap.eval.errors import SEVERITY, classify, render
from triggermap.schema import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import preprocess

TEXT = (
    "Exposure requires using the admin API and enabling uploads. "
    "It happens even when symlinks are not present. "
    "Attackers can read files. Debug mode must be on. The proxy caches pages."
)
DOC = preprocess(TEXT)


def span(surface: str) -> tuple[int, int]:
    start = DOC.text.index(surface)
    return start, start + len(surface)


def cond(cid: str, surface: str, cat: Category, role: Role) -> Condition:
    return Condition(id=cid, span=span(surface), category=cat, role=role)


def extraction(conditions: tuple[Condition, ...], groups: tuple[Group, ...] = ()) -> Extraction:
    return Extraction(
        content_hash=DOC.content_hash,
        preprocessing_version="1",
        model_id="m",
        document_status=DocumentStatus.HAS_CONDITIONS,
        conditions=conditions,
        groups=groups,
    )


U, C, P, A = Category.USAGE, Category.CONFIGURATION, Category.PLATFORM, Category.ACCESS
REQ, NOT = Role.REQUIRED, Role.NOT_REQUIRED

GOLD = extraction(
    (
        cond("g1", "using the admin API", U, REQ),
        cond("g2", "enabling uploads", U, REQ),
        cond("g3", "symlinks", P, NOT),
        cond("g4", "Debug mode must be on", C, REQ),
        cond("g5", "The proxy caches pages", P, REQ),
    ),
    (Group(operator=GroupOperator.ALL, members=("g1", "g2")),),
)
PRED = extraction(
    (
        cond("p1", "using the admin API", A, REQ),  # category error
        cond("p2", "enabling uploads", U, REQ),  # correct, but grouped ANY
        cond("p3", "symlinks", P, REQ),  # reversed meaning
        cond("p4", "Attackers can read files", A, REQ),  # invented prerequisite
        cond("p5", "Debug mode", C, REQ),  # boundary error
    ),
    (Group(operator=GroupOperator.ANY, members=("p1", "p2")),),
)


def test_every_error_type_is_classified() -> None:
    entries = classify("GHSA-2222-2222-2222", DOC, GOLD, PRED)
    kinds = sorted(e.kind for e in entries)
    assert kinds == sorted(
        [
            "category_error",
            "reversed_meaning",
            "invented_prerequisite",
            "boundary_error",
            "missed_condition",
            "group_error",
        ]
    )
    reversed_ = next(e for e in entries if e.kind == "reversed_meaning")
    assert reversed_.gold == 'PLATFORM/NOT_REQUIRED "symlinks"'
    assert reversed_.predicted == 'PLATFORM/REQUIRED "symlinks"'
    assert "«symlinks»" in reversed_.excerpt
    group = next(e for e in entries if e.kind == "group_error")
    assert (group.gold, group.predicted) == ("ALL of 2", "ANY")


def test_missing_prediction_misses_everything_and_perfect_has_no_errors() -> None:
    missed = classify("x", DOC, GOLD, None)
    assert Counter(e.kind for e in missed) == {"missed_condition": 5, "group_error": 1}
    assert classify("x", DOC, GOLD, GOLD) == []


def Counter_of(entries):  # type: ignore[no-untyped-def]
    from collections import Counter

    return dict(Counter(e.kind for e in entries))


def test_render_orders_by_severity_and_escapes(tmp_path: Path) -> None:
    entries = classify("GHSA-2222-2222-2222", DOC, GOLD, PRED)
    report = render("Errors", entries, 1, {"Split": "dev"})
    positions = [report.index(f"## {kind}") for kind in SEVERITY if f"## {kind}" in report]
    assert positions == sorted(positions)
    assert report.index("## reversed_meaning") < report.index("## invented_prerequisite")
    assert "| reversed_meaning | 1 |" in report
