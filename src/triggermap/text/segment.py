"""Rule-based sentence segmentation over canonical text.

Boundaries never fall inside code, and dotted identifiers (``flask.session.permanent``),
versions (``3.9.2``) and common abbreviations (``e.g.``) do not end a sentence. Each
line of a block is segmented separately; a code block is a single segment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from triggermap.text.markdown import BlockKind, CanonicalText

_ABBREVIATIONS = frozenset(
    {"e.g", "i.e", "eg", "ie", "cf", "vs", "approx", "incl", "no", "fig", "al", "resp", "viz"}
)
_CLOSERS = "\"')]}\u2019\u201d"
_OPENERS = "\"'([{\u2018\u201c"
_WORD_BEFORE = re.compile(r"([A-Za-z][A-Za-z.]*)$")


@dataclass(frozen=True)
class Sentence:
    start: int
    end: int
    block: int  # index into CanonicalText.blocks


def segment(doc: CanonicalText) -> tuple[Sentence, ...]:
    sentences: list[Sentence] = []
    for index, block in enumerate(doc.blocks):
        if block.kind is BlockKind.CODE:
            _add(sentences, doc.text, block.start, block.end, index)
            continue
        line_start = block.start
        while line_start < block.end:
            line_end = doc.text.find("\n", line_start, block.end)
            if line_end < 0:
                line_end = block.end
            start = line_start
            for boundary in _boundaries(doc, line_start, line_end):
                _add(sentences, doc.text, start, boundary, index)
                start = boundary
            _add(sentences, doc.text, start, line_end, index)
            line_start = line_end + 1
    return tuple(sentences)


def _boundaries(doc: CanonicalText, start: int, end: int) -> list[int]:
    text = doc.text
    found: list[int] = []
    for p in range(start, end):
        if text[p] not in ".!?" or doc.in_code(p):
            continue
        q = p + 1
        while q < end and text[q] in _CLOSERS:
            q += 1
        if q >= end or not text[q].isspace():
            continue
        r = q
        while r < end and text[r].isspace():
            r += 1
        if r >= end:
            continue
        nxt = text[r]
        if not (nxt.isupper() or nxt.isdigit() or nxt in _OPENERS or doc.in_code(r)):
            continue
        if text[p] == "." and _is_abbreviation(text[start:p]):
            continue
        found.append(q)
    return found


def _is_abbreviation(before: str) -> bool:
    m = _WORD_BEFORE.search(before)
    return m is not None and m.group(1).lower() in _ABBREVIATIONS


def _add(out: list[Sentence], text: str, start: int, end: int, block: int) -> None:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if start < end:
        out.append(Sentence(start, end, block))
