from collections import Counter
from pathlib import Path

import pytest

from triggermap.eval.errors import SEVERITY, classify, render
from triggermap.schema import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import preprocess

TEXT = (
    "Exposure requires using the admin API and enabling uploads. "
    "It happens even when symlinks are not present. "
    "Attackers can read files. Debug mode must be on. The proxy caches pages."
)
DOC = preprocess(TEXT)


def span(surface: str) -> tuple[int, int]:
    start = DOC.text.index(surface)
    return start, start + len(surface)


def cond(cid: str, surface: str, cat: Category, role: Role) -> Condition:
    return Condition(id=cid, span=span(surface), category=cat, role=role)


def extraction(conditions: tuple[Condition, ...], groups: tuple[Group, ...] = ()) -> Extraction:
    return Extraction(
        content_hash=DOC.content_hash,
        preprocessing_version="1",
        model_id="m",
        document_status=DocumentStatus.HAS_CONDITIONS,
        conditions=conditions,
        groups=groups,
    )


U, C, P, A = Category.USAGE, Category.CONFIGURATION, Category.PLATFORM, Category.ACCESS
REQ, NOT = Role.REQUIRED, Role.NOT_REQUIRED

GOLD = extraction(
    (
        cond("g1", "using the admin API", U, REQ),
        cond("g2", "enabling uploads", U, REQ),
        cond("g3", "symlinks", P, NOT),
        cond("g4", "Debug mode must be on", C, REQ),
        cond("g5", "The proxy caches pages", P, REQ),
    ),
    (Group(operator=GroupOperator.ALL, members=("g1", "g2")),),
)
PRED = extraction(
    (
        cond("p1", "using the admin API", A, REQ),  # category error
        cond("p2", "enabling uploads", U, REQ),  # correct, but grouped ANY
        cond("p3", "symlinks", P, REQ),  # reversed meaning
        cond("p4", "Attackers can read files", A, REQ),  # invented prerequisite
        cond("p5", "Debug mode", C, REQ),  # boundary error
    ),
    (Group(operator=GroupOperator.ANY, members=("p1", "p2")),),
)


def test_every_error_type_is_classified() -> None:
    entries = classify("GHSA-2222-2222-2222", DOC, GOLD, PRED)
    kinds = sorted(e.kind for e in entries)
    assert kinds == sorted(
        [
            "category_error",
            "reversed_meaning",
            "invented_prerequisite",
            "boundary_error",
            "missed_condition",
            "group_error",
        ]
    )
    reversed_ = next(e for e in entries if e.kind == "reversed_meaning")
    assert reversed_.gold == 'PLATFORM/NOT_REQUIRED "symlinks"'
    assert reversed_.predicted == 'PLATFORM/REQUIRED "symlinks"'
    assert "«symlinks»" in reversed_.excerpt
    group = next(e for e in entries if e.kind == "group_error")
    assert (group.gold, group.predicted) == ("ALL of 2", "ANY")


def test_missing_prediction_misses_everything_and_perfect_has_no_errors() -> None:
    missed = classify("x", DOC, GOLD, None)
    assert Counter(e.kind for e in missed) == {"missed_condition": 5, "group_error": 1}
    assert classify("x", DOC, GOLD, GOLD) == []


def Counter_of(entries):  # type: ignore[no-untyped-def]
    from collections import Counter

    return dict(Counter(e.kind for e in entries))


def test_render_orders_by_severity_and_escapes(tmp_path: Path) -> None:
    entries = classify("GHSA-2222-2222-2222", DOC, GOLD, PRED)
    report = render("Errors", entries, 1, {"Split": "dev"})
    positions = [report.index(f"## {kind}") for kind in SEVERITY if f"## {kind}" in report]
    assert positions == sorted(positions)
    assert report.index("## reversed_meaning") < report.index("## invented_prerequisite")
    assert "| reversed_meaning | 1 |" in report


def _errors_inputs(tmp_path: Path, manual: int, split_name: str = "dev") -> list[str]:
    """Errors arguments over 6 records in one split, the first `manual` of them hand-labelled."""
    from tests.factories import write_split_manifest
    from tests.synthetic import TRAIN_VOCAB, make_dataset
    from triggermap.ingest.build import CORPUS_FILE
    from triggermap.models.rules.extractor import RuleExtractor
    from triggermap.schema import AnnotationOrigin

    data = make_dataset(6, TRAIN_VOCAB, seed=3, prefix="train")
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / CORPUS_FILE).write_text("".join(d.model_dump_json() + "\n" for d, _, _ in data))
    records = [
        r.model_copy(
            update={
                "origin": (
                    AnnotationOrigin.MANUAL if i < manual else AnnotationOrigin.MODEL_DRAFT_ACCEPTED
                )
            }
        )
        for i, (_, _, r) in enumerate(data)
    ]
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(r.model_dump_json() + "\n" for r in records))
    pred = tmp_path / "pred.jsonl"
    extractor = RuleExtractor()
    pred.write_text(
        "".join(extractor.extract(p, r.advisory_id).model_dump_json() + "\n" for _, p, r in data)
    )
    split = write_split_manifest(
        tmp_path / "split.json", {r.advisory_id: split_name for _, _, r in data}
    )
    return [
        "errors",
        "--gold",
        str(gold),
        "--pred",
        str(pred),
        "--split-manifest",
        str(split),
        "--processed",
        str(processed),
        "--split",
        split_name,
    ]


def test_errors_uses_only_hand_labelled_gold_by_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from triggermap.cli import main

    out = tmp_path / "errors.md"
    assert main([*_errors_inputs(tmp_path, manual=2), "--out", str(out)]) == 0
    assert "in 2 documents" in capsys.readouterr().out
    assert "manual" in out.read_text()


def test_errors_refuses_model_drafts_unless_asked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from triggermap.cli import main

    out = tmp_path / "errors.md"
    args = _errors_inputs(tmp_path, manual=0)
    with pytest.raises(SystemExit, match="origin 'manual'"):
        main([*args, "--out", str(out)])
    assert not out.exists()
    assert main([*args, "--gold-origin", "all", "--out", str(out)]) == 0
    assert "in 6 documents" in capsys.readouterr().out


def test_errors_without_manual_test_gold_logs_no_test_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import triggermap.cli as cli

    log = tmp_path / "access-log.md"
    monkeypatch.setattr(cli, "TEST_ACCESS_LOG", log)
    args = _errors_inputs(tmp_path, manual=0, split_name="test")
    with pytest.raises(SystemExit, match="origin 'manual'"):
        cli.main([*args, "--release-evaluation", "check", "--out", str(tmp_path / "e.md")])
    assert not log.exists()
