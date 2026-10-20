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
DEFAULT_PILOT = Path("annotations/pilot/pilot_manifest.json")


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


def _corpus_sample_pilot(args: argparse.Namespace) -> int:
    from triggermap.corpus.groups import build_groups
    from triggermap.corpus.sampling import PilotParams, pilot_manifest, sample_pilot
    from triggermap.ingest.build import CORPUS_FILE, load_corpus, write_manifest
    from triggermap.text.preprocessing import PREPROCESSING_VERSION

    snapshot = json.loads(args.manifest.read_text(encoding="utf-8"))
    docs = load_corpus(args.processed / CORPUS_FILE)
    params = PilotParams(seed=args.seed)
    items = sample_pilot(docs, build_groups(docs), params)
    write_manifest(pilot_manifest(items, params, snapshot, PREPROCESSING_VERSION), args.out)
    print(f"wrote {len(items)} pilot items to {args.out}")
    return 0


def _annotate_tasks(args: argparse.Namespace) -> int:
    from triggermap.annotate.label_studio import build_task
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    pilot = json.loads(args.pilot.read_text(encoding="utf-8"))
    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    tasks = [build_task(corpus[item["advisory_id"]], item["order"]) for item in pilot["items"]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(tasks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(tasks)} Label Studio tasks to {args.out}")
    return 0


def _annotate_import(args: argparse.Namespace) -> int:
    from triggermap.annotate.importer import (
        import_export,
        load_export,
        render_report,
        write_records,
    )
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    pilot = json.loads(args.pilot.read_text(encoding="utf-8"))
    items = {item["advisory_id"]: item for item in pilot["items"]}
    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    conversions = import_export(
        load_export(args.export), corpus, args.annotation_version, args.annotator
    )
    written = write_records(conversions, args.out)
    report = args.report or args.out.with_name(args.out.stem + "_report.md")
    report.write_text(render_report(conversions, items, written), encoding="utf-8")
    problems = sum(bool(c.issues) for c in conversions)
    print(f"wrote {written} records to {args.out}; {problems} tasks with issues; see {report}")
    return 1 if problems else 0


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
    pilot = corpus_cmds.add_parser("sample-pilot", help="select the pilot annotation sample")
    pilot.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    pilot.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    pilot.add_argument("--seed", type=int, default=20261020)
    pilot.add_argument("--out", type=Path, default=DEFAULT_PILOT)
    pilot.set_defaults(handler=_corpus_sample_pilot)

    annotate = commands.add_parser("annotate", help="Label Studio tasks and imports")
    annotate_cmds = annotate.add_subparsers(dest="subcommand", required=True)
    tasks = annotate_cmds.add_parser("tasks", help="write Label Studio tasks for a sample")
    tasks.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    tasks.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    tasks.add_argument("--out", type=Path, default=Path("data/label_studio/pilot_tasks.json"))
    tasks.set_defaults(handler=_annotate_tasks)
    imp = annotate_cmds.add_parser("import", help="validate a Label Studio JSON export")
    imp.add_argument("export", type=Path, help="Label Studio JSON export file")
    imp.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    imp.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    imp.add_argument("--annotator", required=True, help="pseudonymous annotator id, e.g. A1")
    imp.add_argument("--annotation-version", default="pilot-1")
    imp.add_argument("--out", type=Path, default=Path("annotations/pilot/pilot-1.jsonl"))
    imp.add_argument("--report", type=Path)
    imp.set_defaults(handler=_annotate_import)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    handler = args.handler
    return int(handler(args))
