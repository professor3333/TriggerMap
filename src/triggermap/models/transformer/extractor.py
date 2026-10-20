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
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

import torch
from safetensors.torch import load_file, save_file
from transformers import AutoConfig, AutoModel, AutoTokenizer

from triggermap.models.structure import scope_of
from triggermap.models.transformer.data import (
    CATEGORIES,
    GROUP_LABELS,
    ROLES,
    Window,
    WindowParams,
    decode_bio,
    make_windows,
)
from triggermap.models.transformer.model import ConditionModel
from triggermap.schema.models import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument


def pick_device(preference: str = "auto") -> torch.device:
    if preference != "auto":
        return torch.device(preference)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


@dataclass
class _Found:
    span: tuple[int, int]
    confidence: float
    category: int
    role: int
    role_probability: float
    centrality: int  # distance (tokens) to the nearer window edge


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


def _split_lines(text: str, span: tuple[int, int]) -> list[tuple[int, int]]:
    pieces = []
    start = span[0]
    while start < span[1]:
        end = text.find("\n", start, span[1])
        end = span[1] if end < 0 else end
        a, b = start, end
        while a < b and text[a].isspace():
            a += 1
        while b > a and (text[b - 1].isspace() or text[b - 1] in ".,;:"):
            b -= 1
        if b - a >= 2:
            pieces.append((a, b))
        start = end + 1
    return pieces


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

    @torch.no_grad()
    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction:
        windows = make_windows(doc, self.tokenizer, self.params)
        found: dict[tuple[int, int], _Found] = {}
        pair_votes: dict[tuple[tuple[int, int], tuple[int, int]], tuple[int, list[float]]] = {}
        pad_id = int(self.tokenizer.pad_token_id or 0)
        for start in range(0, len(windows), self.batch_size):
            chunk = windows[start : start + self.batch_size]
            batch = _collate(chunk, self.device, pad_id)
            hidden = self.model.encode(
                batch["input_ids"], batch["attention_mask"], batch.get("token_type_ids")
            )
            probs = self.model.bio_logits(hidden).softmax(-1).float().cpu()
            for b, window in enumerate(chunk):
                self._window(doc, window, hidden[b], probs[b], found, pair_votes)
        return self._assemble(doc, advisory_id, found, pair_votes)

    def _window(
        self,
        doc: PreprocessedDocument,
        window: Window,
        hidden: torch.Tensor,
        probs: torch.Tensor,
        found: dict[tuple[int, int], _Found],
        pair_votes: dict[tuple[tuple[int, int], tuple[int, int]], tuple[int, list[float]]],
    ) -> None:
        positions = [i for i, o in enumerate(window.offsets) if o is not None]
        if not positions:
            return
        tags = [
            int(probs[i].argmax()) if offset is not None else -100
            for i, offset in enumerate(window.offsets)
        ]
        ranges = decode_bio(tags)
        if not ranges:
            return
        category_logits, role_logits = self.model.attribute_logits(hidden, ranges)
        category_p = category_logits.softmax(-1).float().cpu()
        role_p = role_logits.softmax(-1).float().cpu()
        first_pos, last_pos = positions[0], positions[-1]
        local: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for k, (first, last) in enumerate(ranges):
            start_off, end_off = window.offsets[first], window.offsets[last]
            assert start_off is not None and end_off is not None
            confidence = min(float(probs[i][tags[i]]) for i in range(first, last + 1))
            centrality = min(first - first_pos, last_pos - last)
            for piece in _split_lines(doc.text, (start_off[0], end_off[1])):
                candidate = _Found(
                    piece,
                    confidence,
                    int(category_p[k].argmax()),
                    int(role_p[k].argmax()),
                    float(role_p[k].max()),
                    centrality,
                )
                current = found.get(piece)
                if current is None or candidate.centrality > current.centrality:
                    found[piece] = candidate
                local.append((piece, (first, last)))
        for (span_a, range_a), (span_b, range_b) in pairwise(local):
            if not scope_of(doc, span_a).same(scope_of(doc, span_b)):
                continue
            logits = self.model.group_logits(hidden, [(range_a, range_b)])[0]
            centrality = min(range_a[0] - first_pos, last_pos - range_b[1])
            vote = logits.softmax(-1).float().cpu().tolist()
            key = (span_a, span_b)
            if key not in pair_votes or centrality > pair_votes[key][0]:
                pair_votes[key] = (centrality, vote)

    def _assemble(
        self,
        doc: PreprocessedDocument,
        advisory_id: str | None,
        found: dict[tuple[int, int], _Found],
        pair_votes: dict[tuple[tuple[int, int], tuple[int, int]], tuple[int, list[float]]],
    ) -> Extraction:
        kept: list[_Found] = []
        for item in sorted(found.values(), key=lambda f: (-f.confidence, f.span)):
            if all(item.span[1] <= k.span[0] or item.span[0] >= k.span[1] for k in kept):
                kept.append(item)
        kept.sort(key=lambda f: f.span)
        conditions = [
            Condition(
                id=f"c{i + 1}",
                span=item.span,
                category=Category(CATEGORIES[item.category]),
                role=Role(ROLES[item.role]),
                source="model",
                confidence=round(item.confidence * item.role_probability, 4),
            )
            for i, item in enumerate(kept)
        ]
        chains: list[tuple[list[int], set[str]]] = []
        for i in range(len(conditions) - 1):
            key = (conditions[i].span, conditions[i + 1].span)
            if key not in pair_votes:
                continue
            vote = pair_votes[key][1]
            label = GROUP_LABELS[max(range(len(vote)), key=vote.__getitem__)]
            if label == "NONE":
                continue
            if chains and chains[-1][0][-1] == i:
                chains[-1][0].append(i + 1)
                chains[-1][1].add(label)
            else:
                chains.append(([i, i + 1], {label}))
        groups = [
            Group(
                operator=(
                    GroupOperator(next(iter(labels)))
                    if len(labels) == 1
                    else GroupOperator.UNRESOLVED
                ),
                members=tuple(conditions[k].id for k in members),
            )
            for members, labels in chains
        ]
        flags = [f"low_confidence:{c.id}" for c in conditions if (c.confidence or 0) < 0.5]
        flags += ["unresolved_group" for g in groups if g.operator is GroupOperator.UNRESOLVED]
        return Extraction(
            advisory_id=advisory_id,
            content_hash=doc.content_hash,
            preprocessing_version=doc.version,
            model_id=self.model_id,
            document_status=(
                DocumentStatus.HAS_CONDITIONS
                if conditions
                else DocumentStatus.NO_EXPLICIT_CONDITION
            ),
            conditions=tuple(conditions),
            groups=tuple(groups),
            review_flags=tuple(flags),
        )
