"""Request and response models for the HTTP API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from triggermap.schema.models import Category, DocumentStatus, Group, Role

Answer = Literal["PRESENT", "ABSENT", "UNKNOWN", "UNANSWERED"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(_Strict):
    """Exactly one of a known advisory id (GHSA, CVE or PYSEC) or pasted text."""

    advisory_id: str | None = Field(default=None, max_length=64)
    text: str | None = None
    title: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def _one_source(self) -> Source:
        if (self.advisory_id is None) == (self.text is None):
            raise ValueError("give exactly one of advisory_id or text")
        if self.text is not None and not self.text.strip():
            raise ValueError("text is empty")
        return self


class ExtractionRequest(Source):
    pass


class ConditionOut(_Strict):
    id: str
    span: tuple[int, int]
    raw_span: tuple[int, int]
    surface: str
    category: Category
    role: Role
    source: str
    confidence: float | None
    review_reasons: list[str]


class ExtractionOut(_Strict):
    advisory_id: str | None
    title: str
    source_url: str | None
    packages: list[str]
    source_commit: str | None
    content_hash: str
    preprocessing_version: str
    model_id: str
    review_policy_version: str
    document_status: DocumentStatus
    text: str
    conditions: list[ConditionOut]
    groups: list[Group]
    review_flags: list[str]
    cached: bool


class ReviewCondition(_Strict):
    id: str = Field(min_length=1, max_length=32)
    span: tuple[int, int]
    category: Category
    role: Role
    source: Literal["model", "rules", "human"]
    answer: Answer = "UNANSWERED"
    confidence: float | None = Field(default=None, ge=0, le=1)


class ReviewState(_Strict):
    document_status: DocumentStatus
    conditions: list[ReviewCondition] = Field(default_factory=list, max_length=500)
    groups: list[Group] = Field(default_factory=list, max_length=200)
    notes: str | None = Field(default=None, max_length=5000)


class ReviewCreate(Source):
    model_id: str
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    preprocessing_version: str
    review_policy_version: str
    state: ReviewState


class RevisionCreate(_Strict):
    state: ReviewState
    note: str | None = Field(default=None, max_length=1000)


class ReviewCreated(_Strict):
    review_id: str
    created: bool


class RevisionCreated(_Strict):
    review_id: str
    seq: int
    created: bool


class OsvItem(_Strict):
    vulnerability_id: str
    package: str
    version: str | None
    ecosystem: str
    status: Literal["extracted", "not_in_snapshot", "unsupported_ecosystem"]
    advisory_id: str | None = None
    document_status: DocumentStatus | None = None
    conditions: int | None = None
    review_required: int | None = None


class OsvImportOut(_Strict):
    items: list[OsvItem]
    counts: dict[str, int]
