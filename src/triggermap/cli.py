"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from triggermap import __version__

DEFAULT_SNAPSHOT = Path("data/raw/advisory-database")
DEFAULT_PROCESSED = Path("data/processed")
DEFAULT_MANIFEST = Path("data/manifests/snapshot.json")


def _ingest_fetch(args: argparse.Namespace) -> int:
    from triggermap.ingest.snapshot import fetch_snapshot

    commit = fetch_snapshot(args.dest, args.commit)
    print(f"snapshot {args.dest} at {commit}")
    return 0


def _ingest_build(args: argparse.Namespace) -> int:
    from triggermap.ingest.build import ingest, write_corpus, write_manifest
    from triggermap.ingest.snapshot import snapshot_commit, snapshot_commit_date

    commit = snapshot_commit(args.snapshot)
    result = ingest(args.snapshot, commit)
    manifest = write_corpus(result, args.out, commit, snapshot_commit_date(args.snapshot))
    write_manifest(manifest, args.manifest)
    print(json.dumps(manifest["counts"], indent=2))
    print(f"wrote {args.out} and {args.manifest}")
    return 0


def _corpus_stats(args: argparse.Namespace) -> int:
    from triggermap.corpus.stats import corpus_stats, render_markdown
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    stats = corpus_stats(load_corpus(args.processed / CORPUS_FILE))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_markdown(stats, manifest), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="triggermap", description=__doc__)
    parser.add_argument("--version", action="version", version=f"triggermap {__version__}")
    commands = parser.add_subparsers(dest="command")

    ingest = commands.add_parser("ingest", help="acquire and filter the advisory snapshot")
    ingest_cmds = ingest.add_subparsers(dest="subcommand", required=True)
    fetch = ingest_cmds.add_parser("fetch", help="sparse-clone reviewed advisories")
    fetch.add_argument("--dest", type=Path, default=DEFAULT_SNAPSHOT)
    fetch.add_argument("--commit", help="move the snapshot to this exact commit")
    fetch.set_defaults(handler=_ingest_fetch)
    build = ingest_cmds.add_parser("build", help="filter to PyPI and write the corpus")
    build.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    build.add_argument("--out", type=Path, default=DEFAULT_PROCESSED)
    build.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    build.set_defaults(handler=_ingest_build)

    corpus = commands.add_parser("corpus", help="corpus statistics and sampling")
    corpus_cmds = corpus.add_subparsers(dest="subcommand", required=True)
    stats = corpus_cmds.add_parser("stats", help="write corpus statistics as Markdown")
    stats.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    stats.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    stats.add_argument("--out", type=Path, default=Path("docs/corpus_stats.md"))
    stats.set_defaults(handler=_corpus_stats)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    handler = args.handler
    return int(handler(args))
