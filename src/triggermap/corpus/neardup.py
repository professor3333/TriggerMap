"""Near-duplicate advisories via MinHash LSH over word shingles, verified by exact Jaccard.

Candidate pairs come from banded MinHash signatures; every reported pair is then checked
with the exact Jaccard similarity of its shingle sets, so the threshold is exact and the
LSH only affects recall of very borderline pairs.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from itertools import combinations

import numpy as np

_WORD = re.compile(r"[a-z0-9_]+")
_PRIME = (1 << 31) - 1  # products of two 31-bit values fit in int64


@dataclass(frozen=True)
class NearDupParams:
    shingle: int = 5
    permutations: int = 128
    bands: int = 32  # rows per band = permutations / bands
    # 0.6 chosen on snapshot 1912cbd6: cross-package pairs above it are shared boilerplate,
    # and for leakage control over-merging only costs group size.
    threshold: float = 0.6
    seed: int = 20261020


def shingles(text: str, size: int) -> frozenset[int]:
    words = _WORD.findall(text.lower())
    if len(words) < size:
        return frozenset({_hash(" ".join(words))}) if words else frozenset()
    return frozenset(_hash(" ".join(words[i : i + size])) for i in range(len(words) - size + 1))


def _hash(text: str) -> int:
    return int.from_bytes(hashlib.blake2b(text.encode(), digest_size=8).digest(), "big") % _PRIME


def jaccard(a: frozenset[int], b: frozenset[int]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def _coefficients(params: NearDupParams) -> tuple[np.ndarray, np.ndarray]:
    a, b = [], []
    for i in range(params.permutations):
        digest = hashlib.blake2b(f"{params.seed}:{i}".encode(), digest_size=16).digest()
        a.append(int.from_bytes(digest[:8], "big") % (_PRIME - 1) + 1)
        b.append(int.from_bytes(digest[8:], "big") % _PRIME)
    return np.array(a, dtype=np.int64)[:, None], np.array(b, dtype=np.int64)[:, None]


def near_duplicate_pairs(
    texts: Mapping[str, str], params: NearDupParams | None = None
) -> list[tuple[str, str, float]]:
    """Pairs of ids whose shingle Jaccard is at least ``params.threshold``, sorted."""
    params = params or NearDupParams()
    rows = params.permutations // params.bands
    a, b = _coefficients(params)
    sets = {key: shingles(text, params.shingle) for key, text in sorted(texts.items())}
    buckets: dict[tuple[int, tuple[int, ...]], list[str]] = {}
    for key, values in sets.items():
        if not values:
            continue
        v = np.fromiter(values, dtype=np.int64, count=len(values))[None, :]
        signature = ((a * v + b) % _PRIME).min(axis=1).tolist()
        for band in range(params.bands):
            chunk = tuple(signature[band * rows : (band + 1) * rows])
            buckets.setdefault((band, chunk), []).append(key)
    candidates: set[tuple[str, str]] = set()
    for members in buckets.values():
        for first, second in combinations(members, 2):
            candidates.add((first, second) if first < second else (second, first))
    pairs = []
    for left, right in sorted(candidates):
        score = jaccard(sets[left], sets[right])
        if score >= params.threshold:
            pairs.append((left, right, round(score, 4)))
    return pairs


def similarity_profile(
    texts: Mapping[str, str], thresholds: Iterable[float], params: NearDupParams | None = None
) -> dict[float, int]:
    """How many verified pairs exist at each threshold (for choosing one)."""
    base = params or NearDupParams()
    lowest = min(thresholds)
    pairs = near_duplicate_pairs(
        texts,
        NearDupParams(base.shingle, base.permutations, base.bands, lowest, base.seed),
    )
    return {t: sum(score >= t for _, _, score in pairs) for t in thresholds}
