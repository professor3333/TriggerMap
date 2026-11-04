"""Every committed annotation file is valid and pinned to its sample and snapshot.

CI has no corpus, so span text is checked at import time (``annotate import``); here every
check that needs no text runs on every committed record. Records in the locked test split are
checked for provenance only: their labels are not read.
"""

import json
from pathlib import Path

import pytest

from triggermap.schema import AdvisoryAnnotation, AnnotationOrigin, validate_structure

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = json.loads((ROOT / "data/manifests/snapshot.json").read_text())
ASSIGNMENT = json.loads((ROOT / "splits/pool-v1.json").read_text())["assignment"]
FILES = sorted((ROOT / "annotations").glob("*/*.jsonl"))


def _sample_for(path: Path) -> Path:
    if path.parent.name == "pilot":
        return path.parent / "pilot_manifest.json"
    return path.with_suffix(".json")


def test_annotation_files_exist() -> None:
    assert FILES, "no committed annotation files found"


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_committed_annotation_file(path: Path) -> None:
    items = {
        item["advisory_id"]: item for item in json.loads(_sample_for(path).read_text())["items"]
    }
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        record = AdvisoryAnnotation.model_validate_json(line)
        aid = record.advisory_id
        assert aid not in seen, f"{path.name}: {aid} appears twice"
        seen.add(aid)
        assert aid in items, f"{path.name}: {aid} is not in its sample"
        assert record.content_hash == items[aid]["content_hash"], f"{aid}: text hash differs"
        assert record.source_commit == SNAPSHOT["source"]["commit"], f"{aid}: other snapshot"
        assert record.preprocessing_version == SNAPSHOT["preprocessing_version"]
        if record.origin not in (None, AnnotationOrigin.MANUAL):
            assert record.origin_model, f"{aid}: model-drafted record without origin_model"
        if ASSIGNMENT.get(aid) == "test":
            continue  # locked: provenance only
        assert validate_structure(record) == [], f"{aid}: structural issues"
