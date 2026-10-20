import json
from collections import Counter
from pathlib import Path

import pytest

from tests.factories import make_doc
from triggermap.corpus.batches import (
    BatchParams,
    already_sampled,
    batch_manifest,
    sample_batch,
    uncertainty,
)
from triggermap.schema import Category, Condition, DocumentStatus, Extraction, Role


def ghsa(i: int) -> str:
    a = "23456789cfghjmpqrvwx"
    return f"GHSA-{a[i // 400 % 20] * 4}-{a[i // 20 % 20] * 4}-{a[i % 20] * 4}"


@pytest.fixture
def setup():  # type: ignore[no-untyped-def]
    docs = []
    for i in range(80):
        text = "When debug is enabled and the user is authenticated." if i % 4 == 0 else f"Bug {i}."
        docs.append(make_doc(ghsa(i), f"{text} {i}", (f"p{i // 4}",)))
    assignment = {d.advisory_id: ("train" if i < 60 else "dev") for i, d in enumerate(docs)}
    manifest = {
        "params": {"version": "t"},
        "assignment_sha256": "x",
        "assignment": assignment,
        "group_of": {d.advisory_id: f"g{i // 4}" for i, d in enumerate(docs)},
        "excluded_documents": {ghsa(1): "test"},
    }
    return docs, manifest


def test_natural_batch_caps_groups_and_skips_seen(setup) -> None:  # type: ignore[no-untyped-def]
    docs, manifest = setup
    params = BatchParams(name="b1", pool="train", n=20, per_group_cap=2)
    items = sample_batch(docs, manifest, params, exclude={ghsa(2)})
    ids = [i.advisory_id for i in items]
    assert len(ids) == len(set(ids)) == 20
    assert ghsa(1) not in ids and ghsa(2) not in ids  # excluded and already sampled
    assert all(manifest["assignment"][a] == "train" for a in ids)
    assert max(Counter(i.leakage_group for i in items).values()) <= 2
    assert items == sample_batch(docs, manifest, params, exclude={ghsa(2)})
    assert [i.order for i in items] == list(range(20))
    other = sample_batch(docs, manifest, params.model_copy(update={"name": "b2"}), exclude=set())
    assert [i.advisory_id for i in other] != ids  # seed depends on the batch name


def test_evaluation_pools_are_natural_only(setup) -> None:  # type: ignore[no-untyped-def]
    docs, manifest = setup
    with pytest.raises(ValueError, match="natural"):
        sample_batch(
            docs, manifest, BatchParams(name="x", pool="dev", n=5, strategy="enriched"), set()
        )
    items = sample_batch(docs, manifest, BatchParams(name="d", pool="dev", n=5), set())
    assert {i.intended_use for i in items} == {"evaluation"}
    with pytest.raises(ValueError, match="only"):
        sample_batch(docs, manifest, BatchParams(name="d", pool="dev", n=50), set())


def test_enriched_prefers_condition_rich_documents(setup) -> None:  # type: ignore[no-untyped-def]
    docs, manifest = setup
    params = BatchParams(name="e", pool="train", n=10, strategy="enriched", per_group_cap=5)
    items = sample_batch(docs, manifest, params, set())
    assert all(i.condition_score >= 2 for i in items)


def prediction(aid: str, confidence: float | None) -> Extraction:
    conditions = (
        ()
        if confidence is None
        else (
            Condition(
                id="c1",
                span=(0, 4),
                category=Category.USAGE,
                role=Role.REQUIRED,
                confidence=confidence,
            ),
        )
    )
    return Extraction(
        advisory_id=aid,
        content_hash="a" * 64,
        preprocessing_version="1",
        model_id="m",
        document_status=DocumentStatus.HAS_CONDITIONS
        if conditions
        else DocumentStatus.NO_EXPLICIT_CONDITION,
        conditions=conditions,
    )


def test_uncertainty_sampling_mixes_in_natural(setup) -> None:  # type: ignore[no-untyped-def]
    docs, manifest = setup
    assert uncertainty(prediction("x", 0.5)) == 1.0
    assert uncertainty(prediction("x", 0.99)) == pytest.approx(0.02)
    assert uncertainty(prediction("x", None)) == 0.0
    preds = {
        d.advisory_id: prediction(d.advisory_id, 0.5 if i < 8 else 0.99) for i, d in enumerate(docs)
    }
    params = BatchParams(name="u", pool="train", n=10, strategy="uncertainty", per_group_cap=4)
    items = sample_batch(docs, manifest, params, {ghsa(0)}, preds)
    strata = Counter(i.stratum for i in items)
    assert strata == {"uncertainty": 7, "natural": 3}
    uncertain = {i.advisory_id for i in items if i.stratum == "uncertainty"}
    assert {ghsa(i) for i in range(2, 8)} <= uncertain
    with pytest.raises(ValueError, match="predictions"):
        sample_batch(docs, manifest, params, set())


def test_manifest_and_already_sampled(setup, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    docs, manifest = setup
    params = BatchParams(name="b", pool="train", n=3)
    items = sample_batch(docs, manifest, params, set())
    data = batch_manifest(items, params, manifest)
    path = tmp_path / "b.json"
    path.write_text(json.dumps(data))
    assert already_sampled([path]) == {i.advisory_id for i in items}
    assert data["split_version"] == "t" and data["counts"] == {"natural": 3}


def test_committed_samples_never_overlap_and_respect_pools() -> None:
    root = Path(__file__).resolve().parents[1]
    split = json.loads((root / "splits/pool-v1.json").read_text())
    seen: Counter[str] = Counter()
    for path in sorted((root / "annotations/batches").glob("*.json")):
        data = json.loads(path.read_text())
        assert data["split_assignment_sha256"] == split["assignment_sha256"]
        for item in data["items"]:
            seen[item["advisory_id"]] += 1
            assert split["assignment"][item["advisory_id"]] == item["pool"]
            assert item["advisory_id"] not in split["excluded_documents"]
            if item["pool"] != "train":
                assert item["stratum"] == "natural"
    pilot = json.loads((root / "annotations/pilot/pilot_manifest.json").read_text())
    seen.update(i["advisory_id"] for i in pilot["items"])
    assert [aid for aid, n in seen.items() if n > 1] == []
