from pathlib import Path

import pytest

from triggermap.cli import main
from triggermap.eval.bootstrap import bootstrap, clusters_of, paired_bootstrap
from triggermap.eval.metrics import collect, micro, precision_coverage, summary
from triggermap.eval.runner import check_alignment, evaluate
from triggermap.schema import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)

H = "a" * 64
U, C, A, P = Category.USAGE, Category.CONFIGURATION, Category.ACCESS, Category.PLATFORM
REQ, EXC, NOT = Role.REQUIRED, Role.EXCEPTION, Role.NOT_REQUIRED


def cond(cid: str, span: tuple[int, int], cat: Category, role: Role, conf: float | None = None):  # type: ignore[no-untyped-def]
    return Condition(id=cid, span=span, category=cat, role=role, confidence=conf)


def gold(aid: str, conditions: tuple[Condition, ...] = (), groups: tuple[Group, ...] = ()):  # type: ignore[no-untyped-def]
    status = DocumentStatus.HAS_CONDITIONS if conditions else DocumentStatus.NO_EXPLICIT_CONDITION
    return AdvisoryAnnotation(
        advisory_id=aid,
        source_commit="c" * 40,
        content_hash=H,
        preprocessing_version="1",
        annotation_version="t",
        document_status=status,
        conditions=conditions,
        groups=groups,
    )


def pred(aid: str, conditions: tuple[Condition, ...] = (), groups: tuple[Group, ...] = ()):  # type: ignore[no-untyped-def]
    status = DocumentStatus.HAS_CONDITIONS if conditions else DocumentStatus.NO_EXPLICIT_CONDITION
    return Extraction(
        advisory_id=aid,
        content_hash=H,
        preprocessing_version="1",
        model_id="test",
        document_status=status,
        conditions=conditions,
        groups=groups,
    )


GA, GB, GC = "GHSA-2222-2222-2222", "GHSA-3333-3333-3333", "GHSA-4444-4444-4444"


@pytest.fixture
def scored():  # type: ignore[no-untyped-def]
    gold_docs = {
        GA: gold(
            GA,
            (
                cond("c1", (0, 5), U, REQ),
                cond("c2", (10, 15), C, REQ),
                cond("c3", (20, 25), P, NOT),
            ),
            (Group(operator=GroupOperator.ALL, members=("c1", "c2")),),
        ),
        GB: gold(GB),
        GC: gold(GC, (cond("c1", (0, 4), A, EXC),)),
    }
    predictions = {
        GA: pred(
            GA,
            (
                cond("p1", (0, 5), U, REQ, 0.9),  # correct
                cond("p2", (10, 15), U, REQ, 0.8),  # right span, wrong category
                cond("p3", (30, 35), A, REQ, 0.3),  # invented prerequisite
                cond("p4", (20, 25), P, REQ, 0.6),  # reversed meaning
            ),
            (Group(operator=GroupOperator.ALL, members=("p1", "p2")),),
        ),
        GB: pred(GB),
        # GC has no prediction: counts as empty.
    }
    return gold_docs, predictions


def test_summary_matches_hand_computed_values(scored) -> None:  # type: ignore[no-untyped-def]
    docs = collect(*scored)
    s = summary(docs)
    assert s["span_precision"] == s["span_recall"] == s["span_f1"] == 0.75
    assert s["typed_f1"] == 0.25
    assert s["role_macro_f1"] == pytest.approx((2 / 3 + 0 + 0) / 3)
    assert s["group_f1"] == 1.0
    assert s["doc_exact_with_conditions"] == 0.0
    assert s["doc_exact_without_conditions"] == 1.0
    assert s["false_prerequisite_rate"] == 0.25
    assert s["reversed_meaning_rate"] == pytest.approx(1 / 3)
    assert s["category_acc_on_matched_spans"] == pytest.approx(2 / 3)
    assert s["role_acc_on_matched_spans"] == pytest.approx(2 / 3)
    required = micro(docs, "role:REQUIRED")
    assert (required.precision, required.recall, required.support) == (0.5, 1.0, 2)
    assert micro(docs, "role:UNCERTAIN").support == 0


def test_precision_coverage_curve(scored) -> None:  # type: ignore[no-untyped-def]
    curve = precision_coverage(collect(*scored), points=4)
    assert [p.coverage for p in curve] == [0.25, 0.5, 0.75, 1.0]
    assert [p.threshold for p in curve] == [0.9, 0.8, 0.6, 0.3]
    assert curve[0].precision == 1.0
    assert curve[-1].precision == 0.25
    assert curve[0].retained_recall == 0.25


def test_bootstrap_is_seeded_and_brackets_estimate(scored) -> None:  # type: ignore[no-untyped-def]
    docs = collect(*scored)
    first = bootstrap(docs, summary, samples=200, seed=1)
    assert first == bootstrap(docs, summary, samples=200, seed=1)
    for interval in first.values():
        assert interval.low <= interval.high


def test_clusters_group_related_documents(scored) -> None:  # type: ignore[no-untyped-def]
    docs = collect(*scored)
    assert clusters_of(docs, None) == [[0], [1], [2]]
    assert clusters_of(docs, {GA: "x", GC: "x"}) == [[1], [0, 2]]


def test_paired_bootstrap(scored) -> None:  # type: ignore[no-untyped-def]
    gold_docs, predictions = scored
    docs = collect(gold_docs, predictions)
    same = paired_bootstrap(docs, docs, summary, samples=100)
    assert same["typed_f1"].difference == 0.0
    assert same["typed_f1"].p_not_better == 1.0
    perfect = collect(
        gold_docs, {aid: pred(aid, g.conditions, g.groups) for aid, g in gold_docs.items()}
    )
    better = paired_bootstrap(docs, perfect, summary, samples=100)
    assert better["typed_f1"].difference == 0.75
    # With 3 documents, ~4% of resamples contain only the empty document (difference 0).
    assert better["typed_f1"].low >= 0
    assert better["typed_f1"].p_not_better < 0.1
    with pytest.raises(ValueError):
        paired_bootstrap(docs, docs[:2], summary)


def test_alignment_is_enforced(scored) -> None:  # type: ignore[no-untyped-def]
    gold_docs, predictions = scored
    stale = predictions[GA].model_copy(update={"content_hash": "b" * 64})
    with pytest.raises(ValueError, match=GA):
        check_alignment(gold_docs, {GA: stale})
    docs, intervals = evaluate(gold_docs, predictions, samples=50)
    assert len(docs) == 3
    assert intervals["typed_f1"].estimate == 0.25


def test_evaluate_cli(scored, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    gold_docs, predictions = scored
    gold_path, pred_path, out = tmp_path / "g.jsonl", tmp_path / "p.jsonl", tmp_path / "r.md"
    gold_path.write_text("".join(g.model_dump_json() + "\n" for g in gold_docs.values()))
    pred_path.write_text("".join(p.model_dump_json() + "\n" for p in predictions.values()))
    from tests.factories import write_split_manifest

    split = write_split_manifest(tmp_path / "split.json", {GA: "dev", GB: "dev", GC: "dev"})
    args = [str(gold_path), str(pred_path), "--clusters", "document", "--samples", "50"]
    assert main(["evaluate", *args, "--split-manifest", str(split), "--out", str(out)]) == 0
    report = out.read_text()
    assert "| Typed condition micro-F1 (span + category + role) | 0.250 |" in report
    assert "| REQUIRED | 0.500 | 1.000 | 0.667 | 2 |" in report
    assert "## Precision versus coverage" in report


def test_test_split_is_locked_and_logged(scored, tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from tests.factories import write_split_manifest

    gold_docs, predictions = scored
    gold_path, pred_path = tmp_path / "g.jsonl", tmp_path / "p.jsonl"
    gold_path.write_text("".join(g.model_dump_json() + "\n" for g in gold_docs.values()))
    pred_path.write_text("".join(p.model_dump_json() + "\n" for p in predictions.values()))
    split = write_split_manifest(tmp_path / "split.json", {GA: "dev", GB: "test", GC: "train"})
    monkeypatch.chdir(tmp_path)
    base = ["evaluate", str(gold_path), str(pred_path), "--split-manifest", str(split)]
    base += ["--clusters", "document", "--samples", "20", "--out", "r.md"]
    with pytest.raises(SystemExit, match="locked"):
        main([*base, "--split", "test"])
    assert not (tmp_path / "docs/test-access-log.md").exists()
    assert main([*base, "--split", "test", "--release-evaluation", "v0.1 release"]) == 0
    log = (tmp_path / "docs/test-access-log.md").read_text()
    assert "v0.1 release" in log and "test" in log
    assert main([*base, "--split", "dev"]) == 0
    assert "Documents: 1 " in (tmp_path / "r.md").read_text()


def test_multiple_gold_files_merge_and_reject_duplicates(scored, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    from triggermap.eval.runner import load_gold_files

    gold_docs, _ = scored
    records = list(gold_docs.values())
    first, second = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    first.write_text(records[0].model_dump_json() + "\n")
    second.write_text("".join(r.model_dump_json() + "\n" for r in records[1:]))
    assert set(load_gold_files([first, second])) == set(gold_docs)
    with pytest.raises(ValueError, match="more than one gold file"):
        load_gold_files([first, first])
