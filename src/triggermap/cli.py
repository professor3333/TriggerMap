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
DEFAULT_SPLIT = Path("splits/pool-v1.json")
TEST_ACCESS_LOG = Path("docs/test-access-log.md")


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
    # pilot-1 was drawn with package co-occurrence + exact duplicates only.
    items = sample_pilot(docs, build_groups(docs, upstream=False), params)
    write_manifest(pilot_manifest(items, params, snapshot, PREPROCESSING_VERSION), args.out)
    print(f"wrote {len(items)} pilot items to {args.out}")
    return 0


def _corpus_split(args: argparse.Namespace) -> int:
    from triggermap.corpus.groups import build_groups
    from triggermap.corpus.neardup import NearDupParams, near_duplicate_pairs
    from triggermap.corpus.splits import SplitParams, build_split
    from triggermap.ingest.build import CORPUS_FILE, load_corpus, write_manifest

    params = SplitParams(version=args.version)
    out = args.out or Path(f"splits/{params.version}.json")
    if out.exists():
        raise SystemExit(f"{out} exists and is frozen; choose a new --version instead")
    docs = load_corpus(args.processed / CORPUS_FILE)
    pairs = near_duplicate_pairs(
        {d.advisory_id: d.details for d in docs},
        NearDupParams(threshold=params.near_duplicate_threshold),
    )
    groups = build_groups(docs, upstream=True, near_duplicates=pairs)
    pilot = json.loads(args.pilot.read_text(encoding="utf-8"))["items"] if args.pilot else []
    snapshot = json.loads(args.manifest.read_text(encoding="utf-8"))
    manifest = build_split(docs, groups, params, pilot)
    manifest = {
        "source_commit": snapshot["source"]["commit"],
        "corpus_sha256": snapshot["outputs"][CORPUS_FILE],
        "near_duplicate_pairs": len(pairs),
        **manifest,
    }
    write_manifest(manifest, out)
    print(json.dumps(manifest["splits"], indent=2))
    print(f"froze {out}; {len(manifest['excluded_documents'])} annotated docs excluded")
    return 0


def _corpus_sample_batch(args: argparse.Namespace) -> int:
    from triggermap.corpus.batches import (
        BatchParams,
        already_sampled,
        batch_manifest,
        sample_batch,
    )
    from triggermap.corpus.splits import load_split
    from triggermap.eval.runner import load_predictions
    from triggermap.ingest.build import CORPUS_FILE, load_corpus, write_manifest

    out = Path("annotations/batches") / f"{args.name}.json"
    if out.exists():
        raise SystemExit(f"{out} exists; batches are immutable once drawn")
    params = BatchParams(
        name=args.name,
        pool=args.pool,
        n=args.n,
        strategy=args.strategy,
        per_group_cap=args.per_group_cap,
        max_words=args.max_words,
    )
    split = load_split(args.split_manifest)
    exclude = already_sampled(sorted(Path("annotations").glob("**/*.json")))
    predictions = load_predictions(args.predictions) if args.predictions else None
    docs = load_corpus(args.processed / CORPUS_FILE)
    items = sample_batch(docs, split, params, exclude, predictions)
    write_manifest(batch_manifest(items, params, split), out)
    print(f"wrote {len(items)} {params.strategy} items from the {params.pool} pool to {out}")
    return 0


def _annotate_tasks(args: argparse.Namespace) -> int:
    from triggermap.annotate.label_studio import build_task
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    sample = json.loads(args.sample.read_text(encoding="utf-8"))
    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    tasks = [build_task(corpus[item["advisory_id"]], item["order"]) for item in sample["items"]]
    out = args.out or Path(f"data/label_studio/{sample['sample_version']}_tasks.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(tasks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(tasks)} Label Studio tasks to {out}")
    return 0


def _annotate_import(args: argparse.Namespace) -> int:
    from triggermap.annotate.importer import (
        import_export,
        load_export,
        render_report,
        write_records,
    )
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    sample = json.loads(args.sample.read_text(encoding="utf-8"))
    items = {item["advisory_id"]: item for item in sample["items"]}
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
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.report import render
    from triggermap.eval.runner import evaluate, load_gold, load_predictions

    gold = load_gold(args.gold)
    pred = load_predictions(args.pred)
    if args.split == "test" and not args.release_evaluation:
        raise SystemExit(
            "the test split is locked: pass --release-evaluation '<reason>' for a declared "
            "release evaluation (it is logged in docs/test-access-log.md)"
        )
    manifest = load_split(args.split_manifest)
    kept = set(select(sorted(gold), manifest, args.split))
    gold = {aid: record for aid, record in gold.items() if aid in kept}
    if not gold:
        raise SystemExit(f"no gold documents in the {args.split} split")
    if args.split == "test":
        _log_test_access(args, sorted({p.model_id for p in pred.values()}))
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
            "Gold": f"`{args.gold}` ({args.split} split of `{args.split_manifest}`)",
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


def _gold_examples(
    gold: list[Path], processed: Path, split_manifest: Path, split: str = "train"
) -> list[Any]:
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.runner import load_gold_files
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.schema.models import AdvisoryAnnotation
    from triggermap.text.preprocessing import compose_raw, preprocess

    corpus = {d.advisory_id: d for d in load_corpus(processed / CORPUS_FILE)}
    examples = []
    records = load_gold_files(gold)
    if split == "test":
        raise ValueError("gold examples for training or tuning never come from the test split")
    wanted = set(select(sorted(records), load_split(split_manifest), split))  # type: ignore[arg-type]
    for aid, record in sorted(records.items()):
        if aid not in wanted:
            continue
        assert isinstance(record, AdvisoryAnnotation)
        doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
        examples.append((doc, record))
    return examples


def _train(args: argparse.Namespace) -> int:
    examples = _gold_examples(args.gold, args.processed, args.split_manifest)
    if not examples:
        raise SystemExit("no gold documents in the train split")
    if args.model == "transformer":
        import tomllib

        from triggermap.corpus.splits import load_split
        from triggermap.models.transformer.train import TrainConfig, train

        if args.config is None:
            raise SystemExit("--model transformer needs --config (see configs/experiments/)")
        settings = tomllib.loads(args.config.read_text(encoding="utf-8"))["train"]
        settings["split_assignment_sha256"] = load_split(args.split_manifest)["assignment_sha256"]
        settings.setdefault("model_id", args.model_id)
        settings["seed"] = args.seed if args.seed is not None else settings.get("seed", 0)
        dev = _gold_examples(args.gold, args.processed, args.split_manifest, "dev")
        transformer = train(TrainConfig(**settings), examples, dev, args.out)
        best = transformer.metadata["best_dev_typed_f1"]
        print(
            f"trained {transformer.model_id} on {len(examples)} documents "
            f"(dev typed F1 {best if best is not None else 'n/a'}); bundle at {args.out}"
        )
        return 0

    from triggermap.models.crf.model import CrfExtractor

    model = CrfExtractor.train(
        examples,
        args.out,
        model_id=args.model_id,
        use_pos=not args.no_pos,
        seed=args.seed or 0,
    )
    print(json.dumps(model.metadata["stats"], indent=2))
    print(f"trained {model.model_id} on {len(examples)} documents; bundle at {args.out}")
    return 0


def _experiment(args: argparse.Namespace) -> int:
    import tomllib

    from triggermap.models.experiment import RunResult, evaluate_run, plan, render_report

    config = tomllib.loads(args.config.read_text(encoding="utf-8"))
    runs = plan(config)
    if args.dry_run:
        for run in runs:
            changed = {k: run.settings[k] for k in sorted(run.settings) if k != "model_id"}
            print(run.name, json.dumps(changed, sort_keys=True))
        print(f"{len(runs)} runs planned")
        return 0

    from triggermap.corpus.splits import load_split
    from triggermap.models.transformer.train import TrainConfig, train

    split = load_split(args.split_manifest)
    examples = _gold_examples(args.gold, args.processed, args.split_manifest)
    dev = _gold_examples(args.gold, args.processed, args.split_manifest, "dev")
    if not examples or not dev:
        raise SystemExit("experiments need gold documents in both the train and dev splits")
    results = []
    from triggermap.models.transformer.extractor import TransformerExtractor

    for run in runs:
        bundle = args.out_root / run.name
        if (bundle / "metadata.json").exists():  # resume: finished runs are not retrained
            extractor = TransformerExtractor.load(bundle)
            print(f"{run.name}: reusing existing bundle")
        else:
            settings = {**run.settings, "split_assignment_sha256": split["assignment_sha256"]}
            extractor = train(TrainConfig(**settings), examples, dev, bundle)
        intervals = evaluate_run(extractor, dev, split["group_of"], args.samples)
        results.append(RunResult(run, intervals, extractor.metadata))
        print(f"{run.name}: dev typed F1 {intervals['typed_f1'].estimate:.3f}")
    report = args.report or Path("reports/experiments") / f"{args.config.stem}.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        render_report(
            f"Experiment: {args.config.stem}",
            results,
            {
                "Config": f"`{args.config}`",
                "Gold": f"{len(args.gold)} file(s): {len(examples)} train, {len(dev)} dev docs",
                "Split": f"`{args.split_manifest}` ({split['assignment_sha256'][:12]})",
            },
        ),
        encoding="utf-8",
    )
    print(f"wrote {report}")
    return 0


def _predict(args: argparse.Namespace) -> int:
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.models.registry import load_extractor
    from triggermap.schema.validate import validate_annotation
    from triggermap.text.preprocessing import compose_raw, preprocess

    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    if args.sample is not None:
        items = json.loads(args.sample.read_text(encoding="utf-8"))["items"]
        ids = [i["advisory_id"] for i in items if args.use in ("all", i["intended_use"])]
    else:
        ids = sorted(corpus)
    try:
        extractor = load_extractor(args.model, args.model_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
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
    from triggermap.models.registry import load_extractor
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
    try:
        extractor = load_extractor(args.model, args.model_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    extraction = extractor.extract(doc, advisory_id)
    html = render_review(doc, extraction, title=title, source_url=source_url, packages=packages)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out} ({len(extraction.conditions)} conditions, {extraction.model_id})")
    return 0


def _log_test_access(args: argparse.Namespace, model_ids: list[str]) -> None:
    from datetime import UTC, datetime

    if not TEST_ACCESS_LOG.exists():
        TEST_ACCESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        TEST_ACCESS_LOG.write_text(
            "# Test-set access log\n\nEvery evaluation on the locked test split, appended "
            "automatically by `triggermap evaluate --split test`.\n\n"
            "| UTC time | Models | Gold | Reason |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    reason = args.release_evaluation.replace("|", "/")
    with TEST_ACCESS_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"| {stamp} | {', '.join(model_ids)} | `{args.gold}` | {reason} |\n")


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
    batch = corpus_cmds.add_parser("sample-batch", help="draw an annotation batch from a pool")
    batch.add_argument("--name", required=True, help="e.g. batch-01; output annotations/batches/")
    batch.add_argument("--pool", choices=["train", "dev", "test"], required=True)
    batch.add_argument("--n", type=int, required=True)
    batch.add_argument("--strategy", choices=["natural", "enriched", "uncertainty"])
    batch.add_argument("--per-group-cap", type=int, default=3)
    batch.add_argument("--max-words", type=int)
    batch.add_argument("--predictions", type=Path, help="Extraction JSONL for uncertainty")
    batch.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    batch.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    batch.set_defaults(handler=_corpus_sample_batch, strategy="natural")
    split = corpus_cmds.add_parser("split", help="freeze leakage-safe train/dev/test pools")
    split.add_argument("--version", default="pool-v1")
    split.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    split.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    split.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    split.add_argument("--out", type=Path)
    split.set_defaults(handler=_corpus_split)

    annotate = commands.add_parser("annotate", help="Label Studio tasks and imports")
    annotate_cmds = annotate.add_subparsers(dest="subcommand", required=True)
    tasks = annotate_cmds.add_parser("tasks", help="write Label Studio tasks for a sample")
    tasks.add_argument("--sample", "--pilot", type=Path, default=DEFAULT_PILOT, dest="sample")
    tasks.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    tasks.add_argument("--out", type=Path, help="default: data/label_studio/<sample>_tasks.json")
    tasks.set_defaults(handler=_annotate_tasks)
    imp = annotate_cmds.add_parser("import", help="validate a Label Studio JSON export")
    imp.add_argument("export", type=Path, help="Label Studio JSON export file")
    imp.add_argument("--sample", "--pilot", type=Path, default=DEFAULT_PILOT, dest="sample")
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
    evaluate.add_argument("--split", choices=["dev", "test"], default="dev")
    evaluate.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    evaluate.add_argument("--release-evaluation", metavar="REASON", help="unlock the test split")
    evaluate.add_argument("--title", default="Evaluation report")
    evaluate.add_argument("--out", type=Path)
    evaluate.set_defaults(handler=_evaluate)

    predict = commands.add_parser("predict", help="run an extraction system over documents")
    predict.add_argument("--model", choices=["rules", "crf", "transformer"], default="rules")
    predict.add_argument("--model-dir", type=Path, help="trained bundle (crf, transformer)")
    predict.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    predict.add_argument("--sample", type=Path, help="sample manifest; default: whole corpus")
    predict.add_argument(
        "--use", choices=["all", "training", "evaluation_candidate"], default="all"
    )
    predict.add_argument("--out", type=Path, required=True)
    predict.set_defaults(handler=_predict)

    train = commands.add_parser("train", help="train a supervised baseline on gold records")
    train.add_argument("--model", choices=["crf", "transformer"], default="crf")
    train.add_argument("--config", type=Path, help="TOML experiment config (transformer)")
    train.add_argument("--gold", type=Path, nargs="+", required=True, help="gold JSONL file(s)")
    train.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    train.add_argument("--out", type=Path, required=True, help="bundle directory to write")
    train.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    train.add_argument("--model-id", default="crf-1")
    train.add_argument("--no-pos", action="store_true", help="skip spaCy part-of-speech features")
    train.add_argument("--seed", type=int, help="overrides the config seed")
    train.set_defaults(handler=_train)

    experiment = commands.add_parser("experiment", help="run a grid of transformer trainings")
    experiment.add_argument("--config", type=Path, required=True)
    experiment.add_argument("--gold", type=Path, nargs="+", help="gold JSONL file(s)")
    experiment.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    experiment.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    experiment.add_argument("--out-root", type=Path, default=Path("artifacts/experiments"))
    experiment.add_argument("--report", type=Path)
    experiment.add_argument("--samples", type=int, default=1000)
    experiment.add_argument("--dry-run", action="store_true", help="print the planned runs")
    experiment.set_defaults(handler=_experiment)

    view = commands.add_parser("view", help="render an evidence-linked review page")
    source = view.add_mutually_exclusive_group(required=True)
    source.add_argument("advisory", nargs="?", help="GHSA id from the processed corpus")
    source.add_argument("--text-file", type=Path, help="advisory text (Markdown) to review")
    view.add_argument("--model", choices=["rules", "crf", "transformer"], default="rules")
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
