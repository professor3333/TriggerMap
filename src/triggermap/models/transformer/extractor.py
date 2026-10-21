"""Inference and bundles for the transformer extractor.

Predictions from overlapping windows are merged by canonical source offsets: for a span
seen in several windows, the window where it sits furthest from an edge wins. Overlapping
spans are resolved greedily by confidence, spans never cross a line, and groups are rebuilt
from consecutive-pair predictions as chains.

Bundle layout: ``model.safetensors`` (all weights), ``encoder/`` (encoder config),
``tokenizer/`` and ``metadata.json``. Loading never downloads anything.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import torch
from safetensors.torch import load_file, save_file
from transformers import AutoConfig, AutoModel, AutoTokenizer

from triggermap.models.transformer.data import Window, WindowParams, make_windows
from triggermap.models.transformer.decode import Decoder, Heads
from triggermap.models.transformer.model import ConditionModel
from triggermap.schema.models import Extraction
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument


def pick_device(preference: str = "auto") -> torch.device:
    if preference != "auto":
        return torch.device(preference)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def _collate(windows: Sequence[Window], device: torch.device, pad_id: int) -> dict[str, Any]:
    width = max(len(w.input_ids) for w in windows)

    def pad(rows: list[list[int]], value: int) -> torch.Tensor:
        return torch.tensor([r + [value] * (width - len(r)) for r in rows], device=device)

    batch: dict[str, Any] = {
        "input_ids": pad([w.input_ids for w in windows], pad_id),
        "attention_mask": pad([w.attention_mask for w in windows], 0),
    }
    if all(w.token_type_ids is not None for w in windows):
        batch["token_type_ids"] = pad([w.token_type_ids or [] for w in windows], 0)
    if all(w.bio for w in windows):
        batch["bio"] = pad([w.bio for w in windows], -100)
        batch["spans"] = [w.spans for w in windows]
        batch["pairs"] = [w.pairs for w in windows]
    return batch


class TransformerExtractor:
    def __init__(
        self,
        model: ConditionModel,
        tokenizer: Any,
        metadata: dict[str, Any],
        device: torch.device,
        batch_size: int = 8,
    ) -> None:
        self.model = model.to(device).eval()
        self.tokenizer = tokenizer
        self.metadata = metadata
        self.model_id = str(metadata["model_id"])
        self.device = device
        self.batch_size = batch_size
        self.params = WindowParams(**metadata["window"])
        self.directory: Path | None = None  # set once the bundle is saved or loaded

    # -- bundles

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        state = {k: v.detach().cpu().contiguous() for k, v in self.model.state_dict().items()}
        save_file(state, str(directory / "model.safetensors"))
        self.model.encoder.config.save_pretrained(directory / "encoder")
        self.tokenizer.save_pretrained(directory / "tokenizer")
        (directory / "metadata.json").write_text(
            json.dumps(self.metadata, indent=2, sort_keys=True)
        )
        self.directory = directory

    @classmethod
    def load(cls, directory: Path, device: str = "auto") -> TransformerExtractor:
        metadata = json.loads((directory / "metadata.json").read_text())
        if metadata["preprocessing_version"] != PREPROCESSING_VERSION:
            raise ValueError(
                f"bundle built for preprocessing {metadata['preprocessing_version']}, "
                f"running {PREPROCESSING_VERSION}"
            )
        config = AutoConfig.from_pretrained(directory / "encoder")
        model = ConditionModel(AutoModel.from_config(config))
        model.load_state_dict(load_file(str(directory / "model.safetensors")))
        tokenizer = AutoTokenizer.from_pretrained(directory / "tokenizer")
        extractor = cls(model, tokenizer, metadata, pick_device(device))
        extractor.directory = directory
        return extractor

    # -- inference

    def heads(self) -> Heads:
        """Current head weights as NumPy arrays (read each call: training updates them)."""
        return Heads.from_state(
            {
                name: tensor.detach().float().cpu().numpy()
                for name, tensor in self.model.state_dict().items()
                if name.split(".")[0] in Heads.NAMES
            }
        )

    @torch.no_grad()
    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction:
        windows = make_windows(doc, self.tokenizer, self.params)
        decoder = Decoder(doc, self.heads())
        pad_id = int(self.tokenizer.pad_token_id or 0)
        for start in range(0, len(windows), self.batch_size):
            chunk = windows[start : start + self.batch_size]
            batch = _collate(chunk, self.device, pad_id)
            hidden = self.model.encode(
                batch["input_ids"], batch["attention_mask"], batch.get("token_type_ids")
            )
            probs = self.model.bio_logits(hidden).softmax(-1).float().cpu().numpy()
            states = hidden.float().cpu().numpy()
            for b, window in enumerate(chunk):
                decoder.add(window, states[b], probs[b])
        return decoder.extraction(self.model_id, advisory_id)
