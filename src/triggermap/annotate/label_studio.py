"""Label Studio tasks out, validated annotation records in.

Tasks carry the canonical text (what annotators label), the raw Markdown for reference,
and the provenance needed to reject stale tasks on import. The converter never changes
a label: it maps offsets, rebuilds groups from relations and reports every problem.
The one mechanical normalisation, trimming whitespace at span edges, is reported.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from pydantic import ValidationError

from triggermap.corpus.groups import UnionFind
from triggermap.ingest.records import AdvisoryDocument
from triggermap.schema.models import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Group,
    GroupOperator,
    Role,
)
from triggermap.schema.validate import Issue, validate_annotation
from triggermap.text.preprocessing import PREPROCESSING_VERSION, compose_raw, preprocess

ADVISORY_URL = "https://github.com/advisories/{}"


def build_task(doc: AdvisoryDocument, order: int) -> dict[str, Any]:
    raw = compose_raw(doc.summary, doc.details)
    pre = preprocess(raw)
    meta = (
        f"#{order} · packages: {', '.join(doc.pypi_packages)} · published {doc.published[:10]}"
        f" · {ADVISORY_URL.format(doc.advisory_id)}"
    )
    return {
        "data": {
            "advisory_id": doc.advisory_id,
            "meta": meta,
            "text": pre.text,
            "raw": raw,
            "content_hash": pre.content_hash,
            "preprocessing_version": pre.version,
            "source_commit": doc.source_commit,
            "order": order,
        }
    }


def utf16_to_codepoint(text: str, offset: int) -> int:
    """Convert a JavaScript (UTF-16 code unit) offset into a Python string index."""
    units = 0
    for index, ch in enumerate(text):
        if units >= offset:
            return index
        units += 2 if ord(ch) > 0xFFFF else 1
    return len(text)


@dataclass
class Conversion:
    advisory_id: str
    record: AdvisoryAnnotation | None
    issues: list[Issue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)  # informational, never blocking
    lead_time: float | None = None


@dataclass
class _Region:
    region_id: str
    start: int
    end: int
    text: str
    labels: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)


def convert_task(
    task: Mapping[str, Any],
    corpus: Mapping[str, AdvisoryDocument],
    annotation_version: str,
    annotator: str,
) -> Conversion:
    data = task.get("data", {})
    aid = str(data.get("advisory_id", "?"))
    conv = Conversion(aid, None)

    doc = corpus.get(aid)
    if doc is None:
        conv.issues.append(Issue("unknown_advisory", "advisory not in the processed corpus"))
        return conv
    raw = compose_raw(doc.summary, doc.details)
    pre = preprocess(raw)
    if data.get("content_hash") != pre.content_hash:
        conv.issues.append(Issue("stale_task", "advisory text changed since the task was made"))
    if data.get("preprocessing_version") != PREPROCESSING_VERSION:
        conv.issues.append(
            Issue("stale_task", f"task preprocessing {data.get('preprocessing_version')}")
        )
    if data.get("text") != pre.text:
        conv.issues.append(Issue("stale_task", "task text differs from current canonical text"))
    if conv.issues:
        return conv

    annotations = [a for a in task.get("annotations", []) if not a.get("was_cancelled")]
    if not annotations:
        conv.issues.append(Issue("not_annotated", "no completed annotation"))
        return conv
    annotation = max(annotations, key=lambda a: str(a.get("updated_at") or a.get("id")))
    if len(annotations) > 1:
        conv.notes.append(f"{len(annotations)} annotations; used the most recently updated")
    lead_time = annotation.get("lead_time")
    conv.lead_time = float(lead_time) if isinstance(lead_time, int | float) else None

    regions, relations, status, note_text = _read_results(annotation.get("result", []), conv)
    conditions, id_map = _conditions(regions, pre.text, conv)
    groups = _groups(relations, id_map, conditions, conv)

    if status is None:
        conv.issues.append(Issue("missing_status", "document status not chosen"))
        return conv
    try:
        record = AdvisoryAnnotation(
            advisory_id=aid,
            source_commit=doc.source_commit,
            content_hash=pre.content_hash,
            preprocessing_version=pre.version,
            annotation_version=annotation_version,
            document_status=DocumentStatus(status),
            conditions=tuple(conditions),
            groups=tuple(groups),
            annotator=annotator,
            notes=note_text,
        )
    except (ValidationError, ValueError) as exc:
        conv.issues.append(Issue("invalid_record", str(exc).splitlines()[0]))
        return conv
    conv.issues += validate_annotation(record, pre.text)
    conv.record = record
    return conv


def _read_results(
    results: Iterable[Mapping[str, Any]], conv: Conversion
) -> tuple[dict[str, _Region], list[Mapping[str, Any]], str | None, str | None]:
    regions: dict[str, _Region] = {}
    relations: list[Mapping[str, Any]] = []
    status: str | None = None
    notes: str | None = None
    for item in results:
        kind, name, value = item.get("type"), item.get("from_name"), item.get("value", {})
        if kind == "relation":
            relations.append(item)
        elif name == "condition" and kind == "labels":
            region = regions.setdefault(
                str(item["id"]), _Region(str(item["id"]), -1, -1, str(value.get("text", "")))
            )
            region.start, region.end = int(value["start"]), int(value["end"])
            region.labels += list(value.get("labels", []))
        elif name == "role" and kind == "choices":
            region = regions.setdefault(
                str(item["id"]),
                _Region(str(item["id"]), -1, -1, str(value.get("text", ""))),
            )
            region.roles += list(value.get("choices", []))
        elif name == "document_status":
            choices = value.get("choices", [])
            status = str(choices[0]) if choices else None
        elif name == "notes":
            texts = value.get("text", [])
            notes = "\n".join(str(t) for t in texts) or None
        else:
            conv.notes.append(f"ignored result {name}/{kind}")
    return regions, relations, status, notes


def _locate(text: str, region: _Region) -> tuple[int, int] | None:
    """Find the region's offsets in Python indices, accepting code-point or UTF-16 offsets."""
    candidates = [
        (region.start, region.end),
        (utf16_to_codepoint(text, region.start), utf16_to_codepoint(text, region.end)),
    ]
    for start, end in candidates:
        if 0 <= start < end <= len(text) and (not region.text or text[start:end] == region.text):
            return start, end
    return None


def _conditions(
    regions: Mapping[str, _Region], text: str, conv: Conversion
) -> tuple[list[Condition], dict[str, str]]:
    located: list[tuple[int, int, _Region]] = []
    for region in regions.values():
        if region.start < 0:
            conv.issues.append(
                Issue("role_without_span", "role on a missing region", region.region_id)
            )
            continue
        span = _locate(text, region)
        if span is None:
            conv.issues.append(
                Issue(
                    "surface_mismatch",
                    f"[{region.start}, {region.end}) does not match {region.text!r}",
                    region.region_id,
                )
            )
            continue
        start, end = span
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        if (start, end) != span:
            conv.notes.append(f"trimmed whitespace on region {region.region_id}")
        if start == end:
            conv.issues.append(Issue("empty_span", "span is only whitespace", region.region_id))
            continue
        located.append((start, end, region))

    conditions: list[Condition] = []
    id_map: dict[str, str] = {}
    for index, (start, end, region) in enumerate(sorted(located, key=lambda x: (x[0], x[1]))):
        cid = f"c{index + 1}"
        id_map[region.region_id] = cid
        if len(region.labels) != 1:
            conv.issues.append(Issue("label_count", f"{len(region.labels)} categories", cid))
            continue
        if len(region.roles) != 1:
            conv.issues.append(Issue("missing_role", f"{len(region.roles)} roles chosen", cid))
            continue
        try:
            category, role = Category(region.labels[0]), Role(region.roles[0])
        except ValueError as exc:
            conv.issues.append(Issue("unknown_label", str(exc), cid))
            continue
        conditions.append(
            Condition(id=cid, span=(start, end), category=category, role=role, source="gold")
        )
    return conditions, id_map


def _groups(
    relations: Sequence[Mapping[str, Any]],
    id_map: Mapping[str, str],
    conditions: Sequence[Condition],
    conv: Conversion,
) -> list[Group]:
    """Each connected component of relation links is one group; all links must agree."""
    uf = UnionFind()
    edges: list[tuple[str, str, str]] = []
    for rel in relations:
        a, b = id_map.get(str(rel.get("from_id"))), id_map.get(str(rel.get("to_id")))
        if a is None or b is None:
            conv.issues.append(Issue("relation_unknown_region", "relation to a dropped region"))
            continue
        labels = list(rel.get("labels") or [])
        if len(labels) != 1:
            conv.issues.append(Issue("relation_label_count", f"{a}-{b}: {labels}"))
            continue
        uf.union([a, b])
        edges.append((a, b, str(labels[0])))

    members: dict[Hashable, set[str]] = {}
    operators: dict[Hashable, set[str]] = {}
    for a, b, label in edges:
        root = uf.find(a)
        members.setdefault(root, set()).update((a, b))
        operators.setdefault(root, set()).add(label)

    order = {c.id: c.span for c in conditions}
    groups: list[Group] = []
    for root, group_members in members.items():
        ordered = tuple(sorted(group_members, key=lambda m: (order.get(m, (-1, -1)), m)))
        if len(operators[root]) != 1:
            conv.issues.append(
                Issue("contradictory_group", f"{list(ordered)} linked as {sorted(operators[root])}")
            )
            continue
        try:
            operator = GroupOperator(next(iter(operators[root])))
        except ValueError:
            conv.issues.append(Issue("unknown_label", f"relation label {operators[root]}"))
            continue
        groups.append(Group(operator=operator, members=ordered))
    groups.sort(key=lambda g: (order.get(g.members[0], (-1, -1)), g.members))
    return groups
