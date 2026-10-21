from itertools import pairwise
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("transformers")

from transformers import AutoTokenizer  # noqa: E402

from tests.synthetic import TRAIN_VOCAB, make_dataset  # noqa: E402
from tests.tiny_transformer import build_tiny_base  # noqa: E402
from triggermap.models.transformer.data import (  # noqa: E402
    WindowParams,
    decode_bio,
    make_windows,
    normalize_offset,
)
from triggermap.models.transformer.extractor import TransformerExtractor  # noqa: E402
from triggermap.models.transformer.train import TrainConfig, train  # noqa: E402
from triggermap.schema import validate_annotation  # noqa: E402
from triggermap.text.preprocessing import preprocess  # noqa: E402

DATA = make_dataset(24, TRAIN_VOCAB, seed=1, prefix="train")


@pytest.fixture(scope="module")
def base(tmp_path_factory: pytest.TempPathFactory) -> Path:
    corpus = [pre.text for _, pre, _ in DATA] * 5
    corpus.append("### Impact\nAffected deployments must:\n- use X\n- use Y")
    return build_tiny_base(tmp_path_factory.mktemp("tiny"), corpus)


def test_offset_normalisation_strips_sentencepiece_spaces() -> None:
    text = "When follow_symlinks is set"
    assert normalize_offset(text, 4, 20) == (5, 20)  # " follow_symlinks" -> "follow_symlinks"
    assert normalize_offset(text, 4, 5) is None


def test_decode_bio() -> None:
    assert decode_bio([-100, 1, 2, 0, 2, 2, 1, -100, 2]) == [(1, 2), (4, 5), (6, 6), (8, 8)]


def test_windows_cover_long_documents_and_labels_round_trip(base: Path) -> None:
    tokenizer = AutoTokenizer.from_pretrained(base)
    _, pre, record = DATA[0]
    long_text = "\n\n".join([pre.text] * 12)
    doc = preprocess(long_text)
    shift = len(pre.text) + 2
    from triggermap.schema import AdvisoryAnnotation, Condition

    conditions = tuple(
        Condition(
            id=f"c{k * 10 + i}",
            span=(c.span[0] + k * shift, c.span[1] + k * shift),
            category=c.category,
            role=c.role,
        )
        for k in range(12)
        for i, c in enumerate(record.conditions)
    )
    long_record = AdvisoryAnnotation(
        **{
            **record.model_dump(),
            "content_hash": doc.content_hash,
            "conditions": conditions,
            "groups": (),
        }
    )
    params = WindowParams(max_length=64, stride=12, context_tokens=8)
    windows = make_windows(doc, tokenizer, params, long_record)
    assert len(windows) > 3
    for left, right in pairwise(windows):
        assert right.char_start < left.char_end  # windows overlap
    assert windows[0].char_start == 0 and windows[-1].char_end == len(doc.text.rstrip())
    recovered = set()
    for window in windows:
        assert len(window.input_ids) <= params.max_length
        for first, last in decode_bio(window.bio):
            start, end = window.offsets[first], window.offsets[last]
            assert start is not None and end is not None
            recovered.add((start[0], end[1]))
        assert window.unreachable == 0
    assert recovered == {c.span for c in conditions}


def test_context_is_prepended_inside_lists(base: Path) -> None:
    tokenizer = AutoTokenizer.from_pretrained(base)
    doc = preprocess("### Impact\nAffected deployments must:\n- use X\n- use Y")
    start = doc.text.index("use Y")
    from triggermap.models.transformer.data import encode_window

    with_ctx = encode_window(doc, tokenizer, (start, len(doc.text)), WindowParams(64, 8, 32))
    without = encode_window(doc, tokenizer, (start, len(doc.text)), WindowParams(64, 8, 32, False))
    assert len(with_ctx.input_ids) > len(without.input_ids)
    assert sum(o is not None for o in with_ctx.offsets) == sum(
        o is not None for o in without.offsets
    )


def config(base: Path, **overrides: object) -> TrainConfig:
    settings: dict[str, object] = {
        "model_id": "tiny-test",
        "base_model": str(base),
        "max_length": 96,
        "stride": 16,
        "context_tokens": 16,
        "learning_rate": 5e-3,
        "epochs": 30,
        "batch_size": 8,
        "gradient_accumulation": 1,
        "patience": 30,
        "device": "cpu",
    }
    settings.update(overrides)
    return TrainConfig(**settings)  # type: ignore[arg-type]


@pytest.fixture(scope="module")
def trained(base: Path, tmp_path_factory: pytest.TempPathFactory) -> TransformerExtractor:
    examples = [(pre, rec) for _, pre, rec in DATA]
    return train(config(base), examples, examples, tmp_path_factory.mktemp("bundle"))


def test_pipeline_can_overfit_training_data(trained: TransformerExtractor) -> None:
    """If labels, offsets, decoding or heads were misaligned this could not reach 1.0."""
    assert trained.metadata["best_dev_typed_f1"] == 1.0
    last = trained.metadata["epochs"][-1]["dev"]
    assert last["group_f1"] == 1.0
    for _, pre, rec in DATA[:6]:
        extraction = trained.extract(pre, rec.advisory_id)
        assert validate_annotation(extraction, pre.text) == []
        assert {c.span for c in extraction.conditions} == {c.span for c in rec.conditions}


def test_metadata_records_provenance(trained: TransformerExtractor) -> None:
    meta = trained.metadata
    assert meta["family"] == "transformer"
    assert meta["training_documents"] == len(DATA)
    assert len(meta["training_hash"]) == 64
    assert meta["unreachable_spans"] == 0
    assert meta["window"]["use_context"] is True
    assert meta["device"] == "cpu"


def test_bundle_round_trip(trained: TransformerExtractor) -> None:
    assert trained.directory is not None
    reloaded = TransformerExtractor.load(trained.directory, device="cpu")
    for _, pre, rec in DATA[:4]:
        assert reloaded.extract(pre, rec.advisory_id) == trained.extract(pre, rec.advisory_id)


def test_ablations_train(base: Path, tmp_path: Path) -> None:
    examples = [(pre, rec) for _, pre, rec in DATA[:8]]
    ablated = config(base, epochs=1, use_context=False, group_loss_weight=0.0)
    model = train(ablated, examples, [], tmp_path)
    assert model.metadata["window"]["use_context"] is False
    assert model.metadata["best_dev_typed_f1"] is None
    small = config(base, epochs=1, max_train_documents=3)
    assert train(small, examples, [], tmp_path / "lc").metadata["training_documents"] == 3


def test_committed_experiment_configs_are_valid() -> None:
    import tomllib

    from triggermap.models.experiment import plan

    root = Path(__file__).resolve().parents[1] / "configs/experiments"
    counts = {}
    for path in sorted(root.glob("*.toml")):
        runs = plan(tomllib.loads(path.read_text()))
        for run in runs:
            TrainConfig(**run.settings)  # extra="forbid": typos fail here
        assert len({r.name for r in runs}) == len(runs)
        counts[path.stem] = len(runs)
    assert counts == {"ablations": 15, "deberta": 6, "distilbert": 6}


def test_cli_train_predict_and_experiment(base: Path, tmp_path: Path) -> None:
    import json

    from tests.factories import write_split_manifest
    from triggermap.cli import main
    from triggermap.schema import Extraction

    data = DATA[:16]
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "advisories.jsonl").write_text(
        "".join(d.model_dump_json() + "\n" for d, _, _ in data)
    )
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(r.model_dump_json() + "\n" for _, _, r in data))
    split = write_split_manifest(
        tmp_path / "split.json",
        {r.advisory_id: ("train" if i < 12 else "dev") for i, (_, _, r) in enumerate(data)},
    )
    config = tmp_path / "tiny.toml"
    config.write_text(
        f"""
[train]
model_id = "tiny"
base_model = "{base}"
max_length = 96
stride = 16
context_tokens = 16
learning_rate = 5e-3
epochs = 2
batch_size = 8
gradient_accumulation = 1
device = "cpu"

[grid]
seed = [0, 1]
"""
    )
    common = ["--processed", str(processed), "--split-manifest", str(split)]
    bundle = tmp_path / "bundle"
    train_args = ["train", "--model", "transformer", "--config", str(config), "--gold", str(gold)]
    assert main([*train_args, "--out", str(bundle), *common]) == 0
    meta = json.loads((bundle / "metadata.json").read_text())
    assert meta["training_documents"] == 12 and meta["split_assignment_sha256"]
    preds = tmp_path / "preds.jsonl"
    predict_args = ["predict", "--model", "transformer", "--model-dir", str(bundle)]
    assert main([*predict_args, "--out", str(preds), "--processed", str(processed)]) == 0
    assert len([Extraction.model_validate_json(x) for x in preds.read_text().splitlines()]) == 16
    report = tmp_path / "report.md"
    experiment_args = ["experiment", "--config", str(config), "--gold", str(gold)]
    experiment_args += ["--out-root", str(tmp_path / "runs"), "--report", str(report)]
    assert main([*experiment_args, "--samples", "20", *common]) == 0
    text = report.read_text()
    assert "tiny-base-seed0" in text and "tiny-base-seed1" in text
    assert "## Across seeds (typed F1)" in text
    # Resume: a second invocation reuses both finished bundles instead of retraining.
    assert main([*experiment_args, "--samples", "20", *common]) == 0
    assert report.read_text().count("tiny-base-seed") == text.count("tiny-base-seed")


@pytest.mark.slow
@pytest.mark.parametrize(
    "name, revision",
    [
        ("distilbert/distilbert-base-cased", "6ea81172465e8b0ad3fddeed32b986cdcdcffcf0"),
        ("microsoft/deberta-v3-small", "a36c739020e01763fe789b4b85e2df55d6180012"),
    ],
)
def test_real_checkpoint_windows_and_training_step(
    name: str, revision: str, aiohttp_advisory: dict[str, str], tmp_path: Path
) -> None:
    """Downloads the real base model: offsets, windows and one optimisation step."""
    from triggermap.schema import AdvisoryAnnotation, Category, Condition, DocumentStatus, Role
    from triggermap.text.preprocessing import compose_raw

    doc = preprocess(compose_raw(aiohttp_advisory["summary"], aiohttp_advisory["details"]))
    surface = "follow_symlinks set to True"
    start = doc.text.index(surface)
    record = AdvisoryAnnotation(
        advisory_id="GHSA-5h86-8mv2-jq9f",
        source_commit="c" * 40,
        content_hash=doc.content_hash,
        preprocessing_version=doc.version,
        annotation_version="smoke",
        document_status=DocumentStatus.HAS_CONDITIONS,
        conditions=(
            Condition(
                id="c1",
                span=(start, start + len(surface)),
                category=Category.CONFIGURATION,
                role=Role.REQUIRED,
            ),
        ),
    )
    tokenizer = AutoTokenizer.from_pretrained(name, revision=revision)
    windows = make_windows(doc, tokenizer, WindowParams(max_length=256, stride=32), record)
    assert sum(w.unreachable for w in windows) == 0
    assert any(len(w.spans) == 1 for w in windows)
    cfg = TrainConfig(
        model_id="smoke",
        base_model=name,
        revision=revision,
        max_length=256,
        stride=32,
        epochs=1,
        batch_size=2,
        gradient_accumulation=1,
        device="cpu",
    )
    model = train(cfg, [(doc, record)], [(doc, record)], tmp_path)
    assert model.metadata["base_revision"] == revision
    assert validate_annotation(model.extract(doc, record.advisory_id), doc.text) == []


def test_cli_model_kinds_match_registry() -> None:
    from triggermap.cli import MODEL_KINDS
    from triggermap.models.registry import KINDS

    assert MODEL_KINDS == KINDS


def test_onnx_export_and_int8_parity(trained: TransformerExtractor, tmp_path: Path) -> None:
    pytest.importorskip("onnxruntime")
    from triggermap.models.registry import load_extractor
    from triggermap.models.transformer.onnx_bundle import export_onnx, quantize_int8
    from triggermap.serve.app import weights_digest

    assert trained.directory is not None
    fp32_dir = export_onnx(trained.directory, tmp_path / "onnx")
    int8_dir = quantize_int8(fp32_dir, tmp_path / "int8")
    fp32 = load_extractor("onnx", fp32_dir)
    int8 = load_extractor("onnx", int8_dir)
    assert fp32.model_id == trained.model_id and int8.model_id == f"{trained.model_id}-int8"

    def signature(extraction):  # type: ignore[no-untyped-def]
        conditions = [(c.span, c.category, c.role) for c in extraction.conditions]
        return conditions + [(g.operator, g.members) for g in extraction.groups]

    for _, pre, _ in DATA:
        reference = signature(trained.extract(pre))
        assert signature(fp32.extract(pre)) == reference
        assert signature(int8.extract(pre)) == reference
    assert (int8_dir / "model.int8.onnx").stat().st_size < (fp32_dir / "model.onnx").stat().st_size
    assert weights_digest("onnx", int8_dir) != weights_digest("onnx", fp32_dir)


def test_scope_index_matches_linear_scope_of() -> None:
    from triggermap.models.structure import ScopeIndex, scope_of

    text = (
        "### Impact\nAffected deployments must:\n- use X; and\n- use Y\n\n"
        "When debug is on and the proxy caches pages, data leaks. Another sentence here."
    )
    doc = preprocess(text)
    index = ScopeIndex(doc)
    for start in range(len(doc.text)):
        span = (start, min(start + 3, len(doc.text)))
        assert index.scope(span) == scope_of(doc, span)
