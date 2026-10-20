from typing import Any

import pytest

from triggermap.cli import main
from triggermap.models.rules.extractor import RuleExtractor, categorize
from triggermap.schema import Category, Extraction, GroupOperator, validate_annotation
from triggermap.text.preprocessing import compose_raw, preprocess


def run(text: str) -> tuple[Extraction, list[tuple[str, str, str]]]:
    doc = preprocess(text)
    ex = RuleExtractor().extract(doc)
    assert validate_annotation(ex, doc.text) == []
    rows = [(doc.text[slice(*c.span)], c.category.value, c.role.value) for c in ex.conditions]
    return ex, rows


def test_aiohttp_impact_sentence_matches_guideline_example() -> None:
    ex, rows = run(
        "When using aiohttp as a web server and enabling static resource resolution with "
        "`follow_symlinks` set to True, it can lead to this vulnerability."
    )
    assert rows == [
        ("using aiohttp as a web server", "USAGE", "REQUIRED"),
        ("enabling static resource resolution", "USAGE", "REQUIRED"),
        ("follow_symlinks set to True", "CONFIGURATION", "REQUIRED"),
    ]
    assert [(g.operator, g.members) for g in ex.groups] == [(GroupOperator.ALL, ("c1", "c2", "c3"))]


def test_flask_list_matches_guideline_example(flask_advisory: dict[str, Any]) -> None:
    ex, rows = run(compose_raw(flask_advisory["summary"], flask_advisory["details"]))
    listed = rows[-5:]
    assert listed == [
        (
            "hosted behind a caching proxy that does not strip cookies or ignore responses "
            "with cookies",
            "PLATFORM",
            "REQUIRED",
        ),
        ("sets session.permanent = True", "CONFIGURATION", "REQUIRED"),
        (
            "does not access or modify the session at any point during a request",
            "USAGE",
            "REQUIRED",
        ),
        ("SESSION_REFRESH_EACH_REQUEST is enabled", "CONFIGURATION", "REQUIRED"),
        (
            "does not set a Cache-Control header to indicate that a page is private or should "
            "not be cached",
            "USAGE",
            "REQUIRED",
        ),
    ]
    assert ex.groups[-1].operator is GroupOperator.ALL
    assert len(ex.groups[-1].members) == 5


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "Only affects deployments using unhashed passwords in AUTH_ACCOUNTS.",
            [("using unhashed passwords in AUTH_ACCOUNTS", "USAGE", "REQUIRED")],
        ),
        (
            "The server is vulnerable unless the strict_mode option is enabled.",
            [("the strict_mode option is enabled", "CONFIGURATION", "EXCEPTION")],
        ),
        (
            "It can read files even when symlinks are not present.",
            [("symlinks", "PLATFORM", "NOT_REQUIRED")],
        ),
        (
            "Code runs, regardless of whether the sandbox is enabled.",
            [("the sandbox is enabled", "CONFIGURATION", "NOT_REQUIRED")],
        ),
        (
            "An unauthenticated attacker can read any file.",
            [("unauthenticated", "ACCESS", "NOT_REQUIRED")],
        ),
        (
            "This allows an authenticated user with edit permission to run code.",
            [("authenticated user with edit permission", "ACCESS", "REQUIRED")],
        ),
        (
            "The data is exposed when the client uses the legacy API or when debug_mode=True.",
            [
                ("the client uses the legacy API", "USAGE", "REQUIRED"),
                ("debug_mode=True", "CONFIGURATION", "REQUIRED"),
            ],
        ),
    ],
)
def test_pattern_families(text: str, expected: list[tuple[str, str, str]]) -> None:
    assert run(text)[1] == expected


@pytest.mark.parametrize(
    "text",
    [
        "A heap overflow occurs when the length field exceeds the buffer.",  # mechanism only
        "If exploited, an attacker can execute arbitrary code.",
        "Users should upgrade to 2.3.2. If you cannot upgrade, disable the option.",
        "Versions before 3.9.2 are affected.",
        "Commands are chained when using |.",
    ],
)
def test_non_conditions_are_not_extracted(text: str) -> None:
    ex, rows = run(text)
    assert rows == []
    assert ex.document_status.value == "NO_EXPLICIT_CONDITION"


def test_workaround_sections_are_skipped() -> None:
    _, rows = run("### Workarounds\nIf you use follow_symlinks=True, disable the option.")
    assert rows == []


def test_any_group_from_or() -> None:
    ex, _ = run("Exposure happens when using the CLI or using the HTTP server.")
    assert [g.operator for g in ex.groups] == [GroupOperator.ANY]


def test_low_confidence_flags() -> None:
    ex, _ = run("Applications that call load() with trust_remote_code=True are at risk.")
    assert ex.conditions[0].confidence is not None and ex.conditions[0].confidence < 0.5
    assert ex.review_flags == ("low_confidence:c1",)


@pytest.mark.parametrize(
    "text, category",
    [
        ("an authenticated admin", Category.ACCESS),
        ("follow_symlinks set to True", Category.CONFIGURATION),
        ("running on Windows", Category.PLATFORM),
        ("calls yaml.load on input", Category.USAGE),
    ],
)
def test_categorize(text: str, category: Category) -> None:
    assert categorize(text) is category


def test_predict_cli_writes_valid_jsonl(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    from tests.factories import make_doc

    processed = tmp_path / "processed"
    processed.mkdir()
    docs = [
        make_doc("GHSA-2222-2222-2222", "Only affects deployments using the legacy API."),
        make_doc("GHSA-3333-3333-3333", "A crash occurs."),
    ]
    (processed / "advisories.jsonl").write_text("".join(d.model_dump_json() + "\n" for d in docs))
    out = tmp_path / "preds.jsonl"
    assert main(["predict", "--processed", str(processed), "--out", str(out)]) == 0
    lines = [Extraction.model_validate_json(line) for line in out.read_text().splitlines()]
    assert [e.advisory_id for e in lines] == ["GHSA-2222-2222-2222", "GHSA-3333-3333-3333"]
    assert lines[0].conditions and not lines[1].conditions
    assert lines[0].content_hash == docs[0].content_hash
    assert compose_raw(docs[0].summary, docs[0].details)  # same composition as ingestion
