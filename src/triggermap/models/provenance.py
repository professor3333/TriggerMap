"""Training-data provenance shared by every learner (no learner dependencies)."""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Sequence

from triggermap.schema.models import AdvisoryAnnotation


def training_hash(records: Sequence[AdvisoryAnnotation]) -> str:
    """SHA-256 of the training records, independent of their order."""
    lines = sorted(r.model_dump_json() for r in records)
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def training_origins(records: Sequence[AdvisoryAnnotation]) -> dict[str, int]:
    """How many training records each label origin contributed (``unrecorded`` before 1.1)."""
    counts = Counter(r.origin.value if r.origin else "unrecorded" for r in records)
    return dict(sorted(counts.items()))
