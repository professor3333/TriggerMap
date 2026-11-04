"""Label-mix drift: does a newly imported batch label differently from earlier gold?

A shift is not an error by itself (batches are sampled differently), but a large one is a
reason to look before training on the batch. Each label's share is compared within its own
unit (roles among conditions, operators among groups, statuses among documents) with a
pooled two-proportion z statistic. A label is **flagged** when ``|z|`` reaches the threshold
*and* the shares differ by at least ``min_points`` (absolute), so that tiny but "significant"
differences on large samples are not flagged.

Conditions and groups cluster within documents, so the z statistic treats them as more
independent than they are and overstates certainty. It is a screening signal, not a test.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from triggermap.schema.models import AdvisoryAnnotation, DocumentStatus, GroupOperator, Role

Z_THRESHOLD = 3.0
MIN_POINTS = 0.05


@dataclass(frozen=True)
class Shift:
    group: str
    label: str
    batch: int
    batch_total: int
    reference: int
    reference_total: int
    z: float
    flagged: bool

    @property
    def batch_share(self) -> float:
        return self.batch / self.batch_total if self.batch_total else 0.0

    @property
    def reference_share(self) -> float:
        return self.reference / self.reference_total if self.reference_total else 0.0


def _mix(records: Sequence[AdvisoryAnnotation]) -> dict[str, Counter[str]]:
    return {
        "Role": Counter(c.role.value for r in records for c in r.conditions),
        "Group operator": Counter(g.operator.value for r in records for g in r.groups),
        "Document status": Counter(r.document_status.value for r in records),
    }


_LABELS = {
    "Role": [r.value for r in Role],
    "Group operator": [o.value for o in GroupOperator],
    "Document status": [s.value for s in DocumentStatus],
}


def z_statistic(a: int, n_a: int, b: int, n_b: int) -> float:
    """Pooled two-proportion z of a/n_a against b/n_b (0 when undefined)."""
    if not n_a or not n_b:
        return 0.0
    pooled = (a + b) / (n_a + n_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    return (a / n_a - b / n_b) / se if se else 0.0


def compare_mix(
    batch: Sequence[AdvisoryAnnotation],
    reference: Sequence[AdvisoryAnnotation],
    z_threshold: float = Z_THRESHOLD,
    min_points: float = MIN_POINTS,
) -> list[Shift]:
    mix_b, mix_r = _mix(batch), _mix(reference)
    shifts = []
    for group, labels in _LABELS.items():
        n_b, n_r = sum(mix_b[group].values()), sum(mix_r[group].values())
        for label in labels:
            b, r = mix_b[group][label], mix_r[group][label]
            z = z_statistic(b, n_b, r, n_r)
            share_gap = abs((b / n_b if n_b else 0.0) - (r / n_r if n_r else 0.0))
            flagged = abs(z) >= z_threshold and share_gap >= min_points
            shifts.append(Shift(group, label, b, n_b, r, n_r, z, flagged))
    return shifts


def render_drift(shifts: Sequence[Shift], reference_note: str) -> list[str]:
    lines = [
        "## Label mix against earlier gold",
        "",
        f"- Reference: {reference_note}",
        f"- Flagged: |z| ≥ {Z_THRESHOLD:g} and a share gap of at least "
        f"{MIN_POINTS * 100:.0f} points. A flag is a reason to look, not an error. Conditions "
        "cluster within documents, so z overstates certainty: treat it as a screen, not a test.",
        "",
        "| Group | Label | This batch | Reference | z | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for s in shifts:
        status = "**shift**" if s.flagged else ""
        lines.append(
            f"| {s.group} | {s.label} | {s.batch} ({s.batch_share:.1%}) "
            f"| {s.reference} ({s.reference_share:.1%}) | {s.z:+.1f} | {status} |"
        )
    flagged = [s for s in shifts if s.flagged]
    lines.append("")
    if flagged:
        lines.append(
            "Shifted: "
            + ", ".join(f"{s.label} {s.reference_share:.1%} → {s.batch_share:.1%}" for s in flagged)
            + ". Check a sample of these labels against the guidelines before training on "
            "this batch."
        )
        lines.append("")
    return lines
