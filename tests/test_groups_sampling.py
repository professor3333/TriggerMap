from collections import Counter

import pytest

from tests.factories import make_doc
from triggermap.corpus.groups import build_groups
from triggermap.corpus.sampling import PilotParams, sample_pilot


def test_project_and_duplicate_groups_merge_transitively() -> None:
    docs = [
        make_doc("GHSA-2222-2222-2222", "a", ("tensorflow",)),
        make_doc("GHSA-3333-3333-3333", "b", ("tensorflow", "tensorflow-gpu")),
        make_doc("GHSA-4444-4444-4444", "c", ("tensorflow-gpu",)),
        make_doc("GHSA-5555-5555-5555", "Same  TEXT", ("other",)),
        make_doc("GHSA-6666-6666-6666", "same text", ("third",)),
        make_doc("GHSA-7777-7777-7777", "x", ("solo",), aliases=("CVE-1",)),
        make_doc("GHSA-8888-8888-8888", "y", ("solo2",), aliases=("CVE-1",)),
        make_doc("GHSA-9999-9999-9999", "", ("e1",), summary="only summary one"),
        make_doc("GHSA-cccc-cccc-cccc", "", ("e2",), summary="only summary two"),
    ]
    groups = build_groups(docs)
    tf = {groups.project[d.advisory_id] for d in docs[:3]}
    assert tf == {"GHSA-2222-2222-2222"}
    assert groups.duplicate["GHSA-6666-6666-6666"] == "GHSA-5555-5555-5555"
    assert groups.duplicate["GHSA-8888-8888-8888"] == "GHSA-7777-7777-7777"
    # Empty details must not make every summary-only advisory a duplicate.
    assert groups.duplicate["GHSA-cccc-cccc-cccc"] == "GHSA-cccc-cccc-cccc"
    # Leakage groups combine both relations.
    assert groups.leakage["GHSA-6666-6666-6666"] == groups.leakage["GHSA-5555-5555-5555"]
    assert groups.project["GHSA-6666-6666-6666"] != groups.project["GHSA-5555-5555-5555"]


def test_pilot_sampling_is_deterministic_and_respects_caps() -> None:
    docs = [
        make_doc(
            f"GHSA-2222-2222-{i:04d}",
            f"{'When enabled, unless admin.' if i % 2 else 'Bug'} {i}",
            (f"p{i % 25}",),
        )
        for i in range(100)
    ]
    groups = build_groups(docs)
    params = PilotParams(n_random=10, n_enriched=10, per_project_cap=1)
    first = sample_pilot(docs, groups, params)
    assert first == sample_pilot(docs, groups, params)
    assert Counter(i.stratum for i in first) == {"random": 10, "enriched": 10}
    assert max(Counter(i.project_group for i in first).values()) == 1
    assert len({i.advisory_id for i in first}) == 20
    assert [i.order for i in first] == list(range(20))
    for item in first:
        expected = "evaluation_candidate" if item.stratum == "random" else "training"
        assert item.intended_use == expected
    assert all(i.condition_score >= 2 for i in first if i.stratum == "enriched")
    assert (
        sample_pilot(
            docs, groups, PilotParams(n_random=10, n_enriched=10, per_project_cap=1, seed=1)
        )
        != first
    )


def test_pilot_sampling_fails_loudly_when_caps_cannot_be_met() -> None:
    docs = [make_doc(f"GHSA-2222-2222-{i:04d}", f"text {i}", ("same",)) for i in range(10)]
    with pytest.raises(ValueError, match="random"):
        sample_pilot(docs, build_groups(docs), PilotParams(n_random=3, n_enriched=0))
