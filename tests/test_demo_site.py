"""The published demo pages are self-contained, attributed and match their provenance record."""

import json
import re
from pathlib import Path

import pytest

DEMO = Path(__file__).resolve().parent.parent / "demo"
PROVENANCE = json.loads((DEMO / "provenance.json").read_text(encoding="utf-8"))
PAGES = sorted(DEMO.glob("*.html"))


def test_every_listed_page_exists_and_is_linked() -> None:
    index = (DEMO / "index.html").read_text(encoding="utf-8")
    for page, advisory_id in PROVENANCE["pages"].items():
        html = (DEMO / page).read_text(encoding="utf-8")
        assert advisory_id in html, f"{page} does not show {advisory_id}"
        assert f'href="{page}"' in index, f"index.html does not link {page}"
        assert advisory_id in index


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_is_self_contained_and_attributed(page: Path) -> None:
    html = page.read_text(encoding="utf-8")
    assert "Content-Security-Policy" in html and "default-src 'none'" in html
    assert not re.search(r"<(script|img|iframe)[^>]+src=", html), "external resource"
    assert not re.search(r"<link[^>]+stylesheet", html), "external stylesheet"
    assert "creativecommons.org/licenses/by/4.0" in html
    assert "highlights added" in html  # modification notice
