"""Benchmark one configuration in a fresh process and print the result as JSON.

Run by the orchestrator as ``python -m triggermap.bench.worker CONFIG WORKLOAD PROCESSED
REPEATS`` so that cold start (imports + model load + first extraction) and peak memory are
measured per configuration, not inherited from a previous one.
"""

from __future__ import annotations

import time

_PROCESS_START = time.perf_counter()

import json  # noqa: E402
import resource  # noqa: E402
import statistics  # noqa: E402
import sys  # noqa: E402
from dataclasses import asdict, dataclass  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any  # noqa: E402


@dataclass(frozen=True)
class BenchConfig:
    kind: str
    model_dir: str | None = None
    threads: int | None = None
    batch_size: int | None = None
    label: str | None = None

    @property
    def name(self) -> str:
        if self.label:
            return self.label
        parts = [self.kind]
        if self.threads:
            parts.append(f"t{self.threads}")
        if self.batch_size:
            parts.append(f"b{self.batch_size}")
        return "-".join(parts)


def parse_config(spec: str) -> BenchConfig:
    """``kind=onnx,dir=PATH,threads=2,batch=4,label=name`` (only ``kind`` is required)."""
    fields = dict(part.split("=", 1) for part in spec.split(",") if part)
    return BenchConfig(
        kind=fields["kind"],
        model_dir=fields.get("dir"),
        threads=int(fields["threads"]) if "threads" in fields else None,
        batch_size=int(fields["batch"]) if "batch" in fields else None,
        label=fields.get("label"),
    )


def _peak_rss_mb() -> float:
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(peak / 2**20 if sys.platform == "darwin" else peak / 2**10, 1)


def _summary(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    last = len(ordered) - 1
    return {
        "n": len(ordered),
        "p50": round(ordered[round(0.5 * last)], 4),
        "p95": round(ordered[round(0.95 * last)], 4),
        "max": round(ordered[-1], 4),
        "mean": round(statistics.fmean(ordered), 4),
    }


def run(
    config: BenchConfig, workload: dict[str, Any], texts: dict[str, str], repeats: int
) -> dict[str, Any]:
    if config.threads and config.kind in ("transformer",):
        import torch

        torch.set_num_threads(config.threads)
    from triggermap.text.preprocessing import preprocess

    imports_done = time.perf_counter()
    model_dir = Path(config.model_dir) if config.model_dir else None
    if config.kind == "onnx":
        from triggermap.models.transformer.onnx_bundle import OnnxExtractor

        assert model_dir is not None
        extractor: Any = OnnxExtractor(model_dir, threads=config.threads)
    else:
        from triggermap.models.registry import load_extractor

        extractor = load_extractor(config.kind, model_dir, device="cpu")
    if config.batch_size and hasattr(extractor, "batch_size"):
        extractor.batch_size = config.batch_size
    loaded = time.perf_counter()

    def once(advisory_id: str) -> float:
        started = time.perf_counter()
        extractor.extract(preprocess(texts[advisory_id]), advisory_id)
        return time.perf_counter() - started

    first_id = workload["buckets"]["natural"][0]["advisory_id"]
    first = once(first_id)
    result: dict[str, Any] = {
        "config": asdict(config) | {"name": config.name},
        "model_id": extractor.model_id,
        "cold_start": {
            "imports_s": round(imports_done - _PROCESS_START, 3),
            "load_s": round(loaded - imports_done, 3),
            "first_extraction_s": round(first, 3),
            "total_s": round(loaded - _PROCESS_START + first, 3),
        },
        "buckets": {},
    }
    for bucket, items in workload["buckets"].items():
        if not items:
            continue
        once(items[0]["advisory_id"])  # warm-up for this length
        runs = 1 if bucket == "natural" else repeats
        latencies = [once(item["advisory_id"]) for _ in range(runs) for item in items]
        stats = _summary(latencies)
        if bucket == "natural":
            stats["docs_per_s"] = round(len(items) / sum(latencies), 3)
        result["buckets"][bucket] = stats
    result["peak_rss_mb"] = _peak_rss_mb()
    return result


def main(argv: list[str]) -> int:
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.text.preprocessing import compose_raw

    config = BenchConfig(**json.loads(argv[0]))
    workload = json.loads(Path(argv[1]).read_text())
    wanted = {i["advisory_id"] for items in workload["buckets"].values() for i in items}
    texts = {
        d.advisory_id: compose_raw(d.summary, d.details)
        for d in load_corpus(Path(argv[2]) / CORPUS_FILE)
        if d.advisory_id in wanted
    }
    print(json.dumps(run(config, workload, texts, int(argv[3]))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
