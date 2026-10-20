"""Hand-built features for the CRF tagger and the logistic-regression classifiers.

Token features follow the plan: shape and affixes, neighbouring words, conditional and
negation cues with distance, part of speech (optional, from spaCy), and document context
(heading, list position, inline code). Stopwords are never removed.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cache
from itertools import pairwise
from typing import Any

from triggermap.models.crf.tokens import Token
from triggermap.text.markdown import BlockKind
from triggermap.text.preprocessing import PreprocessedDocument
from triggermap.text.segment import Sentence

FEATURE_VERSION = "crf-features-1"

Features = dict[str, float | str]

CUES = frozenset(
    "when whenever if unless only provided except even regardless requires required "
    "require must affects affected".split()
)
NEGATIONS = frozenset("not no never without cannot neither nor none n't unauthenticated".split())
_SECTION_KEYWORDS = {
    "impact": re.compile(r"impact", re.I),
    "details": re.compile(r"detail|description|summary|overview", re.I),
    "workaround": re.compile(r"workaround|mitigat|remediat", re.I),
    "fix": re.compile(r"patch|\bfix|resolution|upgrade", re.I),
    "poc": re.compile(r"proof|poc|reproduc|exploit|steps", re.I),
    "affected": re.compile(r"affected|vulnerab|condition|prerequisite|requirement", re.I),
}


def shape(word: str) -> str:
    mapped = re.sub(r"[A-Z]", "X", re.sub(r"[a-z]", "x", re.sub(r"\d", "d", word)))
    return re.sub(r"(.)\1{2,}", r"\1\1", mapped)


def _bucket(n: int | None) -> str:
    if n is None:
        return "none"
    return "0-1" if n <= 1 else "2-3" if n <= 3 else "4-7" if n <= 7 else "8+"


@dataclass(frozen=True)
class SentenceContext:
    block_kind: str
    heading: str
    list_level: int
    lead_in: bool  # paragraph immediately followed by a list


def sentence_context(doc: PreprocessedDocument, sentence: Sentence) -> SentenceContext:
    blocks = doc.canonical.blocks
    block = blocks[sentence.block]
    heading = ""
    for previous in reversed(blocks[: sentence.block]):
        if previous.kind is BlockKind.HEADING:
            heading = doc.text[previous.start : previous.end]
            break
    nxt = blocks[sentence.block + 1] if sentence.block + 1 < len(blocks) else None
    lead_in = (
        block.kind is BlockKind.PARAGRAPH and nxt is not None and nxt.kind is BlockKind.LIST_ITEM
    )
    return SentenceContext(block.kind.value, heading, block.level, lead_in)


def _context_features(ctx: SentenceContext) -> Features:
    feats: Features = {"block": ctx.block_kind, "list_level": str(ctx.list_level)}
    if ctx.lead_in:
        feats["lead_in"] = 1.0
    for name, pattern in _SECTION_KEYWORDS.items():
        if pattern.search(ctx.heading):
            feats[f"section={name}"] = 1.0
    return feats


@cache
def _spacy_nlp() -> Any:
    import spacy

    return spacy.load("en_core_web_sm", disable=["ner", "lemmatizer", "parser"])


def pos_tags(text: str, tokens: Sequence[Token], start: int) -> list[str]:
    """Penn tags from spaCy, aligned to our tokens by the spaCy token covering each start."""
    if not tokens:
        return []
    parsed = _spacy_nlp()(text[start : tokens[-1].end])
    by_char: dict[int, str] = {}
    for tok in parsed:
        for offset in range(tok.idx, tok.idx + len(tok.text)):
            by_char[start + offset] = tok.tag_
    return [by_char.get(t.start, "X") for t in tokens]


def token_features(
    doc: PreprocessedDocument,
    tokens: Sequence[Token],
    ctx: SentenceContext,
    pos: Sequence[str] | None,
) -> list[Features]:
    lowered = [t.text.lower() for t in tokens]
    context = _context_features(ctx)
    last_cue: tuple[int, str] | None = None
    out: list[Features] = []
    for i, tok in enumerate(tokens):
        word = tok.text
        low = lowered[i]
        feats: Features = {
            "bias": 1.0,
            "w": low,
            "suf3": low[-3:],
            "suf2": low[-2:],
            "pre3": low[:3],
            "shape": shape(word),
            "cue_dist": _bucket(i - last_cue[0] if last_cue else None),
        }
        if last_cue:
            feats["last_cue"] = last_cue[1]
        if word.istitle():
            feats["title"] = 1.0
        if word.isupper() and len(word) > 1:
            feats["upper"] = 1.0
        if word.isdigit():
            feats["digit"] = 1.0
        if "_" in word or "." in word.strip(".") or re.search(r"[a-z][A-Z]", word):
            feats["identifier"] = 1.0
        if doc.canonical.in_code(tok.start):
            feats["in_code"] = 1.0
        if low in CUES:
            feats["is_cue"] = 1.0
        if low in NEGATIONS:
            feats["is_neg"] = 1.0
        if any(lowered[j] in NEGATIONS for j in range(max(0, i - 3), min(len(tokens), i + 4))):
            feats["neg_window"] = 1.0
        if pos is not None:
            feats["pos"] = pos[i]
            feats["pos2"] = pos[i][:2]
        for offset in (-2, -1, 1, 2):
            j = i + offset
            if 0 <= j < len(tokens):
                feats[f"{offset}:w"] = lowered[j]
                if pos is not None:
                    feats[f"{offset}:pos"] = pos[j]
            else:
                feats[f"{offset}:edge"] = 1.0
        feats.update(context)
        out.append(feats)
        if low in CUES:
            last_cue = (i, low)
    return out


def span_features(
    tokens: Sequence[Token], first: int, last: int, ctx: SentenceContext, in_code: bool
) -> Features:
    """Features for the attribute classifiers; ``first``..``last`` inclusive token indices."""
    lowered = [t.text.lower() for t in tokens]
    inside = lowered[first : last + 1]
    before = lowered[max(0, first - 5) : first]
    feats: Features = {"len": _bucket(len(inside)), "first": inside[0], "last": inside[-1]}
    for word in inside:
        feats[f"w={word}"] = 1.0
    for a, b in pairwise(inside):
        feats[f"bi={a}_{b}"] = 1.0
    for word in before:
        feats[f"before={word}"] = 1.0
    cue = next((w for w in reversed(lowered[:first]) if w in CUES), None)
    if cue:
        feats[f"cue={cue}"] = 1.0
    if any(w in NEGATIONS for w in inside):
        feats["neg_in_span"] = 1.0
    if any(w in NEGATIONS for w in before[-3:]):
        feats["neg_before"] = 1.0
    if in_code:
        feats["in_code"] = 1.0
    feats.update(_context_features(ctx))
    return feats


def pair_features(
    text: str, a: tuple[int, int], b: tuple[int, int], same_list: bool, lead: str
) -> Features:
    """Features for whether two conditions (character spans, a before b) share a group."""
    between = text[a[1] : b[0]].lower()
    words = re.findall(r"[a-z/]+", between)
    feats: Features = {"gap": _bucket(len(words)), "same_list": float(same_list)}
    for word in words[:6]:
        feats[f"between={word}"] = 1.0
    for marker in ("and", "or", "and/or", "either", "both", "but", "while", "also"):
        if marker in words:
            feats[f"has={marker}"] = 1.0
    if ";" in between:
        feats["semicolon"] = 1.0
    lead_low = lead.lower()
    for marker in ("all of", "any of", "one of", "either", "following", "both", "combine"):
        if marker in lead_low:
            feats[f"lead={marker}"] = 1.0
    return feats
