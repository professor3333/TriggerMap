from triggermap.annotate.gate import Plan, gate, render_gate
from triggermap.schema import (
    AdvisoryAnnotation,
    AnnotationOrigin,
    Category,
    Condition,
    DocumentStatus,
    Role,
)

SHA = "0" * 64
COMMIT = "1" * 40


def record(aid: str, roles: list[Role], origin: AnnotationOrigin) -> AdvisoryAnnotation:
    conditions = tuple(
        Condition(id=f"c{i}", span=(i * 2, i * 2 + 1), category=Category.USAGE, role=role)
        for i, role in enumerate(roles, 1)
    )
    status = DocumentStatus.HAS_CONDITIONS if roles else DocumentStatus.NO_EXPLICIT_CONDITION
    return AdvisoryAnnotation(
        advisory_id=aid,
        source_commit=COMMIT,
        content_hash=SHA,
        preprocessing_version="1",
        annotation_version="pilot-1",
        document_status=status,
        conditions=conditions,
        origin=origin,
    )


IDS = ["GHSA-2222-2222-2222", "GHSA-3333-3333-3333", "GHSA-4444-4444-4444"]


def test_test_split_is_never_counted_and_rates_are_projected() -> None:
    records = [
        record(IDS[0], [Role.REQUIRED, Role.EXCEPTION], AnnotationOrigin.MANUAL),
        record(IDS[1], [Role.REQUIRED], AnnotationOrigin.MODEL_DRAFT_ACCEPTED),
        record(IDS[2], [Role.NOT_REQUIRED] * 9, AnnotationOrigin.MANUAL),  # test split
    ]
    strata = {IDS[0]: "random", IDS[1]: "enriched", IDS[2]: "random"}
    assignment = {IDS[0]: "dev", IDS[1]: "train", IDS[2]: "test"}
    plan = Plan(natural=100, enriched=50, evaluation_natural=30, threshold=60)
    rows, sizes = gate(records, strata, assignment, plan)
    assert sizes == {"random": 1, "enriched": 1}
    by_label = {r.label: r for r in rows}
    assert by_label["NOT_REQUIRED"].projected == 0  # only in the test record
    assert by_label["REQUIRED"].projected == 150 and by_label["REQUIRED"].supported
    assert by_label["EXCEPTION"].projected == 100 and by_label["EXCEPTION"].manual == 1
    assert by_label["EXCEPTION"].projected_evaluation == 30
    assert by_label["ANY"].supported is False
    assert by_label["UNSUPPORTED_STRUCTURE"].supported is None  # statuses are not gated
    text = render_gate(rows, sizes, {"manual": 1}, [300.0, 420.0], plan)
    assert "| Role | ANY" not in text and "| Group operator | ANY | 0 | 0 | 0 | 0 | 0 |" in text
    assert "reported, not gated" in text
    assert "**unsupported**" in text and "Median minutes per document: 6.0" in text
