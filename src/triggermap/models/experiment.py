"""Experiment runner: variants x grid -> trained bundles, dev evaluations and one report.

A config file has a ``[train]`` table (a TrainConfig), an optional ``[grid]`` of lists
(Cartesian product, typically seeds and learning rates) and optional ``[[runs]]`` variants
that override single settings (ablations, learning-curve budgets). Every run is evaluated
on the dev split only, with leakage-group bootstrap intervals.
"""

from __future__ import annotations

import itertools
import statistics
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from triggermap.eval.bootstrap import Interval, bootstrap
from triggermap.eval.metrics import collect, summary


@dataclass(frozen=True)
class PlannedRun:
    name: str
    settings: dict[str, Any]


def plan(config: Mapping[str, Any]) -> list[PlannedRun]:
    base = dict(config["train"])
    variants = config.get("runs") or [{"name": "base"}]
    grid = config.get("grid", {})
    keys = sorted(grid)
    runs = []
    for variant in variants:
        overrides = {k: v for k, v in variant.items() if k != "name"}
        for values in itertools.product(*(grid[k] for k in keys)) if keys else [()]:
            combo = dict(zip(keys, values, strict=True))
            suffix = "-".join(f"{k}{v}" for k, v in combo.items())
            name = "-".join(part for part in (base["model_id"], variant["name"], suffix) if part)
            settings = {**base, **overrides, **combo, "model_id": name}
            runs.append(PlannedRun(name, settings))
    return runs


@dataclass(frozen=True)
class RunResult:
    run: PlannedRun
    intervals: dict[str, Interval]
    metadata: dict[str, Any]


def evaluate_run(
    extractor: Any,
    dev: Sequence[tuple[Any, Any]],
    cluster_of: Mapping[str, str] | None,
    samples: int = 1000,
) -> dict[str, Interval]:
    gold = {record.advisory_id: record for _, record in dev}
    preds = {record.advisory_id: extractor.extract(doc, record.advisory_id) for doc, record in dev}
    return bootstrap(collect(gold, preds), summary, cluster_of, samples)


COLUMNS = [
    ("typed_f1", "Typed F1"),
    ("span_f1", "Span F1"),
    ("role_macro_f1", "Role macro-F1"),
    ("group_f1", "Group F1"),
    ("false_prerequisite_rate", "False prereq."),
]


def render_report(title: str, results: Sequence[RunResult], context: Mapping[str, str]) -> str:
    lines = [f"# {title}", "", *(f"- {k}: {v}" for k, v in context.items()), ""]
    lines += [
        "## Runs (dev split, 95% leakage-group bootstrap intervals)",
        "",
        "| Run | Docs | " + " | ".join(label for _, label in COLUMNS) + " | Best epoch | Seconds |",
        "|---|---:|" + "---:|" * len(COLUMNS) + "---:|---:|",
    ]
    for result in results:
        cells = []
        for key, _ in COLUMNS:
            iv = result.intervals.get(key)
            cells.append(f"{iv.estimate:.3f} [{iv.low:.3f}, {iv.high:.3f}]" if iv else "n/a")
        meta = result.metadata
        lines.append(
            f"| {result.run.name} | {meta['training_documents']} | "
            + " | ".join(cells)
            + f" | {meta.get('best_epoch')} | {meta.get('train_seconds')} |"
        )
    groups: dict[str, list[float]] = {}
    for result in results:
        key = result.run.name.rsplit("-seed", 1)[0]
        if "typed_f1" in result.intervals:
            groups.setdefault(key, []).append(result.intervals["typed_f1"].estimate)
    if any(len(v) > 1 for v in groups.values()):
        lines += ["", "## Across seeds (typed F1)", "", "| Variant | Seeds | Mean | SD |"]
        lines.append("|---|---:|---:|---:|")
        for key, values in groups.items():
            sd = statistics.stdev(values) if len(values) > 1 else 0.0
            lines.append(f"| {key} | {len(values)} | {statistics.mean(values):.3f} | {sd:.3f} |")
    lines.append("")
    return "\n".join(lines)
