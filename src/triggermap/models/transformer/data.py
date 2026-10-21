"""Windows, labels and offsets for transformer models.

A document is tokenised once to find subword boundaries, then cut into overlapping windows
(about 384 to 512 tokens, 64-token overlap) that start and end on word boundaries. Each window
is encoded as a pair: context (governing heading and, inside a list, its lead-in) as the
first sequence and the window text as the second, so list scope survives windowing. Only
window tokens carry labels and offsets; context and special tokens are ignored (-100).

Offsets are canonical-text character offsets with leading whitespace stripped
(SentencePiece tokenisers such as DeBERTa-v3 include the preceding space).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from triggermap.models.structure import ScopeIndex, context_for
from triggermap.schema.models import AdvisoryAnnotation, Category, Role
from triggermap.text.preprocessing import PreprocessedDocument

BIO = ("O", "B", "I")
CATEGORIES = tuple(c.value for c in Category)
ROLES = tuple(r.value for r in Role)
GROUP_LABELS = ("NONE", "ALL", "ANY", "UNRESOLVED")
IGNORE = -100

Offset = tuple[int, int]


@dataclass(frozen=True)
class WindowParams:
    max_length: int = 512
    stride: int = 64  # tokens shared by consecutive windows
    context_tokens: int = 48  # budget reserved for the context sequence
    use_context: bool = True


@dataclass(frozen=True)
class SpanTarget:
    first: int  # input position of the first token
    last: int  # input position of the last token (inclusive)
    category: int
    role: int
    condition_id: str


@dataclass(frozen=True)
class PairTarget:
    left: int  # index into Window.spans
    right: int
    label: int


@dataclass
class Window:
    char_start: int
    char_end: int
    input_ids: list[int]
    attention_mask: list[int]
    token_type_ids: list[int] | None
    offsets: list[Offset | None]  # canonical offsets of window tokens; None elsewhere
    bio: list[int] = field(default_factory=list)
    spans: list[SpanTarget] = field(default_factory=list)
    pairs: list[PairTarget] = field(default_factory=list)
    unreachable: int = 0


def normalize_offset(text: str, start: int, end: int) -> Offset | None:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return (start, end) if start < end else None


def _token_offsets(tokenizer: Any, text: str) -> list[Offset]:
    encoded = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True, verbose=False)
    out = []
    for start, end in encoded["offset_mapping"]:
        normalized = normalize_offset(text, start, end)
        if normalized is not None:
            out.append(normalized)
    return out


def _word_start(text: str, offsets: Sequence[Offset], i: int) -> bool:
    if i == 0:
        return True
    start = offsets[i][0]
    return offsets[i - 1][1] < start or start == 0 or text[start - 1].isspace()


def window_spans(text: str, tokenizer: Any, params: WindowParams) -> list[Offset]:
    """Character ranges of the windows, cut on word boundaries with token overlap."""
    offsets = _token_offsets(tokenizer, text)
    if not offsets:
        return []
    budget = params.max_length - 3 - (params.context_tokens if params.use_context else 0)
    budget = max(budget, 16)
    spans: list[Offset] = []
    start = 0
    while True:
        end = min(start + budget, len(offsets))
        if end < len(offsets):
            cut = end
            while cut > start + budget // 2 and not _word_start(text, offsets, cut):
                cut -= 1
            end = cut if cut > start + budget // 2 else end
        spans.append((offsets[start][0], offsets[end - 1][1]))
        if end >= len(offsets):
            return spans
        nxt = max(end - params.stride, start + 1)
        while nxt > start + 1 and not _word_start(text, offsets, nxt):
            nxt -= 1
        start = nxt


def encode_window(
    doc: PreprocessedDocument,
    tokenizer: Any,
    char_range: Offset,
    params: WindowParams,
) -> Window:
    window_text = doc.text[char_range[0] : char_range[1]]
    context = context_for(doc, char_range[0]) if params.use_context else ""
    if context:
        encoded = tokenizer(
            context,
            window_text,
            return_offsets_mapping=True,
            truncation="only_first",
            max_length=params.max_length,
            verbose=False,
        )
        window_sequence = 1
    else:
        encoded = tokenizer(
            window_text,
            return_offsets_mapping=True,
            truncation=True,
            max_length=params.max_length,
            verbose=False,
        )
        window_sequence = 0
    sequence_ids = encoded.sequence_ids(0)
    offsets: list[Offset | None] = []
    for seq, (start, end) in zip(sequence_ids, encoded["offset_mapping"], strict=True):
        if seq != window_sequence:
            offsets.append(None)
            continue
        offsets.append(normalize_offset(doc.text, start + char_range[0], end + char_range[0]))
    return Window(
        char_start=char_range[0],
        char_end=char_range[1],
        input_ids=list(encoded["input_ids"]),
        attention_mask=list(encoded["attention_mask"]),
        token_type_ids=(list(encoded["token_type_ids"]) if "token_type_ids" in encoded else None),
        offsets=offsets,
    )


def label_window(
    doc: PreprocessedDocument,
    window: Window,
    record: AdvisoryAnnotation,
    scopes: ScopeIndex | None = None,
) -> None:
    """Fill BIO tags, span targets and pair targets from a gold record."""
    scopes = scopes or ScopeIndex(doc)
    window.bio = [IGNORE if o is None else 0 for o in window.offsets]
    by_start = {o[0]: i for i, o in enumerate(window.offsets) if o is not None}
    by_end = {o[1]: i for i, o in enumerate(window.offsets) if o is not None}
    inside = sorted(
        (
            c
            for c in record.conditions
            if window.char_start <= c.span[0] and c.span[1] <= window.char_end
        ),
        key=lambda c: c.span,
    )
    for cond in inside:
        first, last = by_start.get(cond.span[0]), by_end.get(cond.span[1])
        if first is None or last is None or last < first:
            window.unreachable += 1
            continue
        window.bio[first] = 1
        for i in range(first + 1, last + 1):
            if window.offsets[i] is not None:
                window.bio[i] = 2
        window.spans.append(
            SpanTarget(
                first,
                last,
                CATEGORIES.index(cond.category.value),
                ROLES.index(cond.role.value),
                cond.id,
            )
        )
    group_of = {m: (gi, g.operator.value) for gi, g in enumerate(record.groups) for m in g.members}
    spans = {c.id: c.span for c in record.conditions}
    for i in range(len(window.spans) - 1):
        a, b = window.spans[i], window.spans[i + 1]
        if not scopes.scope(spans[a.condition_id]).same(scopes.scope(spans[b.condition_id])):
            continue
        ga, gb = group_of.get(a.condition_id), group_of.get(b.condition_id)
        label = (
            GROUP_LABELS.index(ga[1]) if ga is not None and gb is not None and ga[0] == gb[0] else 0
        )
        window.pairs.append(PairTarget(i, i + 1, label))


def make_windows(
    doc: PreprocessedDocument,
    tokenizer: Any,
    params: WindowParams,
    record: AdvisoryAnnotation | None = None,
) -> list[Window]:
    windows = [
        encode_window(doc, tokenizer, span, params)
        for span in window_spans(doc.text, tokenizer, params)
    ]
    if record is not None:
        if record.content_hash != doc.content_hash:
            raise ValueError(f"{record.advisory_id}: annotation is for different text")
        scopes = ScopeIndex(doc)
        for window in windows:
            label_window(doc, window, record, scopes)
    return windows


def decode_bio(tags: Sequence[int]) -> list[tuple[int, int]]:
    """Inclusive (first, last) position ranges of tagged spans; ignored positions break spans."""
    spans: list[tuple[int, int]] = []
    start: int | None = None
    previous = -1
    for i, tag in enumerate(tags):
        if tag == IGNORE or tag == 0:
            if start is not None:
                spans.append((start, previous))
                start = None
            continue
        if tag == 1 or start is None:
            if start is not None:
                spans.append((start, previous))
            start = i
        previous = i
    if start is not None:
        spans.append((start, previous))
    return spans
