import json
import re
from pathlib import Path
from typing import Any

from triggermap.cli import main
from triggermap.models.rules.extractor import RuleExtractor
from triggermap.serve.render import render_review
from triggermap.text.preprocessing import compose_raw, preprocess


def page(text: str, **kwargs: Any) -> tuple[str, Any]:
    doc = preprocess(text)
    extraction = RuleExtractor().extract(doc, kwargs.pop("advisory_id", None))
    return render_review(doc, extraction, title=kwargs.pop("title", "T"), **kwargs), extraction


def payload(html: str) -> dict[str, Any]:
    m = re.search(r'<script id="payload" type="application/json">(.*?)</script>', html, re.S)
    assert m is not None
    data: dict[str, Any] = json.loads(m.group(1))
    return data


def test_every_condition_is_highlighted_and_listed(flask_advisory: dict[str, Any]) -> None:
    raw = compose_raw(flask_advisory["summary"], flask_advisory["details"])
    html, extraction = page(raw, advisory_id="GHSA-m2qf-hxjv-5gpq", title="Flask")
    for cond in extraction.conditions:
        assert f'id="mark-{cond.id}"' in html
        assert f'class="item" data-cond="{cond.id}"' in html
    assert "All of these must hold" in html
    assert "<ol>" in html  # numbered list kept
    data = payload(html)
    assert [c["id"] for c in data["conditions"]] == [c.id for c in extraction.conditions]
    first = data["conditions"][0]
    assert raw[first["raw_span"][0] : first["raw_span"][1]].replace("`", "")


def test_hostile_text_is_escaped_in_page_and_payload() -> None:
    hostile = (
        'Only affects deployments using <script>alert(1)</script> and "</script><img src=x '
        'onerror=alert(2)>" templates.'
    )
    html, extraction = page(hostile)
    assert extraction.conditions  # the hostile text is inside a condition span
    assert "<script>alert(1)" not in html
    assert "<img src=x" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert html.count("</script>") == 2  # only the payload and the page script close
    data = payload(html)
    assert "<script>alert(1)</script>" in data["conditions"][0]["surface"]


def test_no_condition_notice_and_csp() -> None:
    html, extraction = page("A heap overflow occurs when the length field exceeds the buffer.")
    assert not extraction.conditions
    assert "No explicit conditions found. This does not mean the conditions do not apply" in html
    assert "Content-Security-Policy" in html and "default-src 'none'" in html


def test_view_cli_with_text_file(tmp_path: Path) -> None:
    source = tmp_path / "advisory.md"
    source.write_text("### Impact\nOnly affects deployments using the legacy API.\n")
    out = tmp_path / "view.html"
    assert main(["view", "--text-file", str(source), "--out", str(out)]) == 0
    html = out.read_text()
    assert "advisory.md" in html
    assert 'id="mark-c1"' in html
