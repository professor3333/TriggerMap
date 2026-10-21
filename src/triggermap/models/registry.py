"""One way to obtain any extraction system by name."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from triggermap.schema.models import Extraction
from triggermap.text.preprocessing import PreprocessedDocument

KINDS = ("rules", "crf", "transformer", "onnx")


class Extractor(Protocol):
    model_id: str

    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction: ...


def load_extractor(kind: str, model_dir: Path | None = None, device: str = "auto") -> Extractor:
    if kind == "rules":
        from triggermap.models.rules.extractor import RuleExtractor

        return RuleExtractor()
    if model_dir is None:
        raise ValueError(f"--model {kind} needs --model-dir")
    if kind == "crf":
        from triggermap.models.crf.model import CrfExtractor

        return CrfExtractor.load(model_dir)
    if kind == "transformer":
        from triggermap.models.transformer.extractor import TransformerExtractor

        return TransformerExtractor.load(model_dir, device=device)
    if kind == "onnx":
        from triggermap.models.transformer.onnx_bundle import OnnxExtractor

        return OnnxExtractor.load(model_dir)
    raise ValueError(f"unknown model kind {kind!r}; expected one of {KINDS}")
