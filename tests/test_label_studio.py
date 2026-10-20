from typing import Any

import pytest

from tests.factories import make_doc
from triggermap.annotate.importer import import_export, render_report, write_records
from triggermap.annotate.label_studio import build_task, convert_task, utf16_to_codepoint
from triggermap.schema import Category, DocumentStatus, GroupOperator, Role

AID = "GHSA-5h86-8mv2-jq9f"
SENTENCE = (
    "When using aiohttp as a web server and enabling static resource resolution with "
    "`follow_symlinks` set to True, it can lead to this vulnerability. Symlinks need not exist."
)


def region(rid: str, start: int, end: int, text: str, label: str, role: str | None) -> list[Any]:
    value = {"start": start, "end": end, "text": text}
    items: list[Any] = [
        {
            "id": rid,
            "from_name": "condition",
            "to_name": "text",
            "type": "labels",
            "value": {**value, "labels": [label]},
        }
    ]
    if role:
        items.append(
            {
                "id": rid,
                "from_name": "role",
                "to_name": "text",
                "type": "choices",
                "value": {**value, "choices": [role]},
            }
        )
    return items


def relation(a: str, b: str, label: str) -> dict[str, Any]:
    return {"from_id": a, "to_id": b, "type": "relation", "direction": "right", "labels": [label]}


def status(value: str) -> dict[str, Any]:
    return {
        "id": "s",
        "from_name": "document_status",
        "to_name": "text",
        "type": "choices",
        "value": {"choices": [value]},
    }


@pytest.fixture
def corpus() -> dict[str, Any]:
    return {AID: make_doc(AID, SENTENCE, ("aiohttp",), summary="aiohttp traversal")}


def task_with(corpus: dict[str, Any], results: list[Any], **extra: Any) -> dict[str, Any]:
    task = build_task(corpus[AID], order=0)
    task["annotations"] = [
        {"id": 1, "result": results, "lead_time": 300.0, "updated_at": "2026-10-21T10:00:00Z"}
    ]
    task.update(extra)
    return task


def offsets(text: str, surface: str) -> tuple[int, int]:
    start = text.index(surface)
    return start, start + len(surface)


def reference_results(text: str) -> list[Any]:
    spans = {
        "r1": ("using aiohttp as a web server", "USAGE", "REQUIRED"),
        "r2": ("enabling static resource resolution", "USAGE", "REQUIRED"),
        "r3": ("follow_symlinks set to True", "CONFIGURATION", "REQUIRED"),
        "r4": ("Symlinks need not exist", "PLATFORM", "NOT_REQUIRED"),
    }
    results: list[Any] = []
    for rid, (surface, label, role) in spans.items():
        results += region(rid, *offsets(text, surface), surface, label, role)
    return [
        *results,
        relation("r2", "r1", "ALL"),
        relation("r2", "r3", "ALL"),
        status("HAS_CONDITIONS"),
    ]


def test_reference_annotation_converts_cleanly(corpus: dict[str, Any]) -> None:
    task = build_task(corpus[AID], order=0)
    text = task["data"]["text"]
    conv = convert_task(task_with(corpus, reference_results(text)), corpus, "pilot-1", "A1")
    assert conv.issues == []
    assert conv.record is not None
    record = conv.record
    assert record.document_status is DocumentStatus.HAS_CONDITIONS
    assert [c.id for c in record.conditions] == ["c1", "c2", "c3", "c4"]
    assert [text[slice(*c.span)] for c in record.conditions][2] == "follow_symlinks set to True"
    assert record.conditions[2].category is Category.CONFIGURATION
    assert record.conditions[3].role is Role.NOT_REQUIRED
    assert len(record.groups) == 1
    assert record.groups[0].operator is GroupOperator.ALL
    assert record.groups[0].members == ("c1", "c2", "c3")
    assert record.annotator == "A1"
    assert conv.lead_time == 300.0


def test_utf16_offsets_are_converted() -> None:
    text = "😀 when debug is enabled"
    assert utf16_to_codepoint(text, 3) == 2  # emoji is two UTF-16 units
    assert utf16_to_codepoint(text, 0) == 0
    assert utf16_to_codepoint(text, 99) == len(text)


def test_utf16_offsets_in_an_export(corpus: dict[str, Any]) -> None:
    corpus[AID] = make_doc(AID, "😀 When debug is enabled.", ("aiohttp",), summary="s")
    task = build_task(corpus[AID], order=0)
    text = task["data"]["text"]
    start = text.index("debug is enabled")
    results = [
        *region("r1", start + 1, start + 17, "debug is enabled", "CONFIGURATION", "REQUIRED"),
        status("HAS_CONDITIONS"),
    ]
    conv = convert_task(task_with(corpus, results), corpus, "pilot-1", "A1")
    assert conv.issues == []
    assert conv.record is not None
    assert text[slice(*conv.record.conditions[0].span)] == "debug is enabled"


def test_whitespace_is_trimmed_and_reported(corpus: dict[str, Any]) -> None:
    text = build_task(corpus[AID], order=0)["data"]["text"]
    start, end = offsets(text, " using aiohttp as a web server ")
    results = [
        *region("r1", start, end, text[start:end], "USAGE", "REQUIRED"),
        status("HAS_CONDITIONS"),
    ]
    conv = convert_task(task_with(corpus, results), corpus, "pilot-1", "A1")
    assert conv.issues == []
    assert conv.record is not None
    assert text[slice(*conv.record.conditions[0].span)] == "using aiohttp as a web server"
    assert any("trimmed" in note for note in conv.notes)


@pytest.mark.parametrize(
    "mutate, code",
    [
        (
            lambda r, t: [{**r[0], "value": {**r[0]["value"], "text": "nope"}}, *r[1:]],
            "surface_mismatch",
        ),
        (lambda r, t: [x for x in r if x.get("from_name") != "role"], "missing_role"),
        (lambda r, t: [*r, relation("r1", "r4", "ANY")], "contradictory_group"),
        (lambda r, t: [x for x in r if x.get("from_name") != "document_status"], "missing_status"),
        (lambda r, t: [*r, {**relation("r1", "r4", "ALL"), "labels": []}], "relation_label_count"),
    ],
)
def test_problems_are_reported_not_fixed(corpus: dict[str, Any], mutate: Any, code: str) -> None:
    text = build_task(corpus[AID], order=0)["data"]["text"]
    results = mutate(reference_results(text), text)
    conv = convert_task(task_with(corpus, results), corpus, "pilot-1", "A1")
    assert code in [issue.code for issue in conv.issues]


def test_status_mismatch_from_validator(corpus: dict[str, Any]) -> None:
    text = build_task(corpus[AID], order=0)["data"]["text"]
    results = [*reference_results(text)[:-1], status("NO_EXPLICIT_CONDITION")]
    conv = convert_task(task_with(corpus, results), corpus, "pilot-1", "A1")
    assert [i.code for i in conv.issues] == ["status_mismatch"]


def test_stale_and_unknown_tasks(corpus: dict[str, Any]) -> None:
    task = task_with(corpus, [status("NO_EXPLICIT_CONDITION")])
    task["data"]["content_hash"] = "0" * 64
    assert convert_task(task, corpus, "pilot-1", "A1").issues[0].code == "stale_task"
    task["data"]["advisory_id"] = "GHSA-2222-2222-2222"
    assert convert_task(task, corpus, "pilot-1", "A1").issues[0].code == "unknown_advisory"
    empty = build_task(corpus[AID], order=0)
    assert convert_task(empty, corpus, "pilot-1", "A1").issues[0].code == "not_annotated"


def test_cancelled_annotations_are_ignored(corpus: dict[str, Any]) -> None:
    task = task_with(corpus, [status("NO_EXPLICIT_CONDITION")])
    task["annotations"][0]["was_cancelled"] = True
    assert convert_task(task, corpus, "pilot-1", "A1").issues[0].code == "not_annotated"


def test_import_writes_only_clean_records_and_reports(
    corpus: dict[str, Any], tmp_path: Any
) -> None:
    text = build_task(corpus[AID], order=0)["data"]["text"]
    good = task_with(corpus, reference_results(text))
    bad = task_with(corpus, [status("HAS_CONDITIONS")])
    conversions = import_export([good, bad], corpus, "pilot-1", "A1")
    out = tmp_path / "pilot.jsonl"
    assert write_records(conversions, out) == 1
    assert len(out.read_text().splitlines()) == 1
    report = render_report(conversions, {AID: {"stratum": "random", "words": 50}}, 1)
    assert "status_mismatch" in report
    assert "Median minutes per document: 5.0" in report
    assert "| REQUIRED | 3 |" in report


def test_real_label_studio_export_round_trip(aiohttp_advisory: dict[str, Any]) -> None:
    """A JSON export produced by Label Studio 1.23.2 with our config converts cleanly."""
    import json
    from pathlib import Path

    path = Path(__file__).parent / "fixtures/label_studio/export_aiohttp_ls-1.23.2.json"
    export = json.loads(path.read_text(encoding="utf-8"))
    doc = make_doc(
        AID, aiohttp_advisory["details"], ("aiohttp",), summary=aiohttp_advisory["summary"]
    )
    (conv,) = import_export(export, {AID: doc}, "verify", "A1")
    assert conv.issues == []
    assert conv.record is not None
    text = export[0]["data"]["text"]
    spans = [(text[slice(*c.span)], c.category.value, c.role.value) for c in conv.record.conditions]
    assert spans == [
        ("symlinks", "PLATFORM", "NOT_REQUIRED"),
        ("using aiohttp as a web server", "USAGE", "REQUIRED"),
        ("enabling static resource resolution", "USAGE", "REQUIRED"),
        ("follow_symlinks set to True", "CONFIGURATION", "REQUIRED"),
    ]
    assert [(g.operator.value, g.members) for g in conv.record.groups] == [
        ("ALL", ("c2", "c3", "c4"))
    ]
    assert conv.record.notes == "verification note"
    assert conv.lead_time == 123.4
