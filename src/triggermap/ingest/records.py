"""OSV input shape and the processed advisory record."""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from triggermap.schema.models import GitSha, Sha256


class OsvPackage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    ecosystem: str
    name: str


class OsvAffected(BaseModel):
    model_config = ConfigDict(extra="ignore")

    package: OsvPackage


class OsvReference(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: str | None = None
    url: str


class OsvRecord(BaseModel):
    """The subset of an OSV record that ingestion relies on; other fields are ignored."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(min_length=1)
    modified: str
    published: str
    withdrawn: str | None = None
    aliases: list[str] = []
    summary: str = ""
    details: str = ""
    affected: list[OsvAffected] = Field(min_length=1)
    references: list[OsvReference] = []
    database_specific: dict[str, Any] = {}


_PEP503 = re.compile(r"[-_.]+")


def normalize_package_name(name: str) -> str:
    """PEP 503 normalisation, so ``Flask`` and ``flask`` count as one project."""
    return _PEP503.sub("-", name).lower()


class AdvisoryDocument(BaseModel):
    """One PyPI advisory as kept by ingestion (one JSONL line)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    advisory_id: str
    aliases: tuple[str, ...]
    published: str
    modified: str
    summary: str
    details: str
    pypi_packages: tuple[str, ...]  # PEP 503-normalised names
    ecosystems: tuple[str, ...]
    references: tuple[str, ...]
    cwe_ids: tuple[str, ...]
    source_commit: GitSha
    source_path: str  # relative to the advisory-database repository root
    file_sha256: Sha256
    content_hash: Sha256  # SHA-256 of compose_raw(summary, details)
