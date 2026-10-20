"""Shared encoder with span, attribute and group heads.

- BIO head on every token (condition boundaries).
- Category and role heads on a span representation: [mean of span tokens; first token].
- Group head on consecutive span pairs in one scope:
  [mean A; mean B; mean A * mean B; mean of tokens between them].

During training the attribute and group heads see gold spans; at inference they see the
spans decoded from the BIO head.
"""

from __future__ import annotations

import inspect
from collections.abc import Sequence
from typing import Any

import torch
from torch import nn

from triggermap.models.transformer.data import (
    BIO,
    CATEGORIES,
    GROUP_LABELS,
    IGNORE,
    ROLES,
    PairTarget,
    SpanTarget,
)

SpanRange = tuple[int, int]  # inclusive input positions


class ConditionModel(nn.Module):
    def __init__(self, encoder: Any, dropout: float = 0.1) -> None:
        super().__init__()
        hidden = int(encoder.config.hidden_size)
        self.encoder = encoder
        self.dropout = nn.Dropout(dropout)
        self.bio = nn.Linear(hidden, len(BIO))
        self.category = nn.Linear(2 * hidden, len(CATEGORIES))
        self.role = nn.Linear(2 * hidden, len(ROLES))
        self.group = nn.Linear(4 * hidden, len(GROUP_LABELS))
        params = inspect.signature(encoder.forward).parameters
        self._uses_token_types = "token_type_ids" in params

    def encode(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: torch.Tensor | None = None,
    ) -> torch.Tensor:
        kwargs: dict[str, torch.Tensor] = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
        if self._uses_token_types and token_type_ids is not None:
            kwargs["token_type_ids"] = token_type_ids
        hidden: torch.Tensor = self.encoder(**kwargs).last_hidden_state
        dropped: torch.Tensor = self.dropout(hidden)
        return dropped

    def bio_logits(self, hidden: torch.Tensor) -> torch.Tensor:
        logits: torch.Tensor = self.bio(hidden)
        return logits

    @staticmethod
    def span_repr(hidden: torch.Tensor, span: SpanRange) -> torch.Tensor:
        tokens = hidden[span[0] : span[1] + 1]
        return torch.cat([tokens.mean(dim=0), hidden[span[0]]])

    def attribute_logits(
        self, hidden: torch.Tensor, spans: Sequence[SpanRange]
    ) -> tuple[torch.Tensor, torch.Tensor]:
        reprs = torch.stack([self.span_repr(hidden, s) for s in spans])
        return self.category(reprs), self.role(reprs)

    def group_logits(
        self, hidden: torch.Tensor, pairs: Sequence[tuple[SpanRange, SpanRange]]
    ) -> torch.Tensor:
        rows = []
        for a, b in pairs:
            mean_a = hidden[a[0] : a[1] + 1].mean(dim=0)
            mean_b = hidden[b[0] : b[1] + 1].mean(dim=0)
            between = (
                hidden[a[1] + 1 : b[0]].mean(dim=0) if b[0] > a[1] + 1 else torch.zeros_like(mean_a)
            )
            rows.append(torch.cat([mean_a, mean_b, mean_a * mean_b, between]))
        logits: torch.Tensor = self.group(torch.stack(rows))
        return logits


class LossWeights:
    """Class weights from training data only, plus head weights for ablations."""

    def __init__(
        self,
        bio: torch.Tensor,
        category: torch.Tensor,
        role: torch.Tensor,
        group: torch.Tensor,
        attribute_weight: float = 1.0,
        group_weight: float = 1.0,
    ) -> None:
        self.bio, self.category, self.role, self.group = bio, category, role, group
        self.attribute_weight = attribute_weight
        self.group_weight = group_weight

    def to(self, device: torch.device) -> LossWeights:
        return LossWeights(
            self.bio.to(device),
            self.category.to(device),
            self.role.to(device),
            self.group.to(device),
            self.attribute_weight,
            self.group_weight,
        )


def inverse_frequency(counts: Sequence[int], smoothing: float = 1.0) -> torch.Tensor:
    """Balanced class weights (mean 1) from training counts, smoothed for unseen classes."""
    total = sum(counts) + smoothing * len(counts)
    weights = torch.tensor([total / (len(counts) * (c + smoothing)) for c in counts])
    return weights / weights.mean()


def batch_loss(
    model: ConditionModel,
    batch: dict[str, Any],
    weights: LossWeights,
) -> tuple[torch.Tensor, dict[str, float]]:
    hidden = model.encode(batch["input_ids"], batch["attention_mask"], batch.get("token_type_ids"))
    logits = model.bio_logits(hidden)
    loss_bio = nn.functional.cross_entropy(
        logits.reshape(-1, len(BIO)),
        batch["bio"].reshape(-1),
        weight=weights.bio,
        ignore_index=IGNORE,
    )
    total = loss_bio
    parts = {"bio": float(loss_bio.detach())}

    span_rows: list[torch.Tensor] = []
    category_y: list[int] = []
    role_y: list[int] = []
    pair_rows: list[torch.Tensor] = []
    pair_y: list[int] = []
    spans_per_item: Sequence[Sequence[SpanTarget]] = batch["spans"]
    pairs_per_item: Sequence[Sequence[PairTarget]] = batch["pairs"]
    for b, (spans, pairs) in enumerate(zip(spans_per_item, pairs_per_item, strict=True)):
        for span in spans:
            span_rows.append(model.span_repr(hidden[b], (span.first, span.last)))
            category_y.append(span.category)
            role_y.append(span.role)
        if pairs and weights.group_weight > 0:
            ranges = [
                (
                    (spans[p.left].first, spans[p.left].last),
                    (spans[p.right].first, spans[p.right].last),
                )
                for p in pairs
            ]
            pair_rows.append(model.group_logits(hidden[b], ranges))
            pair_y.extend(p.label for p in pairs)

    device = hidden.device
    if span_rows and weights.attribute_weight > 0:
        reprs = torch.stack(span_rows)
        loss_cat = nn.functional.cross_entropy(
            model.category(reprs), torch.tensor(category_y, device=device), weight=weights.category
        )
        loss_role = nn.functional.cross_entropy(
            model.role(reprs), torch.tensor(role_y, device=device), weight=weights.role
        )
        total = total + weights.attribute_weight * (loss_cat + loss_role)
        parts["category"] = float(loss_cat.detach())
        parts["role"] = float(loss_role.detach())
    if pair_rows:
        loss_group = nn.functional.cross_entropy(
            torch.cat(pair_rows), torch.tensor(pair_y, device=device), weight=weights.group
        )
        total = total + weights.group_weight * loss_group
        parts["group"] = float(loss_group.detach())
    return total, parts
