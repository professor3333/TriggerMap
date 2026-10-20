"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

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


def _evaluate(args: argparse.Namespace) -> int:
    from triggermap.eval.report import render
    from triggermap.eval.runner import evaluate, load_gold, load_predictions

    gold = load_gold(args.gold)
    pred = load_predictions(args.pred)
    cluster_of = None
    if args.clusters == "project":
        from triggermap.corpus.groups import build_groups
        from triggermap.ingest.build import CORPUS_FILE, load_corpus

        cluster_of = build_groups(load_corpus(args.processed / CORPUS_FILE)).leakage
    docs, intervals = evaluate(gold, pred, cluster_of, args.samples, args.seed)
    model_ids = sorted({p.model_id for p in pred.values()})
    report = render(
        args.title,
        docs,
        intervals,
        {
            "Gold": f"`{args.gold}`",
            "Predictions": f"`{args.pred}` ({', '.join(model_ids) or 'none'})",
            "Bootstrap": f"{args.samples} resamples, {args.clusters} clusters, seed {args.seed}",
        },
    )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(report)
    return 0


def _gold_examples(gold: Path, processed: Path) -> list[Any]:
    from triggermap.eval.runner import load_gold
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.schema.models import AdvisoryAnnotation
    from triggermap.text.preprocessing import compose_raw, preprocess

    corpus = {d.advisory_id: d for d in load_corpus(processed / CORPUS_FILE)}
    examples = []
    for aid, record in sorted(load_gold(gold).items()):
        assert isinstance(record, AdvisoryAnnotation)
        doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
        examples.append((doc, record))
    return examples


def _train(args: argparse.Namespace) -> int:
    from triggermap.models.crf.model import CrfExtractor

    examples = _gold_examples(args.gold, args.processed)
    model = CrfExtractor.train(
        examples, args.out, model_id=args.model_id, use_pos=not args.no_pos, seed=args.seed
    )
    print(json.dumps(model.metadata["stats"], indent=2))
    print(f"trained {model.model_id} on {len(examples)} documents; bundle at {args.out}")
    return 0


def _predict(args: argparse.Namespace) -> int:
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.models.rules.extractor import RuleExtractor
    from triggermap.schema.validate import validate_annotation
    from triggermap.text.preprocessing import compose_raw, preprocess

    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    if args.sample is not None:
        items = json.loads(args.sample.read_text(encoding="utf-8"))["items"]
        ids = [i["advisory_id"] for i in items if args.use in ("all", i["intended_use"])]
    else:
        ids = sorted(corpus)
    extractor: Any
    if args.model == "crf":
        from triggermap.models.crf.model import CrfExtractor

        if args.model_dir is None:
            raise SystemExit("--model crf needs --model-dir")
        extractor = CrfExtractor.load(args.model_dir)
    else:
        extractor = RuleExtractor()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as fh:
        for aid in ids:
            doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
            extraction = extractor.extract(doc, aid)
            issues = validate_annotation(extraction, doc.text)
            if issues:
                raise RuntimeError(f"{aid}: invalid prediction {issues}")
            fh.write(extraction.model_dump_json(exclude_none=True) + "\n")
    print(f"wrote {len(ids)} {extractor.model_id} predictions to {args.out}")
    return 0


def _view(args: argparse.Namespace) -> int:
    from triggermap.models.rules.extractor import RuleExtractor
    from triggermap.serve.render import render_review
    from triggermap.text.preprocessing import compose_raw, preprocess

    packages: tuple[str, ...] = ()
    source_url = None
    if args.text_file is not None:
        raw = args.text_file.read_text(encoding="utf-8")
        advisory_id, title = None, args.text_file.name
    else:
        from triggermap.ingest.build import CORPUS_FILE, load_corpus

        corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
        if args.advisory not in corpus:
            raise SystemExit(f"{args.advisory} is not in the processed corpus")
        record = corpus[args.advisory]
        raw = compose_raw(record.summary, record.details)
        advisory_id, title, packages = record.advisory_id, record.summary, record.pypi_packages
        source_url = f"https://github.com/advisories/{record.advisory_id}"
    doc = preprocess(raw)
    extractor: Any = RuleExtractor()
    if args.model == "crf":
        from triggermap.models.crf.model import CrfExtractor

        if args.model_dir is None:
            raise SystemExit("--model crf needs --model-dir")
        extractor = CrfExtractor.load(args.model_dir)
    extraction = extractor.extract(doc, advisory_id)
    html = render_review(doc, extraction, title=title, source_url=source_url, packages=packages)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out} ({len(extraction.conditions)} conditions, {extraction.model_id})")
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

    evaluate = commands.add_parser("evaluate", help="score predictions against gold")
    evaluate.add_argument("gold", type=Path, help="gold AdvisoryAnnotation JSONL")
    evaluate.add_argument("pred", type=Path, help="predicted Extraction JSONL")
    evaluate.add_argument("--clusters", choices=["document", "project"], default="project")
    evaluate.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    evaluate.add_argument("--samples", type=int, default=1000)
    evaluate.add_argument("--seed", type=int, default=0)
    evaluate.add_argument("--title", default="Evaluation report")
    evaluate.add_argument("--out", type=Path)
    evaluate.set_defaults(handler=_evaluate)

    predict = commands.add_parser("predict", help="run an extraction system over documents")
    predict.add_argument("--model", choices=["rules", "crf"], default="rules")
    predict.add_argument("--model-dir", type=Path, help="trained bundle (crf)")
    predict.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    predict.add_argument("--sample", type=Path, help="sample manifest; default: whole corpus")
    predict.add_argument(
        "--use", choices=["all", "training", "evaluation_candidate"], default="all"
    )
    predict.add_argument("--out", type=Path, required=True)
    predict.set_defaults(handler=_predict)

    train = commands.add_parser("train", help="train a supervised baseline on gold records")
    train.add_argument("--model", choices=["crf"], default="crf")
    train.add_argument("--gold", type=Path, required=True, help="gold AdvisoryAnnotation JSONL")
    train.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    train.add_argument("--out", type=Path, required=True, help="bundle directory to write")
    train.add_argument("--model-id", default="crf-1")
    train.add_argument("--no-pos", action="store_true", help="skip spaCy part-of-speech features")
    train.add_argument("--seed", type=int, default=0)
    train.set_defaults(handler=_train)

    view = commands.add_parser("view", help="render an evidence-linked review page")
    source = view.add_mutually_exclusive_group(required=True)
    source.add_argument("advisory", nargs="?", help="GHSA id from the processed corpus")
    source.add_argument("--text-file", type=Path, help="advisory text (Markdown) to review")
    view.add_argument("--model", choices=["rules", "crf"], default="rules")
    view.add_argument("--model-dir", type=Path)
    view.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    view.add_argument("--out", type=Path, required=True)
    view.set_defaults(handler=_view)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    handler = args.handler
    return int(handler(args))
