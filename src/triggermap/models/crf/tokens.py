"""Tokenisation with character offsets and BIO conversion.

Identifiers stay whole (``follow_symlinks``, ``flask.session.permanent``, ``Cache-Control``)
so their spelling survives tagging. A gold span whose edge falls inside a token cannot be
represented in BIO; such spans are counted as unreachable, never silently moved.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

_TOKEN = re.compile(r"[A-Za-z_][\w]*(?:[.\-/][\w]+)*|\d+(?:\.\d+)*|\S")

Span = tuple[int, int]


@dataclass(frozen=True)
class Token:
    start: int
    end: int
    text: str


def tokenize(text: str, start: int = 0, end: int | None = None) -> list[Token]:
    stop = len(text) if end is None else end
    return [Token(m.start(), m.end(), m.group()) for m in _TOKEN.finditer(text, start, stop)]


def bio_tags(tokens: Sequence[Token], spans: Sequence[Span]) -> tuple[list[str], list[Span]]:
    """BIO tags for ``spans`` over ``tokens``; also returns the spans that cannot be tagged."""
    tags = ["O"] * len(tokens)
    starts = {t.start: i for i, t in enumerate(tokens)}
    ends = {t.end: i for i, t in enumerate(tokens)}
    unreachable: list[Span] = []
    for span in spans:
        first, last = starts.get(span[0]), ends.get(span[1])
        if first is None or last is None or last < first:
            unreachable.append(span)
            continue
        tags[first] = "B"
        for i in range(first + 1, last + 1):
            tags[i] = "I"
    return tags, unreachable


def spans_from_tags(tokens: Sequence[Token], tags: Sequence[str]) -> list[tuple[int, int]]:
    """Token index ranges (inclusive start, exclusive end) of tagged spans."""
    ranges: list[tuple[int, int]] = []
    start: int | None = None
    for i, tag in enumerate(tags):
        if tag == "B" or (tag == "I" and start is None):
            if start is not None:
                ranges.append((start, i))
            start = i
        elif tag == "O" and start is not None:
            ranges.append((start, i))
            start = None
    if start is not None:
        ranges.append((start, len(tags)))
    return ranges
