"""Evidence-linked review page: advisory text with highlights beside a checklist.

Checklist wording is the source span plus a fixed template keyed on category and role;
no text is generated. All advisory text is escaped (Jinja autoescape), and the embedded
JSON payload is escaped for a <script> context.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from triggermap.schema.models import Category, DocumentStatus, Extraction, GroupOperator, Role
from triggermap.text.preprocessing import PreprocessedDocument

ROLE_HEADINGS = {
    Role.REQUIRED: "Required for exposure",
    Role.EXCEPTION: "Not exposed if",
    Role.NOT_REQUIRED: "Explicitly not required",
    Role.UNCERTAIN: "Role unclear: review",
}
CATEGORY_QUESTIONS = {
    Category.CONFIGURATION: "Does your configuration match this?",
    Category.USAGE: "Does your application do this?",
    Category.ACCESS: "Could an attacker have this access?",
    Category.PLATFORM: "Does your environment match this?",
}
GROUP_HEADINGS = {
    GroupOperator.ALL: "All of these must hold",
    GroupOperator.ANY: "Any one of these is enough",
    GroupOperator.UNRESOLVED: "Related conditions: logic unclear, review",
}
STATUS_MESSAGES = {
    DocumentStatus.HAS_CONDITIONS: None,
    DocumentStatus.NO_EXPLICIT_CONDITION: (
        "No explicit conditions found. This does not mean the conditions do not apply: "
        "the advisory text may simply not state them."
    ),
    DocumentStatus.UNSUPPORTED_STRUCTURE: (
        "This advisory has structure the system cannot represent. Review the text directly."
    ),
}


@dataclass(frozen=True)
class Piece:
    text: str
    condition: str | None = None
    category: str | None = None


@dataclass
class RenderedBlock:
    kind: str
    level: int
    list_id: int | None
    ordered: bool
    pieces: list[Piece] = field(default_factory=list)


@dataclass(frozen=True)
class Item:
    id: str
    surface: str
    category: str
    role: str
    question: str
    confidence: float | None
    flagged: bool


@dataclass(frozen=True)
class Section:
    heading: str
    operator: str | None  # ALL/ANY/UNRESOLVED for a group, None for loose items
    items: list[Item]


def _blocks(doc: PreprocessedDocument, extraction: Extraction) -> list[RenderedBlock]:
    spans = sorted(extraction.conditions, key=lambda c: c.span)
    out: list[RenderedBlock] = []
    for block in doc.canonical.blocks:
        rendered = RenderedBlock(block.kind.value, block.level, block.list_id, block.ordered)
        cursor = block.start
        for cond in spans:
            start, end = cond.span
            if end <= block.start or start >= block.end:
                continue
            if start > cursor:
                rendered.pieces.append(Piece(doc.text[cursor:start]))
            rendered.pieces.append(Piece(doc.text[start:end], cond.id, cond.category.value.lower()))
            cursor = end
        if cursor < block.end:
            rendered.pieces.append(Piece(doc.text[cursor : block.end]))
        out.append(rendered)
    return out


@dataclass
class Node:
    """A top-level element: a single block, or a list with its items (and nested code)."""

    kind: str  # "block" or "list"
    blocks: list[RenderedBlock]
    ordered: bool = False


def _nodes(blocks: list[RenderedBlock]) -> list[Node]:
    nodes: list[Node] = []
    for block in blocks:
        if block.list_id is None:
            nodes.append(Node("block", [block]))
        elif nodes and nodes[-1].kind == "list" and nodes[-1].blocks[0].list_id == block.list_id:
            nodes[-1].blocks.append(block)
        else:
            nodes.append(Node("list", [block], block.ordered))
    return nodes


def _sections(doc: PreprocessedDocument, extraction: Extraction) -> list[Section]:
    flagged = {flag.split(":", 1)[1] for flag in extraction.review_flags if ":" in flag}
    items = {
        c.id: Item(
            c.id,
            doc.text[c.span[0] : c.span[1]],
            c.category.value,
            c.role.value,
            CATEGORY_QUESTIONS[c.category],
            c.confidence,
            c.id in flagged,
        )
        for c in extraction.conditions
    }
    sections: list[Section] = []
    grouped: set[str] = set()
    for group in extraction.groups:
        members = [items[m] for m in group.members if m in items]
        grouped.update(group.members)
        roles = {m.role for m in members}
        role_note = f" ({ROLE_HEADINGS[Role(roles.pop())].lower()})" if len(roles) == 1 else ""
        heading = GROUP_HEADINGS[group.operator] + role_note
        sections.append(Section(heading, group.operator.value, members))
    for role in Role:
        loose = [i for cid, i in items.items() if cid not in grouped and i.role == role.value]
        if loose:
            sections.append(Section(ROLE_HEADINGS[role], None, loose))
    return sections


def _script_json(payload: dict[str, Any]) -> str:
    """JSON safe to place inside a <script> element."""
    return (
        json.dumps(payload, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


_ENV = Environment(
    loader=PackageLoader("triggermap.serve", "templates"),
    autoescape=select_autoescape(["html", "j2"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_review(
    doc: PreprocessedDocument,
    extraction: Extraction,
    *,
    title: str,
    source_url: str | None = None,
    packages: tuple[str, ...] = (),
) -> str:
    sections = _sections(doc, extraction)
    payload = {
        "advisory_id": extraction.advisory_id,
        "title": title,
        "source_url": source_url,
        "content_hash": extraction.content_hash,
        "preprocessing_version": extraction.preprocessing_version,
        "model_id": extraction.model_id,
        "document_status": extraction.document_status.value,
        "groups": [g.model_dump(mode="json") for g in extraction.groups],
        "conditions": [
            {
                **c.model_dump(mode="json", exclude_none=True),
                "surface": doc.text[c.span[0] : c.span[1]],
                "raw_span": list(doc.canonical.to_raw(*c.span)),
            }
            for c in extraction.conditions
        ],
        "review_flags": list(extraction.review_flags),
    }
    return _ENV.get_template("review.html.j2").render(
        title=title,
        advisory_id=extraction.advisory_id,
        source_url=source_url,
        packages=packages,
        nodes=_nodes(_blocks(doc, extraction)),
        sections=sections,
        status_message=STATUS_MESSAGES[extraction.document_status],
        extraction=extraction,
        counts={role.value: sum(c.role is role for c in extraction.conditions) for role in Role},
        payload=_script_json(payload),
    )
