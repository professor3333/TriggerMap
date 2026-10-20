"""Exports of a saved review: machine-readable JSON and a readable Markdown record."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

PROVENANCE = (
    "content_hash",
    "model_id",
    "preprocessing_version",
    "review_policy_version",
    "created_at",
)


def _with_surfaces(review: dict[str, Any]) -> list[dict[str, Any]]:
    text = review["text"]
    return [
        {**c, "surface": text[c["span"][0] : c["span"][1]]} for c in review["state"]["conditions"]
    ]


def review_json(review: dict[str, Any]) -> str:
    record = {
        "review_format": 1,
        "exported_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "review_id": review["id"],
        "advisory_id": review["advisory_id"],
        "title": review["title"],
        "source_url": review["source_url"],
        **{key: review[key] for key in PROVENANCE},
        "advisory_changed": review["advisory_changed"],
        "document_status": review["state"]["document_status"],
        "conditions": _with_surfaces(review),
        "groups": review["state"]["groups"],
        "notes": review["state"].get("notes"),
        "history": review["history"],
    }
    return json.dumps(record, indent=2, ensure_ascii=False)


def _cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def review_markdown(review: dict[str, Any]) -> str:
    conditions = _with_surfaces(review)
    by_id = {c["id"]: c for c in conditions}
    lines = [f"# Exposure review: {_cell(review['title'])}", ""]
    if review["advisory_id"]:
        lines.append(f"- Advisory: {review['advisory_id']} ({review['source_url']})")
    lines += [
        f"- Review: `{review['id']}`, created {review['created_at']}, "
        f"{len(review['history'])} saved version(s)",
        f"- Model `{review['model_id']}`, preprocessing `{review['preprocessing_version']}`, "
        f"review policy `{review['review_policy_version']}`",
        f"- Advisory text SHA-256: `{review['content_hash']}`",
        f"- Document status: {review['state']['document_status']}",
    ]
    if review["advisory_changed"]:
        lines.append(
            "- **The advisory has changed since this review was made.** Re-extract and re-check."
        )
    lines.append("")
    if not conditions:
        lines += [
            "No explicit conditions were found. This does not mean the conditions do not "
            "apply: the advisory may simply not state them.",
            "",
        ]

    def row(c: dict[str, Any]) -> str:
        origin = " (added by reviewer)" if c["source"] == "human" else ""
        return (
            f"| {c['answer']} | {c['category']} | {c['role']} | {_cell(c['surface'])}{origin} "
            f"| {c['span'][0]}-{c['span'][1]} |"
        )

    header = ["| Answer | Category | Role | Evidence | Characters |", "|---|---|---|---|---|"]
    grouped: set[str] = set()
    for group in review["state"]["groups"]:
        meaning = {"ALL": "all must hold", "ANY": "any one suffices"}.get(
            group["operator"], "logic unclear"
        )
        lines += [f"## {group['operator']} group ({meaning})", "", *header]
        lines += [row(by_id[m]) for m in group["members"] if m in by_id]
        lines.append("")
        grouped.update(group["members"])
    rest = [c for c in conditions if c["id"] not in grouped]
    if rest:
        lines += ["## Conditions", "", *header, *(row(c) for c in rest), ""]
    if review["state"].get("notes"):
        lines += ["## Reviewer notes", "", review["state"]["notes"], ""]
    lines += ["## History", "", "| Version | Saved | Note |", "|---:|---|---|"]
    lines += [
        f"| {h['seq']} | {h['created_at']} | {_cell(h['note'] or h['kind'])} |"
        for h in review["history"]
    ]
    lines.append("")
    return "\n".join(lines)
