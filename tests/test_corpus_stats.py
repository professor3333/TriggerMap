from triggermap.corpus.cues import condition_score, cue_counts
from triggermap.corpus.stats import corpus_stats, percentiles, render_markdown
from triggermap.ingest.records import AdvisoryDocument


def doc(advisory_id: str, details: str, packages: tuple[str, ...] = ("pkg",)) -> AdvisoryDocument:
    return AdvisoryDocument(
        advisory_id=advisory_id,
        aliases=(),
        published="2024-05-01T00:00:00Z",
        modified="2024-05-01T00:00:00Z",
        summary="Summary",
        details=details,
        pypi_packages=packages,
        ecosystems=("PyPI",),
        references=(),
        cwe_ids=(),
        source_commit="c" * 40,
        source_path="advisories/x.json",
        file_sha256="0" * 64,
        content_hash="1" * 64,
    )


def test_cues_match_whole_words_case_insensitively() -> None:
    counts = cue_counts("Only when DEBUG is Enabled; an authenticated admin. Whenever? notify")
    assert counts["conditional"] == 2  # "Only when", "Whenever"; "notify" is not "if"
    assert counts["configuration"] == 1
    assert counts["access"] == 2


def test_condition_score_prefers_condition_rich_text() -> None:
    assert condition_score("A buffer overflow in parse().") == 0
    assert condition_score("If the option is enabled and the user is authenticated") > 2


def test_percentiles() -> None:
    assert percentiles([5, 1, 3], (0.0, 0.5, 1.0)) == {"p0": 1, "p50": 3, "p100": 5}
    assert percentiles([], (0.5,)) == {"p50": 0}


def test_corpus_stats_and_markdown() -> None:
    docs = [
        doc("GHSA-2222-2222-2222", "### Impact\n- When `x` is enabled"),
        doc("GHSA-3333-3333-3333", "Plain text.", ("a", "b")),
    ]
    stats = corpus_stats(docs)
    assert stats["documents"] == 2
    assert stats["multi_package"] == 1
    assert stats["structure_docs"]["heading"] == 1
    assert stats["structure_docs"]["inline_code"] == 1
    assert stats["cue_group_docs"]["conditional"] == 1
    manifest = {
        "source": {
            "repository": "r",
            "commit": "c" * 40,
            "commit_date": "d",
            "path": "p",
            "license": "CC-BY-4.0",
        },
        "preprocessing_version": "1",
        "counts": {"kept": 2, "scanned": 2},
    }
    text = render_markdown(stats, manifest)
    assert "| kept | 2 |" in text
    assert "c" * 40 in text
