"""Leakage groups: advisories that must never be split across train/dev/test.

Two relations are unioned:
- project: advisories naming a common PyPI package (``tensorflow`` and
  ``tensorflow-gpu`` join because one advisory names both);
- duplicate: identical text, identical details after whitespace/case folding, or a
  shared alias (CVE/PYSEC id).

Near-duplicate detection (shingling) is added when splits are frozen; until then the
pilot only relies on these exact relations.
"""

from __future__ import annotations

import hashlib
from collections.abc import Hashable, Iterable, Sequence
from dataclasses import dataclass

from triggermap.ingest.records import AdvisoryDocument


class UnionFind:
    def __init__(self) -> None:
        self._parent: dict[Hashable, Hashable] = {}

    def find(self, item: Hashable) -> Hashable:
        parent = self._parent.setdefault(item, item)
        if parent != item:
            parent = self._parent[item] = self.find(parent)
        return parent

    def union(self, items: Iterable[Hashable]) -> None:
        iterator = iter(items)
        first = next(iterator, None)
        if first is None:
            return
        root = self.find(first)
        for item in iterator:
            other = self.find(item)
            if other != root:
                self._parent[other] = root


@dataclass(frozen=True)
class Groups:
    project: dict[str, str]  # advisory id -> project group key
    duplicate: dict[str, str]  # advisory id -> duplicate group key
    leakage: dict[str, str]  # advisory id -> combined group key


def _fold(text: str) -> str:
    return hashlib.sha256(" ".join(text.lower().split()).encode()).hexdigest()


def _keys(uf: UnionFind, docs: Sequence[AdvisoryDocument], node: str) -> dict[str, str]:
    members: dict[Hashable, list[str]] = {}
    for doc in docs:
        members.setdefault(uf.find((node, doc.advisory_id)), []).append(doc.advisory_id)
    return {aid: min(ids) for ids in members.values() for aid in ids}


def build_groups(docs: Sequence[AdvisoryDocument]) -> Groups:
    project = UnionFind()
    duplicate = UnionFind()
    for doc in docs:
        node = ("doc", doc.advisory_id)
        project.union([node, *(("pkg", p) for p in doc.pypi_packages)])
        keys: list[Hashable] = [node, ("hash", doc.content_hash)]
        if doc.details.strip():
            keys.append(("details", _fold(doc.details)))
        keys += [("alias", a) for a in doc.aliases]
        duplicate.union(keys)
    project_keys = _keys(project, docs, "doc")
    duplicate_keys = _keys(duplicate, docs, "doc")

    combined = UnionFind()
    for doc in docs:
        aid = doc.advisory_id
        combined.union([("doc", aid), ("p", project_keys[aid]), ("d", duplicate_keys[aid])])
    return Groups(project_keys, duplicate_keys, _keys(combined, docs, "doc"))
