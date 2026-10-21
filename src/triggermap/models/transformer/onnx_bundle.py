"""ONNX export, dynamic INT8 quantization and a PyTorch-free ONNX Runtime extractor.

The exported graph is the encoder plus the BIO head: inputs are token ids and attention
mask (and token types when the encoder uses them); outputs are hidden states and BIO logits,
with dynamic batch and sequence axes. The category, role and group heads stay outside the
graph as NumPy weights (``heads.npz``) and run in the shared decoder, so ONNX and PyTorch
predictions go through identical decoding.

ONNX bundle layout: ``model.onnx`` (or ``model.int8.onnx``), ``heads.npz``, ``tokenizer/``,
``metadata.json`` (adds ``runtime`` and the source bundle's weights digest).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

import numpy as np

from triggermap.models.transformer.data import WindowParams, make_windows
from triggermap.models.transformer.decode import Decoder, Heads, collate, softmax
from triggermap.schema.models import Extraction
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument

ONNX_FILES = ("model.onnx", "model.int8.onnx")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_onnx(bundle: Path, out_dir: Path, opset: int = 18) -> Path:
    """Export a PyTorch transformer bundle to an ONNX bundle (float32)."""
    import torch

    from triggermap.models.transformer.extractor import TransformerExtractor

    source = TransformerExtractor.load(bundle, device="cpu")
    model = source.model.eval()
    # Eager attention traces cleanly; SDPA paths freeze shape-dependent values when traced.
    model.encoder.config._attn_implementation = "eager"
    uses_token_types = model._uses_token_types

    class EncoderAndBio(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.inner = model

        def forward(self, *inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
            token_types = inputs[2] if uses_token_types else None
            hidden = self.inner.encode(inputs[0], inputs[1], token_types)
            return hidden, self.inner.bio_logits(hidden)

    names = ["input_ids", "attention_mask"] + (["token_type_ids"] if uses_token_types else [])
    example = tuple(torch.ones((2, 16), dtype=torch.long) for _ in names)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "model.onnx"
    dynamic = {name: {0: "batch", 1: "sequence"} for name in names}
    torch.onnx.export(
        EncoderAndBio(),
        example,
        str(target),
        input_names=names,
        output_names=["hidden", "bio_logits"],
        dynamic_axes={
            **dynamic,
            "hidden": {0: "batch", 1: "sequence"},
            "bio_logits": {0: "batch", 1: "sequence"},
        },
        opset_version=opset,
        dynamo=False,
    )
    save_arrays: Any = np.savez  # numpy's stub mistypes **arrays as the allow_pickle flag
    save_arrays(out_dir / "heads.npz", **source.heads().arrays())
    source.tokenizer.save_pretrained(out_dir / "tokenizer")
    metadata = dict(source.metadata)
    metadata.update(
        {
            "runtime": "onnx-fp32",
            "onnx_inputs": names,
            "onnx_opset": opset,
            "source_weights_sha256": _sha256(bundle / "model.safetensors"),
        }
    )
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True))
    return out_dir


def quantize_int8(onnx_dir: Path, out_dir: Path) -> Path:
    """Dynamic INT8 quantization of the exported graph (weights int8, activations dynamic)."""
    from onnxruntime.quantization import QuantType, quantize_dynamic

    out_dir.mkdir(parents=True, exist_ok=True)
    quantize_dynamic(
        str(onnx_dir / "model.onnx"),
        str(out_dir / "model.int8.onnx"),
        weight_type=QuantType.QInt8,
    )
    for name in ("heads.npz",):
        shutil.copy2(onnx_dir / name, out_dir / name)
    shutil.copytree(onnx_dir / "tokenizer", out_dir / "tokenizer", dirs_exist_ok=True)
    metadata = json.loads((onnx_dir / "metadata.json").read_text())
    metadata["runtime"] = "onnx-int8"
    metadata["model_id"] = f"{metadata['model_id']}-int8"
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True))
    return out_dir


class OnnxExtractor:
    """Transformer extractor on ONNX Runtime (CPU); imports no PyTorch."""

    def __init__(self, directory: Path, threads: int | None = None, batch_size: int = 8) -> None:
        import onnxruntime as ort
        from transformers import AutoTokenizer

        self.directory = directory
        self.metadata: dict[str, Any] = json.loads((directory / "metadata.json").read_text())
        if self.metadata["preprocessing_version"] != PREPROCESSING_VERSION:
            raise ValueError("ONNX bundle built for a different preprocessing version")
        self.model_id = str(self.metadata["model_id"])
        self.params = WindowParams(**self.metadata["window"])
        self.batch_size = batch_size
        model_file = next(directory / f for f in ONNX_FILES if (directory / f).exists())
        options = ort.SessionOptions()
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        if threads is not None:
            options.intra_op_num_threads = threads
            options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(
            str(model_file), options, providers=["CPUExecutionProvider"]
        )
        self.inputs = [i.name for i in self.session.get_inputs()]
        heads = np.load(directory / "heads.npz")
        self._heads = Heads.from_state({name: heads[name] for name in heads.files})
        self.tokenizer = AutoTokenizer.from_pretrained(directory / "tokenizer")

    @classmethod
    def load(cls, directory: Path, threads: int | None = None) -> OnnxExtractor:
        return cls(directory, threads)

    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction:
        windows = make_windows(doc, self.tokenizer, self.params)
        decoder = Decoder(doc, self._heads)
        pad_id = int(self.tokenizer.pad_token_id or 0)
        for start in range(0, len(windows), self.batch_size):
            chunk = windows[start : start + self.batch_size]
            batch = collate(chunk, pad_id)
            if "token_type_ids" in self.inputs and "token_type_ids" not in batch:
                batch["token_type_ids"] = np.zeros_like(batch["input_ids"])  # PyTorch's default
            hidden, logits = self.session.run(
                ["hidden", "bio_logits"], {name: batch[name] for name in self.inputs}
            )
            probs = softmax(logits)
            for b, window in enumerate(chunk):
                decoder.add(window, hidden[b].astype(np.float32), probs[b])
        return decoder.extraction(self.model_id, advisory_id)
