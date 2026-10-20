"""Cluster bootstrap over documents or project groups.

Resampling whole clusters (all advisories of a project group, or single documents)
keeps the dependence between related advisories inside each resample, so intervals are
not falsely narrow.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from triggermap.eval.metrics import DocCounts

Statistic = Callable[[Sequence[DocCounts]], Mapping[str, float]]


@dataclass(frozen=True)
class Interval:
    estimate: float
    low: float
    high: float


def clusters_of(docs: Sequence[DocCounts], cluster_of: Mapping[str, str] | None) -> list[list[int]]:
    """Indices of ``docs`` grouped into clusters; one cluster per document when no mapping."""
    if cluster_of is None:
        return [[i] for i in range(len(docs))]
    grouped: dict[str, list[int]] = {}
    for index, doc in enumerate(docs):
        grouped.setdefault(cluster_of.get(doc.advisory_id, doc.advisory_id), []).append(index)
    return [grouped[key] for key in sorted(grouped)]


def _percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))]


def _resample(
    docs: Sequence[DocCounts], clusters: list[list[int]], rng: random.Random
) -> list[DocCounts]:
    picked = rng.choices(clusters, k=len(clusters))
    return [docs[i] for cluster in picked for i in cluster]


def bootstrap(
    docs: Sequence[DocCounts],
    statistic: Statistic,
    cluster_of: Mapping[str, str] | None = None,
    samples: int = 1000,
    seed: int = 0,
    alpha: float = 0.05,
) -> dict[str, Interval]:
    point = statistic(docs)
    if not docs:
        return {k: Interval(v, v, v) for k, v in point.items()}
    rng = random.Random(seed)
    clusters = clusters_of(docs, cluster_of)
    draws: dict[str, list[float]] = {k: [] for k in point}
    for _ in range(samples):
        stats = statistic(_resample(docs, clusters, rng))
        for key in point:
            draws[key].append(stats[key])
    return {
        key: Interval(
            point[key], _percentile(draws[key], alpha / 2), _percentile(draws[key], 1 - alpha / 2)
        )
        for key in point
    }


@dataclass(frozen=True)
class Comparison:
    difference: float  # system B minus system A
    low: float
    high: float
    p_not_better: float  # share of resamples where B does not beat A


def paired_bootstrap(
    docs_a: Sequence[DocCounts],
    docs_b: Sequence[DocCounts],
    statistic: Statistic,
    cluster_of: Mapping[str, str] | None = None,
    samples: int = 1000,
    seed: int = 0,
    alpha: float = 0.05,
) -> dict[str, Comparison]:
    """Compare two systems on the same documents with identical resamples."""
    if [d.advisory_id for d in docs_a] != [d.advisory_id for d in docs_b]:
        raise ValueError("paired bootstrap needs both systems scored on the same documents")
    point_a, point_b = statistic(docs_a), statistic(docs_b)
    rng = random.Random(seed)
    clusters = clusters_of(docs_a, cluster_of)
    diffs: dict[str, list[float]] = {k: [] for k in point_a}
    for _ in range(samples):
        picked = rng.choices(clusters, k=len(clusters))
        indices = [i for cluster in picked for i in cluster]
        stats_a = statistic([docs_a[i] for i in indices])
        stats_b = statistic([docs_b[i] for i in indices])
        for key in point_a:
            diffs[key].append(stats_b[key] - stats_a[key])
    return {
        key: Comparison(
            point_b[key] - point_a[key],
            _percentile(diffs[key], alpha / 2),
            _percentile(diffs[key], 1 - alpha / 2),
            sum(d <= 0 for d in diffs[key]) / len(diffs[key]) if diffs[key] else 1.0,
        )
        for key in point_a
    }
