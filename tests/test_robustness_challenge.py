import json
from pathlib import Path
from typing import Any

import pytest

from triggermap.eval.challenge import ChallengeItem, load, resolve, score
from triggermap.eval.robustness import PERTURBATIONS, measure, render, signature
from triggermap.models.rules.extractor import RuleExtractor
from triggermap.text.preprocessing import compose_raw, preprocess

CANONICAL_PRESERVING = [
    "crlf",
    "bullet_style",
    "extra_blank_lines",
    "rewrap",
    "backtick_identifiers",
]


@pytest.mark.parametrize("name", CANONICAL_PRESERVING)
def test_formatting_perturbations_keep_canonical_text(
    name: str, aiohttp_advisory: dict[str, Any], flask_advisory: dict[str, Any]
) -> None:
    for advisory in (aiohttp_advisory, flask_advisory):
        raw = compose_raw(advisory["summary"], advisory["details"])
        assert preprocess(PERTURBATIONS[name](raw)).text == preprocess(raw).text


def test_code_blocks_are_never_perturbed() -> None:
    raw = "Text with debug_mode on.\n```\nx_y = 'a'  # it's\n```"
    for name, perturb in PERTURBATIONS.items():
        if name != "crlf":
            assert "x_y = 'a'  # it's" in perturb(raw), name


def test_rules_are_consistent_on_fixtures(
    aiohttp_advisory: dict[str, Any], flask_advisory: dict[str, Any]
) -> None:
    raws = {
        "a": compose_raw(aiohttp_advisory["summary"], aiohttp_advisory["details"]),
        "f": compose_raw(flask_advisory["summary"], flask_advisory["details"]),
    }
    results = measure(RuleExtractor(), raws)
    assert all(r.consistent == r.documents == 2 for r in results)
    report = render("t", results, {"Sample": "fixtures"})
    assert "Overall consistency: 100.0%" in report


class LengthSensitive:
    """A deliberately fragile extractor: it loses every condition when text has double spaces."""

    model_id = "fragile"

    def extract(self, doc: Any, advisory_id: Any = None) -> Any:
        extraction = RuleExtractor().extract(doc, advisory_id)
        fragile = "  " in doc.text
        return extraction.model_copy(update={"conditions": ()}) if fragile else extraction


def test_inconsistency_is_detected_and_reported() -> None:
    raws = {f"d{i}": f"Only affects deployments using the legacy API{'!' * i}." for i in range(4)}
    (result,) = measure(LengthSensitive(), raws, ["double_spaces"])
    assert result.consistent < result.documents
    assert result.examples


def test_signature_ignores_whitespace_and_quote_style() -> None:
    a, b = (
        preprocess("Only affects deployments using the app's API."),
        preprocess("Only  affects  deployments  using  the  app\u2019s  API."),
    )
    extractor = RuleExtractor()
    assert signature(extractor.extract(a), a) == signature(extractor.extract(b), b)


def item(**overrides: Any) -> dict[str, Any]:
    base = {
        "id": "neg-01a",
        "family": "negation_flip",
        "pair": "neg-01",
        "status": "verified",
        "text": "The server is vulnerable when `debug` is enabled.",
        "conditions": [
            {"surface": "debug is enabled", "category": "CONFIGURATION", "role": "REQUIRED"}
        ],
    }
    base.update(overrides)
    return base


def test_challenge_items_resolve_to_offsets() -> None:
    resolved = resolve(ChallengeItem.model_validate(item()))
    (cond,) = resolved.gold.conditions
    assert resolved.doc.text[slice(*cond.span)] == "debug is enabled"
    twice = item(
        text="If X is set or X is set.",
        conditions=[
            {"surface": "X is set", "occurrence": 2, "category": "USAGE", "role": "REQUIRED"}
        ],
    )
    (second,) = resolve(ChallengeItem.model_validate(twice)).gold.conditions
    assert second.span[0] > 10
    with pytest.raises(ValueError, match="not found"):
        resolve(
            ChallengeItem.model_validate(
                item(conditions=[{"surface": "missing", "category": "USAGE", "role": "REQUIRED"}])
            )
        )


def test_challenge_scoring_by_family_and_pair(tmp_path: Path) -> None:
    rows = [
        item(),
        item(
            id="neg-01b",
            text="The server is vulnerable even when `debug` is not enabled.",
            conditions=[],
        ),
        item(id="d-1", status="draft", pair=None),
    ]
    path = tmp_path / "set.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    items = load(path)
    verified, _ = score([r for r in items if r.item.status == "verified"], RuleExtractor())
    (family,) = verified
    assert (family.family, family.items, family.pairs) == ("negation_flip", 2, 1)
    assert 0 <= family.pairs_both_exact <= 1
    path.write_text("\n".join(json.dumps(r) for r in [rows[0], rows[0]]) + "\n")
    with pytest.raises(ValueError, match="duplicate"):
        load(path)


def test_committed_challenge_set_loads() -> None:
    root = Path(__file__).resolve().parents[1]
    items = load(root / "challenge/challenge_set.jsonl")
    assert all(r.item.status in ("draft", "verified") for r in items)
