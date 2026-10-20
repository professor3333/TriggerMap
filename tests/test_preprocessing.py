import hashlib
from typing import Any

from triggermap.text.preprocessing import (
    PREPROCESSING_VERSION,
    compose_raw,
    content_hash,
    preprocess,
)


def test_compose_raw_joins_present_fields() -> None:
    assert compose_raw("Title", "Body") == "Title\n\nBody"
    assert compose_raw(None, "Body") == "Body"
    assert compose_raw("Title", "") == "Title"


def test_preprocess_is_deterministic_and_hashed(flask_advisory: dict[str, Any]) -> None:
    raw = compose_raw(flask_advisory["summary"], flask_advisory["details"])
    first, second = preprocess(raw), preprocess(raw)
    assert first == second
    assert first.content_hash == hashlib.sha256(raw.encode()).hexdigest() == content_hash(raw)
    assert first.version == PREPROCESSING_VERSION
    assert first.text.startswith("Flask vulnerable to possible disclosure")


def test_every_sentence_maps_back_to_raw(aiohttp_advisory: dict[str, Any]) -> None:
    doc = preprocess(compose_raw(aiohttp_advisory["summary"], aiohttp_advisory["details"]))
    for sentence in doc.sentences:
        raw_start, raw_end = doc.canonical.to_raw(sentence.start, sentence.end)
        assert 0 <= raw_start < raw_end <= len(doc.raw)
