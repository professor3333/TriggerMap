from hypothesis import given, settings
from hypothesis import strategies as st

from triggermap.text.markdown import BlockKind, CanonicalText, canonicalize


def blocks_text(doc: CanonicalText) -> list[tuple[BlockKind, str]]:
    return [(b.kind, doc.text[b.start : b.end]) for b in doc.blocks]


def assert_map_valid(doc: CanonicalText) -> None:
    assert len(doc.raw_starts) == len(doc.raw_ends) == len(doc.text)
    for i, (start, end) in enumerate(zip(doc.raw_starts, doc.raw_ends, strict=True)):
        assert 0 <= start <= end <= len(doc.raw), i
    assert list(doc.raw_starts) == sorted(doc.raw_starts)


def test_inline_code_is_unwrapped_and_mapped_to_raw() -> None:
    raw = "Set `follow_symlinks` to True."
    doc = canonicalize(raw)
    assert doc.text == "Set follow_symlinks to True."
    start = doc.text.index("follow_symlinks")
    end = start + len("follow_symlinks")
    assert (start, end) in doc.code_spans
    raw_start, raw_end = doc.to_raw(start, end)
    assert raw[raw_start:raw_end] == "follow_symlinks"


def test_intraword_underscores_are_not_emphasis() -> None:
    doc = canonicalize("the _only_ case is follow_symlinks and __init__ but *not* **this**")
    assert doc.text == "the only case is follow_symlinks and __init__ but not this"


def test_unmatched_delimiters_stay_literal() -> None:
    assert canonicalize("a * b and 2*3 = 6_").text == "a * b and 2*3 = 6_"


def test_strikethrough() -> None:
    assert canonicalize("~~old~~ new").text == "old new"


def test_headings_atx_and_setext() -> None:
    doc = canonicalize("### Impact ###\nText.\n\nTitle\n=====\n\nSub\n---\nMore.")
    assert blocks_text(doc) == [
        (BlockKind.HEADING, "Impact"),
        (BlockKind.PARAGRAPH, "Text."),
        (BlockKind.HEADING, "Title"),
        (BlockKind.HEADING, "Sub"),
        (BlockKind.PARAGRAPH, "More."),
    ]
    assert [b.level for b in doc.blocks if b.kind is BlockKind.HEADING] == [3, 1, 2]


def test_soft_breaks_become_spaces_and_blocks_keep_blank_lines() -> None:
    doc = canonicalize("one\r\ntwo  \nthree\n\n\nfour")
    assert doc.text == "one two three\n\nfour"


def test_links_keep_text_and_drop_target() -> None:
    raw = "See [`session.permanent = True`](https://x.test/a_(b)) and ![logo](i.png)."
    doc = canonicalize(raw)
    assert doc.text == "See session.permanent = True and logo."


def test_reference_style_brackets_stay_literal() -> None:
    assert canonicalize("index list[str][0] or [REDACTED]").text == (
        "index list[str][0] or [REDACTED]"
    )


def test_escapes_entities_and_autolinks() -> None:
    raw = r"Use \*args &amp; \_x &lt;tag&gt; <https://example.test/a> &bogus;"
    doc = canonicalize(raw)
    assert doc.text == "Use *args & _x <tag> https://example.test/a &bogus;"
    amp = doc.text.index("&")
    assert doc.raw[slice(*doc.to_raw(amp, amp + 1))] == "&amp;"


def test_formatting_tags_dropped_but_payload_tags_kept() -> None:
    raw = "a<br>b <strong>c</strong> <!-- hidden --> <script>alert(1)</script>"
    assert canonicalize(raw).text == "a b c  <script>alert(1)</script>"


def test_nfc_applies_to_prose_but_not_code() -> None:
    decomposed = "cafe\u0301"
    doc = canonicalize(f"{decomposed} `{decomposed}`")
    assert doc.text == f"caf\u00e9 {decomposed}"
    e = doc.text.index("\u00e9")
    assert doc.raw[slice(*doc.to_raw(e, e + 1))] == "e\u0301"


def test_fenced_code_is_verbatim() -> None:
    raw = "Example:\n```python\nif x:\n    run(follow_symlinks=True)  # *not* emphasis\n```\nAfter."
    doc = canonicalize(raw)
    assert blocks_text(doc) == [
        (BlockKind.PARAGRAPH, "Example:"),
        (BlockKind.CODE, "if x:\n    run(follow_symlinks=True)  # *not* emphasis"),
        (BlockKind.PARAGRAPH, "After."),
    ]
    code = doc.blocks[1]
    assert (code.start, code.end) in doc.code_spans


def test_indented_code_after_blank_line() -> None:
    doc = canonicalize("Para.\n\n    pip install x\n    run()\n\nNext.")
    assert blocks_text(doc)[1] == (BlockKind.CODE, "pip install x\nrun()")


def test_lists_keep_items_nesting_and_list_identity() -> None:
    raw = "Conditions:\n\n1. first\n   wrapped\n2. second\n   - nested\n\n- other list? no\n\nEnd."
    doc = canonicalize(raw)
    items = [b for b in doc.blocks if b.kind is BlockKind.LIST_ITEM]
    assert [doc.text[b.start : b.end] for b in items] == [
        "first wrapped",
        "second",
        "nested",
        "other list? no",
    ]
    assert [b.level for b in items] == [0, 0, 1, 0]
    assert len({b.list_id for b in items}) == 1
    assert items[0].ordered
    assert blocks_text(doc)[-1] == (BlockKind.PARAGRAPH, "End.")


def test_list_item_with_fenced_code() -> None:
    raw = "- install:\n  ```\n  pip install x\n  ```\n- done"
    doc = canonicalize(raw)
    assert blocks_text(doc) == [
        (BlockKind.LIST_ITEM, "install:"),
        (BlockKind.CODE, "pip install x"),
        (BlockKind.LIST_ITEM, "done"),
    ]
    assert doc.blocks[1].list_id == doc.blocks[0].list_id


def test_table_rows_become_lines() -> None:
    raw = "| Option | Default |\n|---|:-:|\n| `debug` | False |\n\nAfter"
    doc = canonicalize(raw)
    assert blocks_text(doc)[0] == (BlockKind.TABLE, "Option | Default\ndebug | False")


def test_quote_and_hr_and_link_definitions() -> None:
    raw = "> quoted\n> text\n\n---\n\n[ref]: https://x.test\nEnd"
    doc = canonicalize(raw)
    assert blocks_text(doc) == [(BlockKind.QUOTE, "quoted text"), (BlockKind.PARAGRAPH, "End")]


def test_to_raw_rejects_invalid_spans() -> None:
    doc = canonicalize("abc")
    for start, end in [(-1, 1), (1, 1), (2, 1), (0, 4)]:
        try:
            doc.to_raw(start, end)
        except ValueError:
            continue
        raise AssertionError((start, end))


def test_aiohttp_fixture_offsets(aiohttp_advisory: dict[str, str]) -> None:
    doc = canonicalize(aiohttp_advisory["details"])
    sentence = (
        "When using aiohttp as a web server and enabling static resource resolution with "
        "follow_symlinks set to True, it can lead to this vulnerability."
    )
    base = doc.text.index(sentence)
    expected = {
        (5, 34): "using aiohttp as a web server",
        (39, 74): "enabling static resource resolution",
        (80, 107): "follow_symlinks set to True",
    }
    for (start, end), surface in expected.items():
        assert doc.text[base + start : base + end] == surface
        raw_start, raw_end = doc.to_raw(base + start, base + end)
        assert doc.raw[raw_start:raw_end].replace("`", "") == surface
    assert "symlinks are not present" in doc.text
    assert "within the static root" in doc.text  # "_within_" emphasis removed


def test_flask_fixture_list(flask_advisory: dict[str, str]) -> None:
    doc = canonicalize(flask_advisory["details"])
    items = [doc.text[b.start : b.end] for b in doc.blocks if b.kind is BlockKind.LIST_ITEM]
    assert len(items) == 5
    assert items[1] == "The application sets session.permanent = True."
    assert items[3] == "SESSION_REFRESH_EACH_REQUEST is enabled (the default)."
    assert "https://" not in doc.text


markdownish = st.text(
    alphabet=st.sampled_from(list("ab _*`~#>-|[]()!<>&;\\\n\r\t 1.:é\u0301")), max_size=200
)


@settings(max_examples=400, deadline=None)
@given(markdownish)
def test_offset_map_invariants_on_arbitrary_input(raw: str) -> None:
    doc = canonicalize(raw)
    assert_map_valid(doc)
    for block in doc.blocks:
        assert 0 <= block.start < block.end <= len(doc.text)
    for start, end in doc.code_spans:
        assert 0 <= start < end <= len(doc.text)


@settings(max_examples=200, deadline=None)
@given(st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=200))
def test_canonicalize_never_crashes_on_unicode(raw: str) -> None:
    assert_map_valid(canonicalize(raw))


@given(st.from_regex(r"[A-Za-z][A-Za-z ,]{0,60}", fullmatch=True))
def test_plain_prose_is_unchanged(raw: str) -> None:
    doc = canonicalize(raw)
    assert doc.text == " ".join(raw.split()) if raw.strip() else doc.text == ""
