from pathlib import Path

import pytest

from tests.factories import write_split_manifest
from tests.test_eval import GA, GB, cond, gold, pred
from triggermap.cli import main
from triggermap.eval import multiref
from triggermap.eval.bootstrap import Comparison
from triggermap.schema import Category, Role

U, C, A = Category.USAGE, Category.CONFIGURATION, Category.ACCESS
REQ, EXC = Role.REQUIRED, Role.EXCEPTION


def _refs_and_pred():  # type: ignore[no-untyped-def]
    ref_a = gold(GA, (cond("c1", (0, 5), U, REQ), cond("c2", (10, 15), C, REQ)))
    ref_b = gold(GA, (cond("c1", (0, 5), U, REQ), cond("c3", (20, 25), A, REQ)))
    system = pred(
        GA,
        (
            cond("p1", (0, 5), U, REQ),  # in both references
            cond("p2", (20, 25), A, REQ),  # in B only
            cond("p3", (30, 35), U, REQ),  # in neither, overlaps nothing
            cond("p4", (10, 15), C, EXC),  # A's span with another role
        ),
    )
    return ref_a, ref_b, system


def test_two_reference_summary_by_hand() -> None:
    ref_a, ref_b, system = _refs_and_pred()
    docs = multiref.collect_two({GA: ref_a}, {GA: ref_b}, {GA: system})
    s = multiref.two_reference_summary(docs)
    assert s["typed_f1_a"] == pytest.approx(1 / 3)  # P 1/4, R 1/2
    assert s["typed_f1_b"] == pytest.approx(2 / 3)  # P 2/4, R 1
    assert s["span_f1_a"] == pytest.approx(2 / 3)  # spans: 2 of 4 predicted, both of A's
    assert s["consensus_recall"] == 1.0
    assert s["supported_both"] == pytest.approx(1 / 4)
    assert s["supported_either"] == pytest.approx(2 / 4)
    assert s["invented_a"] == pytest.approx(2 / 3)  # p2 and p3 touch nothing in A
    assert s["invented_b"] == pytest.approx(1 / 3)
    assert s["invented_union"] == pytest.approx(1 / 3)
    assert multiref.consensus_size({GA: ref_a}, {GA: ref_b}) == 1


def test_missing_prediction_counts_as_empty() -> None:
    ref_a, ref_b, _ = _refs_and_pred()
    s = multiref.two_reference_summary(multiref.collect_two({GA: ref_a}, {GA: ref_b}, {}))
    assert s["typed_f1_a"] == 0.0 and s["consensus_recall"] == 0.0 and s["invented_union"] == 0.0


def test_references_must_align() -> None:
    ref_a, ref_b, system = _refs_and_pred()
    with pytest.raises(ValueError, match="same documents"):
        multiref.collect_two({GA: ref_a}, {GA: ref_b, GB: gold(GB)}, {})
    other = ref_b.model_copy(update={"content_hash": "b" * 64})
    with pytest.raises(ValueError, match="different texts"):
        multiref.collect_two({GA: ref_a}, {GA: other}, {})
    stale = system.model_copy(update={"content_hash": "b" * 64})
    with pytest.raises(ValueError, match="different text"):
        multiref.collect_two({GA: ref_a}, {GA: ref_b}, {GA: stale})


def test_verdict_direction() -> None:
    up = Comparison(0.1, 0.05, 0.2, 0.0)
    assert multiref.verdict("typed_f1_a", up) == "better"
    assert multiref.verdict("invented_union", up) == "worse"
    assert multiref.verdict("typed_f1_a", Comparison(0.1, -0.1, 0.2, 0.3)) == "unclear"


def _write(path: Path, records) -> Path:  # type: ignore[no-untyped-def]
    path.write_text("".join(r.model_dump_json() + "\n" for r in records))
    return path


def test_cli_scores_dev_and_refuses_other_splits(tmp_path: Path) -> None:
    ref_a, ref_b, system = _refs_and_pred()
    a = _write(tmp_path / "a.jsonl", [ref_a])
    b = _write(tmp_path / "b.jsonl", [ref_b])
    p1 = _write(tmp_path / "p1.jsonl", [system.model_copy(update={"model_id": "one"})])
    p2 = _write(
        tmp_path / "p2.jsonl",
        [pred(GA, (cond("p1", (0, 5), U, REQ),), ()).model_copy(update={"model_id": "two"})],
    )
    out = tmp_path / "r.md"
    common = ["--clusters", "document", "--samples", "20", "--out", str(out)]
    dev = write_split_manifest(tmp_path / "dev.json", {GA: "dev"})
    assert (
        main(["multiref", str(a), str(b), str(p1), str(p2), "--split-manifest", str(dev), *common])
        == 0
    )
    report = out.read_text()
    assert "| Typed F1 vs reference A | 0.333 [" in report
    assert "## `two` minus `one` (paired)" in report
    assert "- Consensus conditions (identical in A and B): 1" in report
    test = write_split_manifest(tmp_path / "test.json", {GA: "test"})
    with pytest.raises(SystemExit, match="dev split only"):
        main(["multiref", str(a), str(b), str(p1), "--split-manifest", str(test), *common])
    with pytest.raises(SystemExit, match="different model"):
        main(["multiref", str(a), str(b), str(p1), str(p1), "--split-manifest", str(dev), *common])
