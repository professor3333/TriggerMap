"""Fetch a pinned, sparse snapshot of the GitHub Advisory Database."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_URL = "https://github.com/github/advisory-database.git"
REVIEWED_DIR = "advisories/github-reviewed"


def _git(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True, timeout=1800
    )
    return result.stdout.strip()


def fetch_snapshot(dest: Path, commit: str | None = None) -> str:
    """Clone (or reuse) a sparse snapshot of reviewed advisories; return its commit SHA.

    With ``commit``, the snapshot is moved to exactly that commit so a previous corpus
    can be reconstructed. Without it, an existing snapshot is reused unchanged.
    """
    if not (dest / ".git").exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        _git("clone", "--depth", "1", "--filter=blob:none", "--sparse", REPO_URL, str(dest))
        _git("sparse-checkout", "set", REVIEWED_DIR, cwd=dest)
    if commit is not None and snapshot_commit(dest) != commit:
        _git("fetch", "--depth", "1", "origin", commit, cwd=dest)
        _git("checkout", "--detach", commit, cwd=dest)
    return snapshot_commit(dest)


def snapshot_commit(dest: Path) -> str:
    return _git("rev-parse", "HEAD", cwd=dest)


def snapshot_commit_date(dest: Path) -> str:
    return _git("log", "-1", "--format=%cI", cwd=dest)
