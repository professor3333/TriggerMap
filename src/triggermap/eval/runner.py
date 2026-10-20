"""Load gold and predictions, check they describe the same text, score them."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from triggermap.eval.bootstrap import Interval, bootstrap
from triggermap.eval.metrics import DocCounts, Labelled, collect, summary
from triggermap.schema.models import AdvisoryAnnotation, Extraction


def load_gold(path: Path) -> dict[str, Labelled]:
    with path.open(encoding="utf-8") as fh:
        records = [AdvisoryAnnotation.model_validate_json(line) for line in fh if line.strip()]
    return {r.advisory_id: r for r in records}


def load_predictions(path: Path) -> dict[str, Extraction]:
    out: dict[str, Extraction] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                record = Extraction.model_validate_json(line)
                if record.advisory_id is None:
                    raise ValueError("evaluation predictions need an advisory_id")
                out[record.advisory_id] = record
    return out


def check_alignment(gold: Mapping[str, Labelled], pred: Mapping[str, Extraction]) -> None:
    """Refuse to score predictions made on different text or preprocessing."""
    problems = [
        aid
        for aid, p in pred.items()
        if aid in gold
        and (
            p.content_hash != gold[aid].content_hash
            or p.preprocessing_version != gold[aid].preprocessing_version
        )
    ]
    if problems:
        raise ValueError(f"text or preprocessing differs from gold for: {', '.join(problems[:5])}")


def evaluate(
    gold: dict[str, Labelled],
    pred: dict[str, Extraction],
    cluster_of: Mapping[str, str] | None = None,
    samples: int = 1000,
    seed: int = 0,
) -> tuple[list[DocCounts], dict[str, Interval]]:
    check_alignment(gold, pred)
    docs = collect(gold, pred)
    return docs, bootstrap(docs, summary, cluster_of, samples, seed)
