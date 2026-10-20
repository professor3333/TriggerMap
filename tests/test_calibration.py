import json
import random
from pathlib import Path

import pytest

from triggermap.eval.calibration import (
    Calibrator,
    calibration_split,
    choose_threshold,
    expected_calibration_error,
    fit_isotonic,
    fit_platt,
    precision_interval,
    reliability,
)
from triggermap.models.rules.extractor import RuleExtractor
from triggermap.serve.policy import ReviewPolicy, apply_policy, load_policy, save_policy
from triggermap.text.preprocessing import preprocess


def overconfident(n: int = 4000, seed: int = 0) -> list[tuple[float, bool]]:
    """A model whose true accuracy is confidence squared (systematically overconfident)."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        p = rng.uniform(0.3, 0.99)
        out.append((p, rng.random() < p * p))
    return out


def test_platt_and_isotonic_reduce_calibration_error() -> None:
    train, test = overconfident(seed=1), overconfident(seed=2)
    raw = expected_calibration_error(test)
    for calibrator in (fit_platt(train), fit_isotonic(train)):
        calibrated = [(calibrator(p), ok) for p, ok in test]
        assert expected_calibration_error(calibrated) < raw / 3
        restored = Calibrator.from_dict(json.loads(json.dumps(calibrator.to_dict())))
        assert restored(0.7) == pytest.approx(calibrator(0.7))


def test_isotonic_is_monotone() -> None:
    calibrator = fit_isotonic([(0.1, True), (0.2, False), (0.3, False), (0.9, True), (0.95, True)])
    xs = [0.0, 0.1, 0.2, 0.5, 0.9, 1.0]
    values = [calibrator(x) for x in xs]
    assert values == sorted(values)
    assert calibrator(0.95) == 1.0


def test_reliability_and_ece() -> None:
    perfect = [(0.8, True)] * 8 + [(0.8, False)] * 2
    assert expected_calibration_error(perfect, bins=1) == pytest.approx(0.0)
    assert expected_calibration_error([(0.9, False)] * 5, bins=1) == pytest.approx(0.9)
    bins = reliability(overconfident(100), bins=4)
    assert sum(b.count for b in bins) == 100 and len(bins) == 4


def test_choose_threshold_maximises_coverage_at_target() -> None:
    scored = [(0.95, True), (0.9, True), (0.85, True), (0.8, False), (0.7, True), (0.6, False)]
    choice = choose_threshold(scored, gold_total=5, target_precision=0.8)
    assert choice is not None
    assert (choice.threshold, choice.kept) == (0.7, 5)
    assert choice.precision == pytest.approx(0.8) and choice.retained_recall == pytest.approx(0.8)
    assert choose_threshold([(0.5, False)], 1, 0.9) is None
    assert choose_threshold([], 1, 0.9) is None


def test_precision_interval_and_split() -> None:
    per_doc = {"a": [(0.9, True), (0.4, False)], "b": [(0.8, True)], "c": [(0.95, False)]}
    low, high = precision_interval(per_doc, 0.7, samples=300)
    assert 0.0 <= low <= 2 / 3 <= high <= 1.0
    calib, held = calibration_split(
        ["a", "b", "c", "d"], {"a": "g1", "b": "g1", "c": "g2", "d": "g3"}
    )
    assert set(calib) | set(held) == {"a", "b", "c", "d"} and not set(calib) & set(held)
    assert ("a" in calib) == ("b" in calib)  # groups stay together


def test_policy_flags_reasons_and_round_trips(tmp_path: Path) -> None:
    text = (
        "### Impact\nOnly affects deployments using the legacy API.\n"
        "It is exploitable unless strict_mode is enabled.\n\n"
        "### Workarounds\nOnly affects deployments using debug_mode=True as a fallback."
    )
    doc = preprocess(text)
    extraction = RuleExtractor().extract(doc)
    # The rules skip workaround sections; a learned model might not, so add such a prediction.
    from triggermap.schema import Category, Condition, Role

    start = doc.text.index("debug_mode=True")
    model_like = Condition(
        id=f"c{len(extraction.conditions) + 1}",
        span=(start, start + len("debug_mode=True")),
        category=Category.CONFIGURATION,
        role=Role.REQUIRED,
        source="model",
        confidence=0.9,
    )
    extraction = extraction.model_copy(update={"conditions": (*extraction.conditions, model_like)})
    reasons = lambda ex, cid: [  # noqa: E731
        f.split(":")[2] for f in ex.review_flags if f.startswith(f"review_required:{cid}:")
    ]

    uncalibrated = apply_policy(extraction, doc, ReviewPolicy(version="p0", model_id="rules-1"))
    by_surface = {doc.text[slice(*c.span)]: c.id for c in uncalibrated.conditions}
    legacy = by_surface["using the legacy API"]
    assert reasons(uncalibrated, legacy) == ["uncalibrated"]
    strict = by_surface["strict_mode is enabled"]
    assert set(reasons(uncalibrated, strict)) >= {"role_exception", "negation"}
    debug = next(cid for s, cid in by_surface.items() if "debug_mode" in s)
    assert "workaround_section" in reasons(uncalibrated, debug)
    assert "review_policy:p0" in uncalibrated.review_flags

    accepting = ReviewPolicy(
        version="p1",
        model_id="rules-1",
        calibration={"method": "platt", "a": 1.0, "b": 2.0},
        accept_threshold=0.5,
    )
    calibrated = apply_policy(extraction, doc, accepting)
    assert reasons(calibrated, legacy) == []  # confident, plain requirement: accepted
    assert calibrated.conditions[0].confidence != extraction.conditions[0].confidence
    path = tmp_path / "policy.yaml"
    save_policy(accepting, path)
    assert load_policy(path) == accepting
    assert path.read_text().startswith("# Review policy")


def test_committed_default_policy_is_uncalibrated() -> None:
    policy = load_policy(Path(__file__).resolve().parents[1] / "configs/review_policy.yaml")
    assert policy.accept_threshold is None and policy.calibration == {"method": "identity"}


def test_calibrate_cli(tmp_path: Path) -> None:
    from tests.factories import write_split_manifest
    from tests.synthetic import TRAIN_VOCAB, make_dataset
    from triggermap.cli import main

    data = make_dataset(40, TRAIN_VOCAB, seed=3, prefix="train")
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(r.model_dump_json() + "\n" for _, _, r in data))
    pred = tmp_path / "pred.jsonl"
    extractor = RuleExtractor()
    pred.write_text(
        "".join(extractor.extract(p, r.advisory_id).model_dump_json() + "\n" for _, p, r in data)
    )
    split = write_split_manifest(
        tmp_path / "split.json", {r.advisory_id: "dev" for _, _, r in data}
    )
    out = tmp_path / "policy.yaml"
    args = ["calibrate", "--gold", str(gold), "--pred", str(pred), "--split-manifest", str(split)]
    assert main([*args, "--target-precision", "0.5", "--out", str(out)]) == 0
    policy = load_policy(out)
    assert policy.calibration["method"] == "platt"
    assert policy.measured["calibration_documents"] + policy.measured["held_out_documents"] == 40
    assert "ece_calibrated_held_out" in policy.measured
