"""Backend-independent decoding: encoder outputs -> conditions, roles and groups.

Backends (PyTorch, ONNX Runtime) only produce per-window hidden states and BIO
probabilities. The span, category, role and group heads are small linear layers applied
here in NumPy, so every backend shares one decoding path (exact parity testing) and an
ONNX deployment does not need PyTorch.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise

import numpy as np
from numpy.typing import NDArray

from triggermap.models.structure import ScopeIndex
from triggermap.models.transformer.data import (
    CATEGORIES,
    GROUP_LABELS,
    ROLES,
    Window,
    decode_bio,
)
from triggermap.schema.models import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import PreprocessedDocument

Array = NDArray[np.float32]
Span = tuple[int, int]
SpanRange = tuple[int, int]  # inclusive input positions


def softmax(x: NDArray[np.floating]) -> NDArray[np.float64]:
    z = x.astype(np.float64) - x.max(axis=-1, keepdims=True)
    e = np.exp(z)
    out: NDArray[np.float64] = e / e.sum(axis=-1, keepdims=True)
    return out


@dataclass(frozen=True)
class Heads:
    """Weights of the category, role and group linear heads."""

    category_w: Array
    category_b: Array
    role_w: Array
    role_b: Array
    group_w: Array
    group_b: Array

    NAMES = ("category", "role", "group")

    @classmethod
    def from_state(cls, state: Mapping[str, NDArray[np.floating]]) -> Heads:
        def get(name: str) -> Array:
            return np.asarray(state[name], dtype=np.float32)

        return cls(
            get("category.weight"),
            get("category.bias"),
            get("role.weight"),
            get("role.bias"),
            get("group.weight"),
            get("group.bias"),
        )

    def arrays(self) -> dict[str, Array]:
        return {
            "category.weight": self.category_w,
            "category.bias": self.category_b,
            "role.weight": self.role_w,
            "role.bias": self.role_b,
            "group.weight": self.group_w,
            "group.bias": self.group_b,
        }

    def attributes(
        self, hidden: Array, ranges: Sequence[SpanRange]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        reprs = np.stack(
            [np.concatenate([hidden[a : b + 1].mean(axis=0), hidden[a]]) for a, b in ranges]
        )
        category = softmax(reprs @ self.category_w.T + self.category_b)
        role = softmax(reprs @ self.role_w.T + self.role_b)
        return category, role

    def group(self, hidden: Array, a: SpanRange, b: SpanRange) -> NDArray[np.float64]:
        mean_a = hidden[a[0] : a[1] + 1].mean(axis=0)
        mean_b = hidden[b[0] : b[1] + 1].mean(axis=0)
        between = hidden[a[1] + 1 : b[0]].mean(axis=0) if b[0] > a[1] + 1 else np.zeros_like(mean_a)
        row = np.concatenate([mean_a, mean_b, mean_a * mean_b, between])
        return softmax(row @ self.group_w.T + self.group_b)


@dataclass
class _Found:
    span: Span
    confidence: float
    category: int
    role: int
    role_probability: float
    centrality: int  # distance (tokens) to the nearer window edge


def split_lines(text: str, span: Span) -> list[Span]:
    """Spans never cross a line: split at newlines and trim each piece."""
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


def collate(windows: Sequence[Window], pad_id: int) -> dict[str, NDArray[np.int64]]:
    """Pad a batch of windows to the longest one (dynamic padding)."""
    width = max(len(w.input_ids) for w in windows)

    def pad(rows: Sequence[Sequence[int]], value: int) -> NDArray[np.int64]:
        return np.array([list(r) + [value] * (width - len(r)) for r in rows], dtype=np.int64)

    batch = {
        "input_ids": pad([w.input_ids for w in windows], pad_id),
        "attention_mask": pad([w.attention_mask for w in windows], 0),
    }
    if all(w.token_type_ids is not None for w in windows):
        batch["token_type_ids"] = pad([w.token_type_ids or [] for w in windows], 0)
    return batch


class Decoder:
    """Accumulates per-window outputs and assembles one Extraction for a document."""

    def __init__(self, doc: PreprocessedDocument, heads: Heads) -> None:
        self.doc = doc
        self.heads = heads
        self.scopes = ScopeIndex(doc)
        self.found: dict[Span, _Found] = {}
        self.pair_votes: dict[tuple[Span, Span], tuple[int, list[float]]] = {}

    def add(self, window: Window, hidden: Array, probs: NDArray[np.floating]) -> None:
        doc = self.doc
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
        category_p, role_p = self.heads.attributes(hidden, ranges)
        first_pos, last_pos = positions[0], positions[-1]
        local: list[tuple[Span, SpanRange]] = []
        for k, (first, last) in enumerate(ranges):
            start_off, end_off = window.offsets[first], window.offsets[last]
            assert start_off is not None and end_off is not None
            confidence = min(float(probs[i][tags[i]]) for i in range(first, last + 1))
            centrality = min(first - first_pos, last_pos - last)
            for piece in split_lines(doc.text, (start_off[0], end_off[1])):
                candidate = _Found(
                    piece,
                    confidence,
                    int(category_p[k].argmax()),
                    int(role_p[k].argmax()),
                    float(role_p[k].max()),
                    centrality,
                )
                current = self.found.get(piece)
                if current is None or candidate.centrality > current.centrality:
                    self.found[piece] = candidate
                local.append((piece, (first, last)))
        for (span_a, range_a), (span_b, range_b) in pairwise(local):
            if not self.scopes.scope(span_a).same(self.scopes.scope(span_b)):
                continue
            vote = self.heads.group(hidden, range_a, range_b).tolist()
            centrality = min(range_a[0] - first_pos, last_pos - range_b[1])
            key = (span_a, span_b)
            if key not in self.pair_votes or centrality > self.pair_votes[key][0]:
                self.pair_votes[key] = (centrality, vote)

    def extraction(self, model_id: str, advisory_id: str | None) -> Extraction:
        kept: list[_Found] = []
        for item in sorted(self.found.values(), key=lambda f: (-f.confidence, f.span)):
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
            if key not in self.pair_votes:
                continue
            vote = self.pair_votes[key][1]
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
            content_hash=self.doc.content_hash,
            preprocessing_version=self.doc.version,
            model_id=model_id,
            document_status=(
                DocumentStatus.HAS_CONDITIONS
                if conditions
                else DocumentStatus.NO_EXPLICIT_CONDITION
            ),
            conditions=tuple(conditions),
            groups=tuple(groups),
            review_flags=tuple(flags),
        )
