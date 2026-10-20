import json
from pathlib import Path

import pytest

pytest.importorskip("fastapi")

from triggermap.serve import release as releases
from triggermap.serve.app import Service, Settings, release_settings

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "configs/review_policy.yaml"


def test_create_activate_and_rollback(tmp_path: Path) -> None:
    root = tmp_path / "releases"
    r1 = releases.create_release(root, "r1", "img:1", "rules", None, POLICY)
    manifest = json.loads((r1 / "release.json").read_text())
    assert manifest["model_id"] == "rules-2" and len(manifest["weights_sha256"]) == 64
    assert manifest["review_policy_version"] == "review-policy-0"
    assert (r1 / "review_policy.yaml").exists() and not (r1 / "model").exists()
    with pytest.raises(FileExistsError):
        releases.create_release(root, "r1", "img:1", "rules", None, POLICY)
    with pytest.raises(ValueError, match="bundle"):
        releases.create_release(root, "r9", "img:9", "crf", None, POLICY)

    releases.create_release(root, "r2", "img:2", "rules", None, POLICY)
    assert releases.current_release(root) is None
    releases.activate(root, "r1")
    releases.activate(root, "r2")
    assert releases.current_release(root) == "r2"
    assert (root / ".env").read_text() == "TRIGGERMAP_IMAGE=img:2\nTRIGGERMAP_RELEASE=r2\n"
    assert (root / "current" / "release.json").exists()  # the pointer resolves
    assert releases.previous_release(root) == "r1"

    back = releases.rollback(root)
    assert back["release_id"] == "r1" and releases.current_release(root) == "r1"
    assert "img:1" in (root / ".env").read_text()
    assert releases.history(root) == ["r1", "r2", "r1"]


def test_rollback_needs_a_previous_release(tmp_path: Path) -> None:
    root = tmp_path / "releases"
    releases.create_release(root, "only", "img", "rules", None, POLICY)
    releases.activate(root, "only")
    with pytest.raises(RuntimeError, match="no previous release"):
        releases.rollback(root)


def test_release_settings_and_integrity_guard(tmp_path: Path) -> None:
    root = tmp_path / "releases"
    r1 = releases.create_release(root, "r1", "img", "rules", None, POLICY)
    settings = Settings(database=tmp_path / "db.sqlite", **release_settings(r1))
    assert settings.release == "r1" and settings.model == "rules" and settings.model_dir is None
    assert Service(settings).weights_sha256 == settings.expected_weights_sha256
    tampered = settings.model_copy(update={"expected_weights_sha256": "0" * 64})
    with pytest.raises(RuntimeError, match="refusing to serve"):
        Service(tampered)


def test_crf_release_copies_the_bundle(tmp_path: Path) -> None:
    pytest.importorskip("pycrfsuite")
    from tests.synthetic import TRAIN_VOCAB, make_dataset
    from triggermap.models.crf.model import CrfExtractor

    data = make_dataset(12, TRAIN_VOCAB, seed=1, prefix="train")
    bundle = tmp_path / "bundle"
    CrfExtractor.train([(p, r) for _, p, r in data], bundle, model_id="crf-x", use_pos=False)
    target = releases.create_release(tmp_path / "rel", "c1", "img", "crf", bundle, POLICY)
    manifest = json.loads((target / "release.json").read_text())
    assert manifest["model_id"] == "crf-x" and (target / "model/tagger.crfsuite").exists()
    settings = Settings(database=tmp_path / "db.sqlite", **release_settings(target))
    assert Service(settings).extractor.model_id == "crf-x"
