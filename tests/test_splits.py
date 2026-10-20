import json
from collections import Counter
from pathlib import Path

import pytest

from tests.factories import make_doc
from triggermap.corpus.groups import build_groups
from triggermap.corpus.neardup import NearDupParams, jaccard, near_duplicate_pairs, shingles
from triggermap.corpus.splits import (
    SplitParams,
    assignment_hash,
    build_split,
    check_split_manifest,
    select,
)

BASE = (
    "When the application enables the legacy upload handler and passes user controlled "
    "file names to the storage backend an attacker can overwrite arbitrary files on disk"
)


def test_shingles_and_jaccard() -> None:
    a, b = shingles(BASE, 5), shingles(BASE + " quickly", 5)
    assert 0.9 < jaccard(a, b) < 1.0
    assert jaccard(a, a) == 1.0
    assert shingles("", 5) == frozenset()


def test_near_duplicates_found_and_verified() -> None:
    texts = {
        "a": BASE,
        "b": BASE.replace("legacy", "old"),
        "c": "A completely different advisory about integer overflow in the image decoder.",
    }
    pairs = near_duplicate_pairs(texts, NearDupParams(threshold=0.6))
    assert [(x, y) for x, y, _ in pairs] == [("a", "b")]
    assert pairs[0][2] >= 0.6
    assert near_duplicate_pairs(texts, NearDupParams(threshold=0.99)) == []


def ghsa(i: int) -> str:
    alphabet = "23456789cfghjmpqrvwx"
    return f"GHSA-{alphabet[i // 400 % 20] * 4}-{alphabet[i // 20 % 20] * 4}-{alphabet[i % 20] * 4}"


@pytest.fixture
def corpus():  # type: ignore[no-untyped-def]
    docs = []
    for i in range(120):
        doc = make_doc(ghsa(i), f"Advisory {i} text unique {i * 7919}", (f"pkg{i // 3}",))
        year = 2020 + i % 7
        docs.append(doc.model_copy(update={"published": f"{year}-01-01T00:00:00Z"}))
    # One large project, a shared upstream repo, and an alias duplicate.
    for i in range(120, 160):
        docs.append(make_doc(ghsa(i), f"Large project advisory {i}", ("bigproj",)))
    docs[0] = docs[0].model_copy(update={"upstream_repo": "org/shared"})
    docs[10] = docs[10].model_copy(update={"upstream_repo": "org/shared"})
    docs[20] = docs[20].model_copy(update={"aliases": ("CVE-1",)})
    docs[30] = docs[30].model_copy(update={"aliases": ("CVE-1",)})
    return docs


def test_split_keeps_groups_together_and_respects_pilot(corpus) -> None:  # type: ignore[no-untyped-def]
    groups = build_groups(corpus)
    assert groups.leakage[ghsa(0)] == groups.leakage[ghsa(10)]  # shared upstream repo
    assert groups.leakage[ghsa(20)] == groups.leakage[ghsa(30)]  # shared alias
    pilot = [
        {"advisory_id": ghsa(5), "stratum": "random"},
        {"advisory_id": ghsa(130), "stratum": "random"},  # inside the large project
        {"advisory_id": ghsa(39), "stratum": "enriched"},  # pkg13, with a random doc below
        {"advisory_id": ghsa(40), "stratum": "enriched"},
        {"advisory_id": ghsa(41), "stratum": "random"},
        {"advisory_id": ghsa(60), "stratum": "enriched"},  # pkg20, training only
    ]
    params = SplitParams(max_eval_group_docs=10, dev_fraction=0.2, test_fraction=0.2)
    manifest = build_split(corpus, groups, params, pilot)
    assert check_split_manifest(manifest) == []
    assignment = manifest["assignment"]
    for aid in (ghsa(5), ghsa(130), ghsa(41)):
        assert assignment[aid] in ("dev", "test")
    assert assignment[ghsa(130)] == "dev"  # large project kept for evaluation, not test
    assert manifest["excluded_documents"] == {
        ghsa(39): "training-stratum pilot document in an evaluation group",
        ghsa(40): "training-stratum pilot document in an evaluation group",
    }
    assert assignment[ghsa(60)] == "train"
    # Test holds the newest groups: each test group was first published no earlier than any
    # small group left in dev that the pilot did not force into evaluation.
    first: dict[str, str] = {}
    size: Counter[str] = Counter()
    for doc in corpus:
        key = groups.leakage[doc.advisory_id]
        first[key] = min(first.get(key, doc.published), doc.published)
        size[key] += 1
    forced = {groups.leakage[i["advisory_id"]] for i in pilot}
    test_groups = {k for k in first if assignment[k] == "test"}
    other_small = {
        k
        for k in first
        if assignment[k] == "dev" and size[k] <= params.max_eval_group_docs and k not in forced
    }
    assert test_groups
    assert min(first[k] for k in test_groups) >= max(first[k] for k in other_small)
    assert manifest == build_split(corpus, groups, params, pilot)  # deterministic
    assert select([ghsa(40), ghsa(5)], manifest, "dev") == [
        aid for aid in [ghsa(5)] if assignment[aid] == "dev"
    ]
    with pytest.raises(ValueError, match="not in the split manifest"):
        select(["GHSA-xxxx-xxxx-xxxx"], manifest, "dev")


def test_tampered_manifest_is_detected(corpus) -> None:  # type: ignore[no-untyped-def]
    manifest = build_split(corpus, build_groups(corpus), SplitParams(), [])
    moved = dict(manifest["assignment"])
    victim = ghsa(0)
    moved[victim] = "test" if moved[victim] != "test" else "train"
    broken = {**manifest, "assignment": moved}
    problems = check_split_manifest(broken)
    assert any("assignment_sha256" in p for p in problems)
    fixed_hash = {**broken, "assignment_sha256": assignment_hash(moved)}
    assert any("span several splits" in p or "count" in p for p in check_split_manifest(fixed_hash))


def test_committed_pool_manifest_is_consistent() -> None:
    """Data contract on the frozen split that every experiment depends on."""
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "splits/pool-v1.json").read_text())
    pilot = json.loads((root / "annotations/pilot/pilot_manifest.json").read_text())
    assert check_split_manifest(manifest) == []
    assert manifest["frozen"] is True
    assert manifest["source_commit"] == pilot["source_commit"]
    assignment = manifest["assignment"]
    for item in pilot["items"]:
        split = assignment[item["advisory_id"]]
        if item["stratum"] == "random":
            assert split in ("dev", "test"), item["advisory_id"]
        elif split != "train":
            assert item["advisory_id"] in manifest["excluded_documents"]
    assert sum(s["documents"] for s in manifest["splits"].values()) == len(assignment)
