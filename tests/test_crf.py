import json
from pathlib import Path

import pytest

from tests.synthetic import TEST_VOCAB, TRAIN_VOCAB, make_dataset
from triggermap.eval.metrics import collect, summary
from triggermap.models.crf.model import CrfExtractor
from triggermap.models.crf.tokens import (
    Token,
    bio_tags,
    spans_from_tags,
    split_at_lines,
    tokenize,
)
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
    from tests.factories import write_split_manifest

    split = write_split_manifest(
        tmp_path / "split.json",
        {rec.advisory_id: ("train" if i < 15 else "dev") for i, (_, _, rec) in enumerate(data)},
    )
    common = ["--processed", str(processed)]
    train_args = ["--gold", str(gold), "--out", str(bundle), "--split-manifest", str(split)]
    assert main(["train", *train_args, "--no-pos", *common]) == 0
    assert json.loads((bundle / "metadata.json").read_text())["training_documents"] == 15
    assert (bundle / "tagger.crfsuite").exists() and (bundle / "metadata.json").exists()
    args = ["predict", "--model", "crf", "--model-dir", str(bundle), "--out", str(preds)]
    assert main([*args, *common]) == 0
    lines = preds.read_text().splitlines()
    assert len(lines) == 20
    assert all(Extraction.model_validate_json(line).model_id == "crf-1" for line in lines)


def test_train_origin_filter_is_recorded(tmp_path: Path) -> None:
    from tests.factories import write_split_manifest
    from triggermap.cli import main
    from triggermap.schema import AnnotationOrigin

    data = make_dataset(20, TRAIN_VOCAB, seed=7, prefix="org")
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "advisories.jsonl").write_text(
        "".join(doc.model_dump_json() + "\n" for doc, _, _ in data)
    )
    origins = [AnnotationOrigin.MANUAL] * 12 + [AnnotationOrigin.MODEL_DRAFT_ACCEPTED] * 8
    gold = tmp_path / "gold.jsonl"
    gold.write_text(
        "".join(
            rec.model_copy(update={"origin": o}).model_dump_json() + "\n"
            for (_, _, rec), o in zip(data, origins, strict=True)
        )
    )
    split = write_split_manifest(
        tmp_path / "split.json", {rec.advisory_id: "train" for _, _, rec in data}
    )
    common = ["--gold", str(gold), "--split-manifest", str(split), "--processed", str(processed)]
    meta = {}
    for name, extra in (("all", []), ("manual", ["--origin", "manual"])):
        bundle = tmp_path / name
        assert main(["train", *common, "--out", str(bundle), "--no-pos", *extra]) == 0
        meta[name] = json.loads((bundle / "metadata.json").read_text())
    assert meta["all"]["training_origins"] == {"manual": 12, "model_draft_accepted": 8}
    assert meta["manual"]["training_origins"] == {"manual": 12}
    assert meta["manual"]["training_documents"] == 12
    with pytest.raises(SystemExit, match="--origin"):
        main(["train", *common, "--out", str(tmp_path / "x"), "--origin", "model_draft_edited"])


def test_tagged_ranges_are_split_at_line_breaks() -> None:
    """A tagged run that continues onto the next line becomes one condition per line."""
    text = "uses the legacy API\nwith debug enabled"
    tokens = tokenize(text)
    assert split_at_lines(text, tokens, 0, len(tokens)) == [(0, 4), (4, 7)]
    assert split_at_lines(text, tokens, 1, 3) == [(1, 3)]
    pieces = [
        text[tokens[a].start : tokens[b - 1].end] for a, b in split_at_lines(text, tokens, 0, 7)
    ]
    assert pieces == ["uses the legacy API", "with debug enabled"]


def test_context_ablation_drops_context_features(tmp_path: Path) -> None:
    from triggermap.models.crf.features import sentence_context, token_features

    data = make_dataset(12, TRAIN_VOCAB, seed=7, prefix="ctx")
    _, pre, rec = data[0]
    sentence = pre.sentences[0]
    tokens = tokenize(pre.text, sentence.start, sentence.end)
    ctx = sentence_context(pre, sentence)
    assert "block" in token_features(pre, tokens, ctx, None)[0]
    assert "block" not in token_features(pre, tokens, ctx, None, use_context=False)[0]

    model = CrfExtractor.train(
        [(p, r) for _, p, r in data], tmp_path / "b", use_pos=False, use_context=False
    )
    assert model.metadata["use_context"] is False
    reloaded = CrfExtractor.load(model.directory)
    assert reloaded.use_context is False
    assert reloaded.extract(pre, rec.advisory_id) == model.extract(pre, rec.advisory_id)

    # Bundles written before the ablation existed have no use_context key: context was on.
    meta = json.loads((model.directory / "metadata.json").read_text())
    del meta["use_context"]
    (model.directory / "metadata.json").write_text(json.dumps(meta))
    assert CrfExtractor.load(model.directory).use_context is True


def test_training_budget_is_a_seeded_subset(tmp_path: Path) -> None:
    examples = [(p, r) for _, p, r in make_dataset(20, TRAIN_VOCAB, seed=8, prefix="lc")]

    def hash_of(seed: int, name: str) -> str:
        model = CrfExtractor.train(
            examples, tmp_path / name, use_pos=False, max_train_documents=8, seed=seed
        )
        assert model.metadata["training_documents"] == 8
        assert model.metadata["hyperparameters"]["max_train_documents"] == 8
        return str(model.metadata["training_hash"])

    assert hash_of(0, "a") == hash_of(0, "b")
    assert hash_of(0, "a") != hash_of(1, "c")


def test_crf_settings_reject_unknown_keys() -> None:
    from triggermap.models.experiment import crf_settings

    settings = {"family": "crf", "model_id": "m", "use_context": False}
    assert crf_settings(settings) == {"model_id": "m", "use_context": False}
    with pytest.raises(ValueError, match="use_contxt"):
        crf_settings({"model_id": "m", "use_contxt": False})


def test_crf_experiment_cli(tmp_path: Path) -> None:
    from tests.factories import write_split_manifest
    from triggermap.cli import main

    data = make_dataset(24, TRAIN_VOCAB, seed=9, prefix="exp")
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "advisories.jsonl").write_text(
        "".join(doc.model_dump_json() + "\n" for doc, _, _ in data)
    )
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(rec.model_dump_json() + "\n" for _, _, rec in data))
    split = write_split_manifest(
        tmp_path / "split.json",
        {rec.advisory_id: ("train" if i < 16 else "dev") for i, (_, _, rec) in enumerate(data)},
    )
    config = tmp_path / "crf.toml"
    config.write_text(
        '[train]\nfamily = "crf"\nmodel_id = "c"\nuse_pos = false\n\n'
        '[[runs]]\nname = "full"\n\n[[runs]]\nname = "no-context"\nuse_context = false\n\n'
        '[[runs]]\nname = "docs8-seed0"\nmax_train_documents = 8\n'
    )
    report = tmp_path / "report.md"
    args = ["experiment", "--config", str(config), "--gold", str(gold), "--samples", "20"]
    args += ["--out-root", str(tmp_path / "runs"), "--report", str(report)]
    args += ["--processed", str(processed), "--split-manifest", str(split)]
    assert main(args) == 0
    text = report.read_text()
    assert "| c-full | 16 |" in text and "| c-docs8-seed0 | 8 |" in text
    assert (
        json.loads((tmp_path / "runs/c-no-context/metadata.json").read_text())["use_context"]
        is False
    )
    assert "train_seconds" not in (tmp_path / "runs/c-full/metadata.json").read_text()
    assert main(args) == 0  # resume reuses the bundles
