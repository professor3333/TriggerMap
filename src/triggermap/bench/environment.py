"""Describe the machine a benchmark ran on, and whether it is the documented target host."""

from __future__ import annotations

import os
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

TARGET_MACHINE, TARGET_CPUS, TARGET_MEMORY_GB = "x86_64", 2.0, 4.0


def _cpu_model() -> str:
    if platform.system() == "Darwin":
        try:
            return subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return platform.processor()
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith(("model name", "cpu model")):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def _cgroup_limits() -> tuple[float | None, float | None]:
    """Container CPU and memory limits from cgroup v2, when running in one."""
    cpus = memory = None
    try:
        quota, period = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if quota != "max":
            cpus = int(quota) / int(period)
    except (OSError, ValueError):
        pass
    try:
        raw = Path("/sys/fs/cgroup/memory.max").read_text().strip()
        if raw != "max":
            memory = int(raw) / 2**30
    except (OSError, ValueError):
        pass
    return cpus, memory


def _total_memory_gb() -> float | None:
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
    except (ValueError, OSError, AttributeError):
        return None


def describe() -> dict[str, Any]:
    cpu_limit, memory_limit = _cgroup_limits()
    cpus = cpu_limit or os.cpu_count()
    memory = memory_limit or _total_memory_gb()
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = os.environ.get("TRIGGERMAP_GIT_SHA", "unknown")
    matches = (
        platform.machine() == TARGET_MACHINE
        and cpus is not None
        and abs(cpus - TARGET_CPUS) < 0.01
        and memory is not None
        and abs(memory - TARGET_MEMORY_GB) < 0.5
    )
    return {
        "measured_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "system": platform.system(),
        "machine": platform.machine(),
        "cpu_model": _cpu_model(),
        "logical_cpus": os.cpu_count(),
        "cpu_limit": cpu_limit,
        "memory_gb": round(memory, 2) if memory else None,
        "in_container": cpu_limit is not None or memory_limit is not None,
        "python": platform.python_version(),
        "git_commit": commit,
        "matches_target_host": matches,
    }
