"""Release directories, the active-release pointer, and rollback.

Layout under a releases root (for example ``deploy/releases``):

    <release_id>/release.json        image, model kind and id, weights digest, versions
    <release_id>/review_policy.yaml  thresholds and calibration that belong to this model
    <release_id>/model/              model bundle (absent for the rules model)
    current -> <release_id>          the active release (an atomically replaced symlink)
    .env                             TRIGGERMAP_IMAGE and TRIGGERMAP_RELEASE for compose
    history.jsonl                    every activation, used for rollback

Rolling back switches the pointer *and* the image together, so an application image is never
paired with a model bundle, tokenizer, preprocessing version or thresholds it was not
released with.
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from triggermap import __version__
from triggermap.serve.app import weights_digest
from triggermap.serve.policy import load_policy
from triggermap.text.preprocessing import PREPROCESSING_VERSION


def _model_id(kind: str, model_dir: Path | None) -> str:
    if kind == "rules":
        from triggermap.models.rules.extractor import MODEL_ID

        return MODEL_ID
    assert model_dir is not None
    return str(json.loads((model_dir / "metadata.json").read_text())["model_id"])


def create_release(
    root: Path,
    release_id: str,
    image: str,
    model_kind: str,
    model_dir: Path | None,
    policy: Path,
) -> Path:
    target = root / release_id
    if target.exists():
        raise FileExistsError(f"release {release_id} exists; releases are immutable")
    if model_kind != "rules" and model_dir is None:
        raise ValueError(f"a {model_kind} release needs a model bundle")
    target.mkdir(parents=True)
    if model_dir is not None:
        shutil.copytree(model_dir, target / "model")
    shutil.copy2(policy, target / "review_policy.yaml")
    bundle = target / "model" if model_dir is not None else None
    loaded_policy = load_policy(target / "review_policy.yaml")
    manifest = {
        "release_id": release_id,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "image": image,
        "app_version": __version__,
        "model_kind": model_kind,
        "model_id": _model_id(model_kind, bundle),
        "weights_sha256": weights_digest(model_kind, bundle),
        "preprocessing_version": PREPROCESSING_VERSION,
        "review_policy_version": loaded_policy.version,
        "accept_threshold": loaded_policy.accept_threshold,
    }
    (target / "release.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return target


def read_release(root: Path, release_id: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((root / release_id / "release.json").read_text())
    return data


def current_release(root: Path) -> str | None:
    link = root / "current"
    return os.readlink(link) if link.is_symlink() else None


def activate(root: Path, release_id: str) -> dict[str, Any]:
    """Point ``current`` at a release and write the compose env file, atomically."""
    manifest = read_release(root, release_id)
    tmp = root / ".current.tmp"
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    tmp.symlink_to(release_id)
    os.replace(tmp, root / "current")
    env_tmp = root / ".env.tmp"
    env_tmp.write_text(
        f"TRIGGERMAP_IMAGE={manifest['image']}\nTRIGGERMAP_RELEASE={manifest['release_id']}\n"
    )
    os.replace(env_tmp, root / ".env")
    with (root / "history.jsonl").open("a") as fh:
        stamp = datetime.now(UTC).isoformat(timespec="seconds")
        fh.write(json.dumps({"release_id": release_id, "activated_at": stamp}) + "\n")
    return manifest


def history(root: Path) -> list[str]:
    path = root / "history.jsonl"
    if not path.exists():
        return []
    return [json.loads(line)["release_id"] for line in path.read_text().splitlines() if line]


def previous_release(root: Path) -> str | None:
    """The release that was active before the current one."""
    current = current_release(root)
    for release_id in reversed(history(root)):
        if release_id != current:
            return release_id
    return None


def rollback(root: Path) -> dict[str, Any]:
    target = previous_release(root)
    if target is None:
        raise RuntimeError("no previous release to roll back to")
    return activate(root, target)
