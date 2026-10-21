"""Latency-only bundles: a pretrained encoder with untrained heads.

Inference cost does not depend on head weights, so these bundles measure the serving cost
of a backbone before any training. They are marked ``untrained_heads`` and can never be
released or used for evaluation.
"""

from __future__ import annotations

from pathlib import Path

from triggermap.models.transformer.data import WindowParams
from triggermap.text.preprocessing import PREPROCESSING_VERSION


def build(base_model: str, revision: str | None, out_dir: Path, seed: int = 0) -> Path:
    import torch
    from transformers import AutoModel, AutoTokenizer

    from triggermap.models.transformer.extractor import TransformerExtractor
    from triggermap.models.transformer.model import ConditionModel

    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(base_model, revision=revision)
    encoder = AutoModel.from_pretrained(base_model, revision=revision, dtype=torch.float32)
    window = WindowParams()
    metadata = {
        "model_id": f"{base_model.split('/')[-1]}-untrained-latency",
        "family": "transformer",
        "base_model": base_model,
        "base_revision": getattr(encoder.config, "_commit_hash", None) or revision,
        "preprocessing_version": PREPROCESSING_VERSION,
        "window": {
            "max_length": window.max_length,
            "stride": window.stride,
            "context_tokens": window.context_tokens,
            "use_context": window.use_context,
        },
        "untrained_heads": True,
    }
    extractor = TransformerExtractor(
        ConditionModel(encoder), tokenizer, metadata, torch.device("cpu")
    )
    extractor.save(out_dir)
    return out_dir
