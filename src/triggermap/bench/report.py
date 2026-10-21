"""Run benchmark configurations in fresh processes and render the Markdown report."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from triggermap.bench.worker import BenchConfig

# Engineering targets from the plan, for the documented 2 vCPU / 4 GB x86-64 host.
TARGETS = {"p95_512_s": 2.5, "p95_2000_s": 8.0, "peak_rss_mb": 3072, "docs_per_s": 0.25}


def run_configs(
    configs: Sequence[BenchConfig],
    workload: Path,
    processed: Path,
    repeats: int,
    checkpoint: Path | None = None,
) -> list[dict[str, Any]]:
    """Run each configuration in a fresh process.

    With ``checkpoint``, every finished result is appended immediately and configurations
    already recorded there are skipped, so an interrupted run resumes without losing work.
    """
    done: dict[str, dict[str, Any]] = {}
    if checkpoint is not None and checkpoint.exists():
        for line in checkpoint.read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                done[record["config"]["name"]] = record
    results = []
    for config in configs:
        if config.name in done:
            print(f"  {config.name}: reused from checkpoint", file=sys.stderr)
            results.append(done[config.name])
            continue
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "triggermap.bench.worker",
                json.dumps(asdict(config)),
                str(workload),
                str(processed),
                str(repeats),
            ],
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            tail = completed.stderr.strip().splitlines()[-3:]
            raise RuntimeError(f"{config.name} failed: {' | '.join(tail)}")
        record = json.loads(completed.stdout.strip().splitlines()[-1])
        if checkpoint is not None:
            with checkpoint.open("a") as fh:
                fh.write(json.dumps(record) + "\n")
        results.append(record)
        print(f"  {config.name}: done", file=sys.stderr)
    return results


def _verdict(value: float | None, target: float, higher_is_better: bool, on_target: bool) -> str:
    if value is None:
        return "n/a"
    met = value >= target if higher_is_better else value <= target
    if not on_target:
        return f"{value:g}"
    return f"{value:g} {'✅' if met else '❌'}"


def render(
    title: str,
    environment: Mapping[str, Any],
    workload: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    load: Sequence[Mapping[str, Any]] = (),
    notes: Sequence[str] = (),
) -> str:
    on_target = bool(environment["matches_target_host"])
    env_line = (
        f"{environment['cpu_model']} ({environment['machine']}), "
        f"{environment['cpu_limit'] or environment['logical_cpus']} CPUs"
        f"{' (container limit)' if environment['cpu_limit'] else ''}, "
        f"{environment['memory_gb']} GB, {environment['system']}, Python {environment['python']}"
    )
    lines = [
        f"# {title}",
        "",
        f"- Measured {environment['measured_at']} at commit `{environment['git_commit']}`",
        f"- Hardware: {env_line}",
        (
            "- **This is the documented target host**: targets are judged below."
            if on_target
            else "- **Local proxy run, not the documented 2 vCPU / 4 GB x86-64 target host.** "
            "Numbers indicate relative cost; targets are not judged here."
        ),
        f"- Workload `{workload['version']}`: {workload['source']}; lengths in "
        f"`{workload['tokenizer']['name']}` subword tokens. Natural-sample distribution: "
        + ", ".join(f"{k} {v}" for k, v in workload["natural_token_distribution"].items()),
        *(f"- {note}" for note in notes),
        "",
        "## Warm latency, memory and throughput (in process, one request at a time)",
        "",
        "| Configuration | Model | p50 ~512 | p95 ~512 | p50 ~2000 | p95 ~2000 "
        "| Natural docs/s | Peak RSS (MB) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        b = r["buckets"]
        short, long_ = b.get("~512", {}), b.get("~2000", {})
        rate = b.get("natural", {}).get("docs_per_s")
        lines.append(
            f"| {r['config']['name']} | `{r['model_id']}` "
            f"| {short.get('p50', 'n/a')} "
            f"| {_verdict(short.get('p95'), TARGETS['p95_512_s'], False, on_target)} "
            f"| {long_.get('p50', 'n/a')} "
            f"| {_verdict(long_.get('p95'), TARGETS['p95_2000_s'], False, on_target)} "
            f"| {_verdict(rate, TARGETS['docs_per_s'], True, on_target)} "
            f"| {_verdict(r['peak_rss_mb'], TARGETS['peak_rss_mb'], False, on_target)} |"
        )
    lines += [
        f"| *Target (documented host)* | | | ≤ {TARGETS['p95_512_s']} | "
        f"| ≤ {TARGETS['p95_2000_s']} | ≥ {TARGETS['docs_per_s']} | ≤ {TARGETS['peak_rss_mb']} |",
        "",
        "Latencies are seconds per document, including preprocessing, windowing, inference and "
        "decoding; p95 over all documents and repeats in the bucket.",
        "",
        "## Cold start (fresh process)",
        "",
        "| Configuration | Imports (s) | Model load (s) | First extraction (s) | Total (s) |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in results:
        c = r["cold_start"]
        lines.append(
            f"| {r['config']['name']} | {c['imports_s']} | {c['load_s']} "
            f"| {c['first_extraction_s']} | {c['total_s']} |"
        )
    if load:
        lines += [
            "",
            "## HTTP load test",
            "",
            "| Service | Requests | Concurrency | Success | p50 (s) | p95 (s) | p99 (s) "
            "| Throughput (req/s) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for item in load:
            lat = item["latency_s"]
            lines.append(
                f"| {item.get('label', 'service')} | {item['requests']} | {item['concurrency']} "
                f"| {item['success_rate']:.2%} | {lat['p50']} | {lat['p95']} | {lat['p99']} "
                f"| {item['throughput_rps']} |"
            )
        lines += ["", "Target: ≥ 99.5% successful requests at the supported load."]
    lines.append("")
    return "\n".join(lines)
