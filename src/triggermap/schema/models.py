"""Label inventory and annotation records (v1).

This module is the single source of truth for labels. Changing it requires matching
changes to the validator, annotation guidelines, Label Studio config, evaluator,
review policy and UI templates in the same commit.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ANNOTATION_SCHEMA_VERSION = "1"


class Category(StrEnum):
    CONFIGURATION = "CONFIGURATION"
    USAGE = "USAGE"
    ACCESS = "ACCESS"
    PLATFORM = "PLATFORM"


class Role(StrEnum):
    REQUIRED = "REQUIRED"
    EXCEPTION = "EXCEPTION"
    NOT_REQUIRED = "NOT_REQUIRED"
    UNCERTAIN = "UNCERTAIN"


class GroupOperator(StrEnum):
    ALL = "ALL"
    ANY = "ANY"
    UNRESOLVED = "UNRESOLVED"


class DocumentStatus(StrEnum):
    HAS_CONDITIONS = "HAS_CONDITIONS"
    NO_EXPLICIT_CONDITION = "NO_EXPLICIT_CONDITION"
    UNSUPPORTED_STRUCTURE = "UNSUPPORTED_STRUCTURE"


class ReviewAnswer(StrEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    UNKNOWN = "UNKNOWN"


ConditionSource = Literal["gold", "rules", "model", "human"]

Sha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
GitSha = Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Condition(_Frozen):
    """A contiguous condition span; offsets are half-open into the canonical text."""

    id: str = Field(min_length=1)
    span: tuple[int, int]
    category: Category
    role: Role
    source: ConditionSource = "gold"
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    @field_validator("span")
    @classmethod
    def _span_ordered(cls, span: tuple[int, int]) -> tuple[int, int]:
        start, end = span
        if start < 0 or end <= start:
            raise ValueError(f"span must satisfy 0 <= start < end, got {span}")
        return span


class Group(_Frozen):
    """A flat logical group of conditions within one sentence or list block."""

    operator: GroupOperator
    members: tuple[str, ...]


class AdvisoryAnnotation(_Frozen):
    """One annotated advisory, stored as one JSONL line."""

    advisory_id: str = Field(pattern=r"^GHSA(-[23456789cfghjmpqrvwx]{4}){3}$")
    source_commit: GitSha
    content_hash: Sha256
    preprocessing_version: str
    annotation_version: str
    schema_version: str = ANNOTATION_SCHEMA_VERSION
    document_status: DocumentStatus
    conditions: tuple[Condition, ...] = ()
    groups: tuple[Group, ...] = ()
    annotator: str | None = None
    adjudicated: bool = False
    notes: str | None = None


class Extraction(_Frozen):
    """A system's prediction for one document; same label space as a gold annotation.

    ``review_flags`` carries machine-readable reasons a reviewer should look closer
    (for example ``low_confidence:c2`` or ``unresolved_group``).
    """

    advisory_id: str | None = None  # pasted text has no advisory id
    content_hash: Sha256
    preprocessing_version: str
    model_id: str = Field(min_length=1)
    document_status: DocumentStatus
    conditions: tuple[Condition, ...] = ()
    groups: tuple[Group, ...] = ()
    review_flags: tuple[str, ...] = ()
