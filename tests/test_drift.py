import pytest

from tests.synthetic import synthetic_id
from triggermap.annotate.drift import compare_mix, render_drift, z_statistic
from triggermap.schema import AdvisoryAnnotation, Category, Condition, DocumentStatus, Role


def _record(index: int, roles: list[Role]) -> AdvisoryAnnotation:
    conditions = tuple(
        Condition(id=f"c{i}", span=(5 + i, 6 + i), category=Category.USAGE, role=role)
        for i, role in enumerate(roles)
    )
    status = DocumentStatus.HAS_CONDITIONS if roles else DocumentStatus.NO_EXPLICIT_CONDITION
    return AdvisoryAnnotation(
        advisory_id=synthetic_id("org", index),
        source_commit="a" * 40,
        content_hash="0" * 64,
        preprocessing_version="test",
        annotation_version="t",
        document_status=status,
        conditions=conditions,
    )


def test_z_statistic() -> None:
    assert z_statistic(0, 0, 5, 10) == 0.0
    assert z_statistic(5, 10, 5, 10) == 0.0
    assert z_statistic(50, 100, 10, 100) == pytest.approx(
        6.172, abs=1e-3
    )  # pooled 0.3, se sqrt(0.21 * 0.02)


def test_large_role_shift_is_flagged_and_small_one_is_not() -> None:
    reference = [_record(i, [Role.REQUIRED] * 4) for i in range(30)]
    shifted = [_record(i, [Role.REQUIRED, Role.UNCERTAIN, Role.UNCERTAIN]) for i in range(30)]
    steady = [_record(i, [Role.REQUIRED] * 4) for i in range(29)] + [_record(99, [])]
    by_label = {(s.group, s.label): s for s in compare_mix(shifted, reference)}
    assert by_label[("Role", "UNCERTAIN")].flagged
    assert by_label[("Role", "REQUIRED")].flagged and by_label[("Role", "REQUIRED")].z < 0
    assert not by_label[("Role", "EXCEPTION")].flagged
    assert not any(s.flagged for s in compare_mix(steady, reference))
    lines = render_drift(compare_mix(shifted, reference), "30 records")
    assert any("UNCERTAIN 0.0% → 66.7%" in line for line in lines)
    assert any("| Role | UNCERTAIN | 60 (66.7%) | 0 (0.0%) |" in line for line in lines)
