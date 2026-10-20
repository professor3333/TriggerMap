import json
from pathlib import Path
from typing import Any

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def load_advisory(advisory_id: str) -> dict[str, Any]:
    path = FIXTURES / "advisories" / f"{advisory_id}.json"
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return data


@pytest.fixture
def aiohttp_advisory() -> dict[str, Any]:
    return load_advisory("GHSA-5h86-8mv2-jq9f")


@pytest.fixture
def flask_advisory() -> dict[str, Any]:
    return load_advisory("GHSA-m2qf-hxjv-5gpq")
