"""Confidence calibration and abstention thresholds.

Raw confidences (rules: fixed per rule; CRF/transformer: span marginal x role probability)
are mapped to the probability that a predicted condition is correct (exact span, category
and role). Calibration and threshold choice use a held-out *calibration* half of the dev
split, chosen by leakage group; the other half checks the result out of sample.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np

from triggermap.schema.models import DocumentStatus, Extraction

Method = Literal["identity", "platt", "isotonic"]
Scored = tuple[float, bool]  # (confidence, typed-correct)


@dataclass(frozen=True)
class Calibrator:
    method: Method
    params: dict[str, Any]

    def __call__(self, confidence: float) -> float:
        if self.method == "identity":
            return confidence
        if self.method == "platt":
            z = self.params["a"] * _logit(confidence) + self.params["b"]
            return 0.5 * (1 + math.tanh(z / 2))  # sigmoid without overflow
        xs, ys = self.params["x"], self.params["y"]
        return float(np.interp(confidence, xs, ys))

    def to_dict(self) -> dict[str, Any]:
        return {"method": self.method, **self.params}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Calibrator:
        params = {k: v for k, v in data.items() if k != "method"}
        return cls(data["method"], params)


def _logit(p: float, eps: float = 1e-4) -> float:
    p = min(max(p, eps), 1 - eps)
    return math.log(p / (1 - p))


def fit_platt(scored: Sequence[Scored], l2: float = 1e-3, iterations: int = 100) -> Calibrator:
    """Logistic regression on logit(confidence), fitted with damped Newton steps.

    Full Newton steps can overshoot from the starting point and diverge (seen on transformer
    confidences), so each step is halved until the penalised log-loss decreases.
    """
    if not scored:
        return Calibrator("identity", {})
    x = np.array([_logit(p) for p, _ in scored])
    y = np.array([1.0 if ok else 0.0 for _, ok in scored])

    def loss(a: float, b: float) -> float:
        z = a * x + b
        return float(np.sum(np.logaddexp(0.0, z) - y * z) + 0.5 * l2 * a * a)

    a, b = 1.0, 0.0
    current = loss(a, b)
    for _ in range(iterations):
        p = 0.5 * (1 + np.tanh((a * x + b) / 2))
        w = p * (1 - p)
        grad = np.array([np.sum((p - y) * x) + l2 * a, np.sum(p - y)])
        hess = np.array(
            [[np.sum(w * x * x) + l2, np.sum(w * x)], [np.sum(w * x), np.sum(w) + 1e-9]]
        )
        step = np.linalg.solve(hess, grad)
        t = 1.0
        while t > 1e-10 and loss(a - t * step[0], b - t * step[1]) > current:
            t /= 2
        a, b = a - t * step[0], b - t * step[1]
        current = loss(a, b)
        if np.max(np.abs(t * step)) < 1e-8:
            break
    return Calibrator("platt", {"a": round(float(a), 6), "b": round(float(b), 6)})


def fit_isotonic(scored: Sequence[Scored]) -> Calibrator:
    """Pool-adjacent-violators: a non-decreasing step map from confidence to accuracy."""
    if not scored:
        return Calibrator("identity", {})
    ordered = sorted(scored, key=lambda s: s[0])
    blocks: list[list[float]] = []  # [sum_y, count, max_x]
    for p, ok in ordered:
        blocks.append([1.0 if ok else 0.0, 1.0, p])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            y, n, x = blocks.pop()
            blocks[-1][0] += y
            blocks[-1][1] += n
            blocks[-1][2] = x
    xs = [round(b[2], 6) for b in blocks]
    ys = [round(b[0] / b[1], 6) for b in blocks]
    return Calibrator("isotonic", {"x": xs, "y": ys})


def fit(method: Method, scored: Sequence[Scored]) -> Calibrator:
    if method == "platt":
        return fit_platt(scored)
    if method == "isotonic":
        return fit_isotonic(scored)
    return Calibrator("identity", {})


@dataclass(frozen=True)
class ReliabilityBin:
    mean_confidence: float
    accuracy: float
    count: int


def reliability(scored: Sequence[Scored], bins: int = 10) -> list[ReliabilityBin]:
    """Equal-mass bins (robust when confidences cluster, as fixed rule scores do)."""
    ordered = sorted(scored, key=lambda s: s[0])
    if not ordered:
        return []
    out = []
    for i in range(bins):
        chunk = ordered[i * len(ordered) // bins : (i + 1) * len(ordered) // bins]
        if chunk:
            out.append(
                ReliabilityBin(
                    sum(p for p, _ in chunk) / len(chunk),
                    sum(ok for _, ok in chunk) / len(chunk),
                    len(chunk),
                )
            )
    return out


def expected_calibration_error(scored: Sequence[Scored], bins: int = 10) -> float:
    total = len(scored)
    if not total:
        return 0.0
    return sum(
        b.count / total * abs(b.mean_confidence - b.accuracy) for b in reliability(scored, bins)
    )


@dataclass(frozen=True)
class Threshold:
    threshold: float
    coverage: float
    precision: float
    retained_recall: float
    kept: int


def choose_threshold(
    scored: Sequence[Scored], gold_total: int, target_precision: float
) -> Threshold | None:
    """The lowest threshold (largest coverage) whose kept predictions meet the target."""
    if not scored:
        return None
    ordered = sorted(scored, key=lambda s: -s[0])
    best: Threshold | None = None
    correct = 0
    for i, (p, ok) in enumerate(ordered, start=1):
        correct += ok
        last_of_tie = i == len(ordered) or ordered[i][0] < p
        if not last_of_tie:
            continue
        precision = correct / i
        if precision >= target_precision:
            best = Threshold(
                p, i / len(ordered), precision, correct / gold_total if gold_total else 0.0, i
            )
    return best


def precision_interval(
    per_doc: Mapping[str, Sequence[Scored]],
    threshold: float,
    cluster_of: Mapping[str, str] | None = None,
    samples: int = 1000,
    seed: int = 0,
) -> tuple[float, float]:
    """95% cluster-bootstrap interval of precision among predictions kept at ``threshold``."""
    clusters: dict[str, list[str]] = {}
    for aid in sorted(per_doc):
        clusters.setdefault((cluster_of or {}).get(aid, aid), []).append(aid)
    keys = sorted(clusters)
    rng = random.Random(seed)
    values = []
    for _ in range(samples):
        kept = correct = 0
        for key in rng.choices(keys, k=len(keys)):
            for aid in clusters[key]:
                for p, ok in per_doc[aid]:
                    if p >= threshold:
                        kept += 1
                        correct += ok
        if kept:
            values.append(correct / kept)
    if not values:
        return (0.0, 0.0)
    values.sort()
    return values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]


def calibration_split(
    doc_ids: Sequence[str], group_of: Mapping[str, str], fraction: float = 0.5, seed: int = 0
) -> tuple[list[str], list[str]]:
    """Split dev documents by leakage group into (calibration, held-out evaluation)."""
    groups = sorted({group_of.get(aid, aid) for aid in doc_ids})
    rng = random.Random(seed)
    rng.shuffle(groups)
    chosen = set(groups[: round(len(groups) * fraction)])
    calibration = [aid for aid in doc_ids if group_of.get(aid, aid) in chosen]
    held_out = [aid for aid in doc_ids if group_of.get(aid, aid) not in chosen]
    return calibration, held_out


def keep_confident(extraction: Extraction, threshold: float) -> Extraction:
    """The predictions a reviewer sees without a low-confidence flag at ``threshold``.

    Conditions below the threshold are dropped (a condition without a confidence is kept);
    groups keep their remaining members and disappear below two. A document left with no
    condition becomes ``NO_EXPLICIT_CONDITION``: the model found none above the threshold.
    """
    kept = tuple(
        c for c in extraction.conditions if c.confidence is None or c.confidence >= threshold
    )
    ids = {c.id for c in kept}
    groups = []
    for group in extraction.groups:
        members = tuple(m for m in group.members if m in ids)
        if len(members) >= 2:
            groups.append(group.model_copy(update={"members": members}))
    status = extraction.document_status
    if status is DocumentStatus.HAS_CONDITIONS and not kept:
        status = DocumentStatus.NO_EXPLICIT_CONDITION
    return extraction.model_copy(
        update={"conditions": kept, "groups": tuple(groups), "document_status": status}
    )
