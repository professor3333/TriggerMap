"""The snapshot commit date does not depend on the git version or the committer's time zone."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from triggermap.ingest.snapshot import snapshot_commit_date


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
@pytest.mark.parametrize(
    ("committed", "expected"),
    [
        ("2026-10-20T03:38:30+0000", "2026-10-20T03:38:30Z"),
        ("2026-10-20T05:38:30+0200", "2026-10-20T03:38:30Z"),  # converted to UTC
    ],
)
def test_commit_date_is_utc_with_z(tmp_path: Path, committed: str, expected: str) -> None:
    env = {**os.environ, "GIT_COMMITTER_DATE": committed, "GIT_AUTHOR_DATE": committed}
    run = {"cwd": tmp_path, "env": env, "check": True, "capture_output": True}
    subprocess.run(["git", "init", "-q"], **run)  # type: ignore[call-overload]
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            "t",
        ],
        **run,  # type: ignore[call-overload]
    )
    assert snapshot_commit_date(tmp_path) == expected
