from triggermap.text.markdown import canonicalize
from triggermap.text.segment import segment


def sentences(raw: str) -> list[str]:
    doc = canonicalize(raw)
    return [doc.text[s.start : s.end] for s in segment(doc)]


def test_versions_identifiers_and_abbreviations_do_not_split() -> None:
    raw = (
        "Versions before 3.9.2 are affected. Set flask.session.permanent to True, e.g. Redis "
        "sessions. Fixed in v2.3.2. `follow_symlinks` must be False!"
    )
    assert sentences(raw) == [
        "Versions before 3.9.2 are affected.",
        "Set flask.session.permanent to True, e.g. Redis sessions.",
        "Fixed in v2.3.2.",
        "follow_symlinks must be False!",
    ]


def test_lowercase_continuation_and_missing_space_do_not_split() -> None:
    assert sentences("Use the option. then restart.It works.") == [
        "Use the option. then restart.It works."
    ]


def test_quotes_and_parentheses_close_sentences() -> None:
    assert sentences('He said "it is unsafe." Then (as noted.) Done.') == [
        'He said "it is unsafe."',
        "Then (as noted.)",
        "Done.",
    ]


def test_each_list_item_and_code_block_is_separate() -> None:
    raw = "Requires:\n- a. B too\n- c\n\n```\nx = 1. Y = 2\n```"
    assert sentences(raw) == ["Requires:", "a.", "B too", "c", "x = 1. Y = 2"]


def test_sentences_record_their_block() -> None:
    doc = canonicalize("# Title\n\nOne. Two.")
    assert [s.block for s in segment(doc)] == [0, 1, 1]
