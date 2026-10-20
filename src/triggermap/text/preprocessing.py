"""The single preprocessing entry point shared by annotation, training and serving.

Bump PREPROCESSING_VERSION whenever the raw-text composition, canonical text, offset
map or segmentation could change: annotations are pinned to this version, so a bump
requires migrating and re-validating every existing annotation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from triggermap.text.markdown import CanonicalText, canonicalize
from triggermap.text.segment import Sentence, segment

PREPROCESSING_VERSION = "1"

# The annotated document is the advisory summary followed by its details.
FIELD_SEPARATOR = "\n\n"


@dataclass(frozen=True)
class PreprocessedDocument:
    content_hash: str  # SHA-256 of the raw text
    canonical: CanonicalText
    sentences: tuple[Sentence, ...]
    version: str = PREPROCESSING_VERSION

    @property
    def raw(self) -> str:
        return self.canonical.raw

    @property
    def text(self) -> str:
        return self.canonical.text


def compose_raw(summary: str | None, details: str | None) -> str:
    """Build the raw document text from OSV ``summary`` and ``details``."""
    return FIELD_SEPARATOR.join(part for part in (summary, details) if part)


def content_hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preprocess(raw: str) -> PreprocessedDocument:
    canonical = canonicalize(raw)
    return PreprocessedDocument(content_hash(raw), canonical, segment(canonical))
