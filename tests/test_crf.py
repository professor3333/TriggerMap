from pathlib import Path

import pytest

from tests.synthetic import TEST_VOCAB, TRAIN_VOCAB, make_dataset
from triggermap.eval.metrics import collect, summary
from triggermap.models.crf.model import CrfExtractor
from triggermap.models.crf.tokens import Token, bio_tags, spans_from_tags, tokenize
from triggermap.schema import validate_annotation


def test_tokenizer_keeps_identifiers_whole() -> None:
    text = "Set 'follow_symlinks'=True on flask.session.permanent via Cache-Control 3.9.2."
    words = [t.text for t in tokenize(text)]
    assert words == [
        "Set", "'", "follow_symlinks", "'", "=", "True", "on", "flask.session.permanent",
        "via", "Cache-Control", "3.9.2", ".",
    ]  # fmt: skip
    assert all(text[t.start : t.end] == t.text for t in tokenize(text))


def test_bio_round_trip_and_unreachable_spans() -> None:
    text = "when follow_symlinks is set to True"
    tokens = tokenize(text)
    tags, unreachable = bio_tags(tokens, [(5, 35), (5, 11)])
    assert unreachable == [(5, 11)]  # "follow" ends inside the token follow_symlinks
    assert tags == ["O", "B", "I", "I", "I", "I"]
    assert spans_from_tags(tokens, tags) == [(1, 6)]
    assert spans_from_tags([Token(0, 1, "a")] * 3, ["I", "O", "B"]) == [(0, 1), (2, 3)]


@pytest.fixture(scope="module")
def trained(tmp_path_factory: pytest.TempPathFactory) -> CrfExtractor:
    train = make_dataset(60, TRAIN_VOCAB, seed=1, prefix="train")
    out = tmp_path_factory.mktemp("crf")
    return CrfExtractor.train([(pre, rec) for _, pre, rec in train], out, use_pos=False)


def test_generalises_to_unseen_vocabulary(trained: CrfExtractor) -> None:
    test = make_dataset(30, TEST_VOCAB, seed=2, prefix="test")
    gold = {rec.advisory_id: rec for _, _, rec in test}
    preds = {}
    for _, pre, rec in test:
        extraction = trained.extract(pre, rec.advisory_id)
        assert validate_annotation(extraction, pre.text) == []
        preds[rec.advisory_id] = extraction
    scores = summary(collect(gold, preds))  # type: ignore[arg-type]
    assert scores["span_f1"] >= 0.9
    assert scores["typed_f1"] >= 0.85
    assert scores["group_f1"] >= 0.8
    assert scores["doc_exact_without_conditions"] == 1.0


def test_metadata_and_reload(trained: CrfExtractor) -> None:
    meta = trained.metadata
    assert meta["family"] == "crf" and meta["use_pos"] is False
    assert meta["stats"]["unreachable_spans"] == 0
    assert set(meta["label_counts"]["role"]) == {"REQUIRED", "EXCEPTION"}
    reloaded = CrfExtractor.load(trained.directory)
    _, pre, rec = make_dataset(1, TEST_VOCAB, seed=5, prefix="x")[0]
    assert reloaded.extract(pre, rec.advisory_id) == trained.extract(pre, rec.advisory_id)


def test_rejects_annotation_for_other_text(tmp_path: Path) -> None:
    (_, pre, rec), (_, other, _) = make_dataset(2, TRAIN_VOCAB, seed=3, prefix="t")
    if pre.content_hash == other.content_hash:
        pytest.skip("identical synthetic texts")
    with pytest.raises(ValueError, match="different text"):
        CrfExtractor.train([(other, rec)], tmp_path, use_pos=False)


def test_part_of_speech_features(tmp_path: Path) -> None:
    pytest.importorskip("spacy")
    data = make_dataset(12, TRAIN_VOCAB, seed=4, prefix="pos")
    model = CrfExtractor.train([(p, r) for _, p, r in data], tmp_path, use_pos=True)
    assert model.metadata["use_pos"] is True
    _, pre, rec = data[0]
    assert validate_annotation(model.extract(pre, rec.advisory_id), pre.text) == []


def test_train_and_predict_cli(tmp_path: Path) -> None:
    from triggermap.cli import main
    from triggermap.schema import Extraction

    data = make_dataset(20, TRAIN_VOCAB, seed=6, prefix="cli")
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "advisories.jsonl").write_text(
        "".join(doc.model_dump_json() + "\n" for doc, _, _ in data)
    )
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(rec.model_dump_json() + "\n" for _, _, rec in data))
    bundle, preds = tmp_path / "bundle", tmp_path / "preds.jsonl"
    common = ["--processed", str(processed)]
    assert main(["train", "--gold", str(gold), "--out", str(bundle), "--no-pos", *common]) == 0
    assert (bundle / "tagger.crfsuite").exists() and (bundle / "metadata.json").exists()
    args = ["predict", "--model", "crf", "--model-dir", str(bundle), "--out", str(preds)]
    assert main([*args, *common]) == 0
    lines = preds.read_text().splitlines()
    assert len(lines) == 20
    assert all(Extraction.model_validate_json(line).model_id == "crf-1" for line in lines)
