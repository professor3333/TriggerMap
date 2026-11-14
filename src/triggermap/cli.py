"""Command-line entry point."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from triggermap import __version__
from triggermap.schema import AnnotationOrigin

DEFAULT_SNAPSHOT = Path("data/raw/advisory-database")
DEFAULT_PROCESSED = Path("data/processed")
DEFAULT_MANIFEST = Path("data/manifests/snapshot.json")
DEFAULT_PILOT = Path("annotations/pilot/pilot_manifest.json")
DEFAULT_SPLIT = Path("splits/pool-v1.json")
MODEL_KINDS = ("rules", "crf", "transformer", "onnx")  # keep in sync with models.registry.KINDS
DEFAULT_POLICY = Path("configs/review_policy.yaml")
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
    source = None
    if args.predictions and predictions is not None:
        source = {
            "file": args.predictions.name,
            "sha256": hashlib.sha256(args.predictions.read_bytes()).hexdigest(),
            "models": sorted({p.model_id for p in predictions.values()}),
            "documents": len(predictions),
        }
    write_manifest(batch_manifest(items, params, split, source), out)
    print(f"wrote {len(items)} {params.strategy} items from the {params.pool} pool to {out}")
    return 0


def _corpus_split_dev(args: argparse.Namespace) -> int:
    """Selection / held-out halves of dev gold, grouped like the splits, committed once."""
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.calibration import calibration_split
    from triggermap.eval.runner import load_gold_files

    if args.out_dir.exists():
        raise SystemExit(f"{args.out_dir} exists; selection splits are immutable once drawn")
    split = load_split(args.split_manifest)
    gold = load_gold_files(args.gold)
    dev = select(sorted(gold), split, "dev")
    if not dev:
        raise SystemExit("no gold documents in the dev split")
    selection, held_out = calibration_split(dev, split["group_of"], args.fraction, args.seed)
    args.out_dir.mkdir(parents=True)
    halves = {"selection": sorted(selection), "holdout": sorted(held_out)}
    for name, ids in halves.items():
        (args.out_dir / f"{name}.json").write_text(json.dumps(ids, indent=0) + "\n")
    groups = {n: len({split["group_of"].get(a, a) for a in ids}) for n, ids in halves.items()}
    manifest = {
        "gold": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in args.gold},
        "split_assignment_sha256": split["assignment_sha256"],
        "fraction": args.fraction,
        "seed": args.seed,
        "documents": {n: len(ids) for n, ids in halves.items()},
        "leakage_groups": groups,
        "files": {
            f"{n}.json": hashlib.sha256((args.out_dir / f"{n}.json").read_bytes()).hexdigest()
            for n in halves
        },
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        f"wrote {args.out_dir}: selection {len(selection)} docs ({groups['selection']} groups), "
        f"held-out {len(held_out)} docs ({groups['holdout']} groups)"
    )
    return 0


def _threshold(args: argparse.Namespace) -> int:
    """What a reviewer sees unflagged: predictions at or above ``--min-confidence``."""
    from triggermap.eval.calibration import keep_confident
    from triggermap.eval.runner import load_predictions
    from triggermap.schema.validate import validate_structure

    pred = load_predictions(args.pred)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    before = after = 0
    with args.out.open("w", encoding="utf-8") as fh:
        for aid in sorted(pred):
            kept = keep_confident(pred[aid], args.min_confidence)
            if issues := validate_structure(kept):
                raise SystemExit(f"{aid}: invalid after thresholding: {issues}")
            before += len(pred[aid].conditions)
            after += len(kept.conditions)
            fh.write(kept.model_dump_json() + "\n")
    print(f"kept {after} of {before} conditions at confidence >= {args.min_confidence}")
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
    reference, note = _drift_reference(args, {c.advisory_id for c in conversions})
    report = args.report or args.out.with_name(args.out.stem + "_report.md")
    report.write_text(render_report(conversions, items, written, reference, note), encoding="utf-8")
    problems = sum(bool(c.issues) for c in conversions)
    print(f"wrote {written} records to {args.out}; {problems} tasks with issues; see {report}")
    return 1 if problems else 0


def _drift_reference(args: argparse.Namespace, batch_ids: set[str]) -> tuple[list[Any], str]:
    """Earlier gold records to compare a batch's label mix with (test split never read)."""
    if not args.reference:
        return [], ""
    from triggermap.corpus.splits import load_split
    from triggermap.eval.runner import load_gold_files
    from triggermap.schema import AdvisoryAnnotation

    assignment = load_split(args.split_manifest)["assignment"]
    records = [
        r
        for aid, r in sorted(load_gold_files(args.reference).items())
        if isinstance(r, AdvisoryAnnotation)
        and aid not in batch_ids
        and assignment.get(aid) != "test"
    ]
    origins = ", ".join(
        f"{k} {v}"
        for k, v in sorted(
            Counter(r.origin.value if r.origin else "unrecorded" for r in records).items()
        )
    )
    files = ", ".join(f"`{p}`" for p in args.reference)
    return records, f"{len(records)} records from {files}, test split excluded ({origins})"


def _annotate_gate(args: argparse.Namespace) -> int:
    from collections import Counter

    from triggermap.annotate.gate import gate, render_gate, strata_of
    from triggermap.annotate.importer import load_export
    from triggermap.corpus.splits import load_split
    from triggermap.eval.runner import load_gold
    from triggermap.schema import AdvisoryAnnotation

    assignment = load_split(args.split_manifest)["assignment"]
    records = [
        r
        for r in load_gold(args.gold).values()
        if isinstance(r, AdvisoryAnnotation) and assignment.get(r.advisory_id) != "test"
    ]
    rows, sizes = gate(records, strata_of(json.loads(args.sample.read_text("utf-8"))), assignment)
    origins = Counter(r.origin.value if r.origin else "unrecorded" for r in records)
    lead_times: list[float] = []
    if args.export:
        for task in load_export(args.export):
            for ann in task.get("annotations", []):
                lead = ann.get("lead_time")
                manual = ann.get("parent_prediction") is None and not ann.get("was_cancelled")
                if manual and isinstance(lead, int | float):
                    lead_times.append(float(lead))
    source = f"`{args.gold}`, split `{args.split_manifest}`"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_gate(rows, sizes, origins, lead_times, source=source), "utf-8")
    unsupported = [r.label for r in rows if r.supported is False]
    print(f"wrote {args.out}; unsupported: {', '.join(unsupported) or 'none'}")
    return 0


def _of_origin(gold: Mapping[str, Any], origin: str) -> dict[str, Any]:
    """Gold records of one origin slice. Only hand-labelled records measure accuracy."""
    if origin == "all":
        return dict(gold)
    return {
        aid: r for aid, r in gold.items() if getattr(r, "origin", None) == AnnotationOrigin.MANUAL
    }


def _scored_gold(args: argparse.Namespace, model_ids: Sequence[str]) -> dict[str, Any]:
    """Gold records of the requested split and origin; the test split needs a declared reason."""
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.runner import load_gold_files

    if args.split == "test" and not args.release_evaluation:
        raise SystemExit(
            "the test split is locked: pass --release-evaluation '<reason>' for a declared "
            "release evaluation (it is logged in docs/test-access-log.md)"
        )
    try:
        gold = load_gold_files(_gold_paths(args))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    kept = set(select(sorted(gold), load_split(args.split_manifest), args.split))
    gold = {aid: record for aid, record in gold.items() if aid in kept}
    gold = _of_origin(gold, args.gold_origin)
    only = _subset(args.subset)
    if only is not None:
        gold = {aid: record for aid, record in gold.items() if aid in only}
    if not gold:
        raise SystemExit(f"no gold documents in the {args.split} split")
    if args.split == "test":
        _log_test_access(args, sorted(model_ids))
    return gold


def _subset(path: Path | None) -> set[str] | None:
    """Advisory ids from a JSON list file (a committed selection or held-out subset)."""
    if path is None:
        return None
    ids = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
        raise SystemExit(f"{path}: expected a JSON list of advisory ids")
    return set(ids)


def _clusters(args: argparse.Namespace) -> dict[str, str] | None:
    if args.clusters != "project":
        return None
    from triggermap.corpus.groups import build_groups
    from triggermap.ingest.build import CORPUS_FILE, load_corpus

    return dict(build_groups(load_corpus(args.processed / CORPUS_FILE)).leakage)


def _gold_context(args: argparse.Namespace, gold: Mapping[str, Any]) -> str:
    return (
        f"{_gold_names(args)} ({args.split} split of `{args.split_manifest}`; "
        f"origin: {args.gold_origin}; "
        + (f"subset `{args.subset}`; " if args.subset else "")
        + f"{len(gold)} documents)"
    )


def _write_report(report: str, out: Path | None) -> None:
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(report)


def _evaluate(args: argparse.Namespace) -> int:
    from triggermap.eval.report import render
    from triggermap.eval.runner import evaluate, load_predictions

    pred = load_predictions(args.pred)
    model_ids = sorted({p.model_id for p in pred.values()})
    gold = _scored_gold(args, model_ids)
    docs, intervals = evaluate(gold, pred, _clusters(args), args.samples, args.seed)
    report = render(
        args.title,
        docs,
        intervals,
        {
            "Gold": _gold_context(args, gold),
            "Predictions": f"`{args.pred}` ({', '.join(model_ids) or 'none'})",
            "Bootstrap": f"{args.samples} resamples, {args.clusters} clusters, seed {args.seed}",
        },
    )
    _write_report(report, args.out)
    return 0


def _multiref(args: argparse.Namespace) -> int:
    """Systems against two references of the same documents; dev split only."""
    from triggermap.corpus.splits import load_split
    from triggermap.eval import multiref
    from triggermap.eval.runner import load_gold, load_predictions

    refs = [load_gold(args.ref_a), load_gold(args.ref_b)]
    assignment = load_split(args.split_manifest)["assignment"]
    outside = sorted({aid for ref in refs for aid in ref if assignment.get(aid) != "dev"})
    if outside:
        raise SystemExit(
            f"multiref scores the dev split only; {len(outside)} documents are not dev "
            f"(first: {outside[0]})"
        )
    preds = [load_predictions(path) for path in args.pred]
    names = [", ".join(sorted({p.model_id for p in pred.values()})) or "none" for pred in preds]
    if len(set(names)) != len(names):
        raise SystemExit("each prediction file must come from a different model")
    try:
        docs = {
            name: multiref.collect_two(refs[0], refs[1], pred)
            for name, pred in zip(names, preds, strict=True)
        }
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    clusters = _clusters(args)
    intervals = {n: multiref.score(d, clusters, args.samples, args.seed) for n, d in docs.items()}
    baseline = docs[names[0]]
    comparisons = {
        n: multiref.compare(baseline, d, clusters, args.samples, args.seed)
        for n, d in docs.items()
        if n != names[0]
    }
    consensus = multiref.consensus_size(*refs)
    report = multiref.render(
        args.title,
        {
            "Reference A": f"`{args.ref_a}`",
            "Reference B": f"`{args.ref_b}`",
            "Predictions": ", ".join(f"`{p}`" for p in args.pred),
            "Bootstrap": f"{args.samples} resamples, {args.clusters} clusters, seed {args.seed}",
        },
        names,
        intervals,
        comparisons,
        {
            "Documents": len(refs[0]),
            "Conditions in A": sum(len(r.conditions) for r in refs[0].values()),
            "Conditions in B": sum(len(r.conditions) for r in refs[1].values()),
            "Consensus conditions (identical in A and B)": consensus,
        },
    )
    _write_report(report, args.out)
    return 0


def _compare(args: argparse.Namespace) -> int:
    from triggermap.eval.bootstrap import paired_bootstrap
    from triggermap.eval.metrics import collect, summary
    from triggermap.eval.report import render_comparison
    from triggermap.eval.runner import check_alignment, load_predictions

    preds = [load_predictions(args.baseline), load_predictions(args.candidate)]
    names = [", ".join(sorted({p.model_id for p in pred.values()})) or "none" for pred in preds]
    gold = _scored_gold(args, sorted({p.model_id for pred in preds for p in pred.values()}))
    for pred in preds:
        check_alignment(gold, pred)
    docs_a, docs_b = (collect(gold, pred) for pred in preds)
    comparison = paired_bootstrap(docs_a, docs_b, summary, _clusters(args), args.samples, args.seed)
    report = render_comparison(
        args.title,
        summary(docs_a),
        summary(docs_b),
        comparison,
        names[0],
        names[1],
        {
            "Gold": _gold_context(args, gold),
            "Baseline (A)": f"`{args.baseline}` ({names[0]})",
            "Candidate (B)": f"`{args.candidate}` ({names[1]})",
            "Bootstrap": f"{args.samples} paired resamples, {args.clusters} clusters, "
            f"seed {args.seed}",
        },
        len(docs_a),
    )
    _write_report(report, args.out)
    return 0


def _gold_examples(
    gold: list[Path],
    processed: Path,
    split_manifest: Path,
    split: str = "train",
    origins: Sequence[str] | None = None,
    only: set[str] | None = None,
) -> list[Any]:
    """Preprocessed (document, record) pairs of one split, optionally of chosen origins only."""
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
        if only is not None and aid not in only:
            continue
        if origins and (record.origin.value if record.origin else "unrecorded") not in origins:
            continue
        doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
        examples.append((doc, record))
    return examples


def _train(args: argparse.Namespace) -> int:
    examples = _gold_examples(args.gold, args.processed, args.split_manifest, origins=args.origin)
    if not examples:
        raise SystemExit("no gold documents in the train split (after any --origin filter)")
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
        dev = _gold_examples(
            args.dev_gold or args.gold,
            args.processed,
            args.split_manifest,
            "dev",
            only=_subset(args.dev_subset),
        )
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
        use_context=not args.no_context,
        max_train_documents=args.max_train_documents,
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

    family = config["train"].get("family", "transformer")
    split = load_split(args.split_manifest)
    examples = _gold_examples(args.gold, args.processed, args.split_manifest, origins=args.origin)
    dev = _gold_examples(
        args.dev_gold or args.gold,
        args.processed,
        args.split_manifest,
        "dev",
        only=_subset(args.dev_subset),
    )
    if not examples or not dev:
        raise SystemExit("experiments need gold documents in both the train and dev splits")
    results = []
    for run in runs:
        bundle = args.out_root / run.name
        if family == "crf":
            extractor: Any = _experiment_crf(run.settings, examples, bundle)
        else:
            extractor = _experiment_transformer(run.settings, examples, dev, bundle, split)
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
                "Gold": f"{len(args.gold)} file(s): {len(examples)} train docs",
                "Dev gold": ", ".join(f"`{p}`" for p in (args.dev_gold or args.gold))
                + (f", subset `{args.dev_subset}`" if args.dev_subset else "")
                + f": {len(dev)} dev docs ("
                + ("this table" if family == "crf" else "early stopping and this table")
                + ")",
                "Split": f"`{args.split_manifest}` ({split['assignment_sha256'][:12]})",
            },
        ),
        encoding="utf-8",
    )
    print(f"wrote {report}")
    return 0


def _experiment_transformer(
    settings: dict[str, Any],
    examples: Sequence[Any],
    dev: Sequence[Any],
    bundle: Path,
    split: dict[str, Any],
) -> Any:
    from triggermap.models.transformer.extractor import TransformerExtractor
    from triggermap.models.transformer.train import TrainConfig, train

    if (bundle / "metadata.json").exists():  # resume: finished runs are not retrained
        print(f"{bundle.name}: reusing existing bundle")
        return TransformerExtractor.load(bundle)
    settings = {**settings, "split_assignment_sha256": split["assignment_sha256"]}
    return train(TrainConfig(**settings), examples, dev, bundle)


def _experiment_crf(settings: dict[str, Any], examples: Sequence[Any], bundle: Path) -> Any:
    import time

    from triggermap.models.crf.model import CrfExtractor
    from triggermap.models.experiment import crf_settings

    if (bundle / "metadata.json").exists():  # resume: finished runs are not retrained
        print(f"{bundle.name}: reusing existing bundle")
        return CrfExtractor.load(bundle)
    started = time.monotonic()
    model = CrfExtractor.train(examples, bundle, **crf_settings(settings))
    # Recorded for the report only; the bundle's own metadata stays deterministic.
    model.metadata = {**model.metadata, "train_seconds": round(time.monotonic() - started)}
    return model


def _calibrate(args: argparse.Namespace) -> int:
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.calibration import (
        calibration_split,
        choose_threshold,
        expected_calibration_error,
        fit,
        precision_interval,
    )
    from triggermap.eval.metrics import collect
    from triggermap.eval.runner import check_alignment, load_gold_files, load_predictions
    from triggermap.serve.policy import ReviewPolicy, save_policy

    gold = _of_origin(load_gold_files(args.gold), args.gold_origin)
    pred = load_predictions(args.pred)
    check_alignment(gold, pred)
    split = load_split(args.split_manifest)
    dev = select(sorted(gold), split, "dev")
    calib_ids, held_ids = calibration_split(dev, split["group_of"], seed=args.seed)
    if not calib_ids or not held_ids:
        raise SystemExit(
            f"need gold dev documents of origin '{args.gold_origin}' in both calibration halves"
        )
    per_doc = {d.advisory_id: d.scored for d in collect({a: gold[a] for a in dev}, pred)}
    gold_total = {a: len(gold[a].conditions) for a in dev}
    calib = [s for a in calib_ids for s in per_doc[a]]
    calibrator = fit(args.method, calib)

    def calibrated(ids: list[str]) -> dict[str, list[tuple[float, bool]]]:
        return {a: [(calibrator(p), ok) for p, ok in per_doc[a]] for a in ids}

    calib_cal, held_cal = calibrated(calib_ids), calibrated(held_ids)
    choice = choose_threshold(
        [s for v in calib_cal.values() for s in v],
        sum(gold_total[a] for a in calib_ids),
        args.target_precision,
    )
    held_scored = [s for v in held_cal.values() for s in v]
    measured: dict[str, Any] = {
        "gold_origin": args.gold_origin,
        "calibration_documents": len(calib_ids),
        "held_out_documents": len(held_ids),
        "ece_raw_held_out": round(
            expected_calibration_error([s for a in held_ids for s in per_doc[a]]), 4
        ),
        "ece_calibrated_held_out": round(expected_calibration_error(held_scored), 4),
    }
    threshold = None
    if choice is not None:
        threshold = round(choice.threshold, 4)
        kept = [ok for p, ok in held_scored if p >= threshold]
        low, high = precision_interval(held_cal, threshold, split["group_of"])
        measured.update(
            {
                "calibration_coverage": round(choice.coverage, 4),
                "calibration_precision": round(choice.precision, 4),
                "held_out_coverage": round(len(kept) / len(held_scored), 4) if held_scored else 0,
                "held_out_precision": round(sum(kept) / len(kept), 4) if kept else None,
                "held_out_precision_ci95": [round(low, 4), round(high, 4)],
                "meets_min_coverage": choice.coverage >= args.min_coverage,
            }
        )
    model_ids = sorted({p.model_id for p in pred.values()})
    policy = ReviewPolicy(
        version=args.version,
        model_id=",".join(model_ids),
        calibration=calibrator.to_dict(),
        accept_threshold=threshold,
        target_precision=args.target_precision,
        min_coverage=args.min_coverage,
        measured=measured,
    )
    save_policy(policy, args.out)
    print(json.dumps(measured, indent=2))
    print(f"wrote {args.out} (accept threshold {threshold})")
    return 0


def _robustness(args: argparse.Namespace) -> int:
    import random

    from triggermap.corpus.splits import load_split
    from triggermap.eval.robustness import PERTURBATIONS, measure, render
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.models.registry import load_extractor
    from triggermap.text.preprocessing import compose_raw

    split = load_split(args.split_manifest)
    docs = [
        d
        for d in load_corpus(args.processed / CORPUS_FILE)
        if split["assignment"].get(d.advisory_id) in ("train", "dev")
    ]
    sample = random.Random(args.seed).sample(docs, min(args.n, len(docs)))
    raws = {d.advisory_id: compose_raw(d.summary, d.details) for d in sample}
    extractor = load_extractor(args.model, args.model_dir)
    results = measure(extractor, raws, args.perturbation or list(PERTURBATIONS))
    out = args.out or Path("reports/robustness") / f"{extractor.model_id}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        render(
            f"Formatting robustness: {extractor.model_id}",
            results,
            {
                "Sample": f"{len(sample)} advisories, train and dev pools (seed {args.seed})",
                "Consistent": "same conditions (normalised surface, category, role) and groups",
            },
        ),
        encoding="utf-8",
    )
    for r in results:
        print(f"{r.name:22} {r.consistent}/{r.documents}")
    print(f"wrote {out}")
    return 0


def _challenge(args: argparse.Namespace) -> int:
    from triggermap.eval.challenge import family_counts, load, render, score
    from triggermap.models.registry import load_extractor

    items = load(args.set)
    extractor = load_extractor(args.model, args.model_dir)
    verified, _ = score([r for r in items if r.item.status == "verified"], extractor)
    drafts, _ = score([r for r in items if r.item.status == "draft"], extractor)
    out = args.out or Path("reports/challenge") / f"{extractor.model_id}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    counts = family_counts(items)
    out.write_text(
        render(
            f"Challenge set: {extractor.model_id}",
            verified,
            drafts,
            {
                "Set": f"`{args.set}`",
                "Items": ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())),
            },
        ),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    return 0


def _errors(args: argparse.Namespace) -> int:
    from triggermap.corpus.splits import load_split, select
    from triggermap.eval.errors import classify, render
    from triggermap.eval.runner import check_alignment, load_gold_files, load_predictions
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.text.preprocessing import compose_raw, preprocess

    if args.split == "test" and not args.release_evaluation:
        raise SystemExit("the test split is locked: pass --release-evaluation '<reason>'")
    gold = _of_origin(load_gold_files(args.gold), args.gold_origin)
    pred = load_predictions(args.pred)
    check_alignment(gold, pred)
    ids = select(sorted(gold), load_split(args.split_manifest), args.split)
    if not ids:
        raise SystemExit(
            f"no gold documents of origin '{args.gold_origin}' in the {args.split} split"
        )
    if args.split == "test":
        _log_test_access(args, sorted({p.model_id for p in pred.values()}))
    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    entries = []
    for aid in ids:
        doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
        entries += classify(aid, doc, gold[aid], pred.get(aid))
    models = ", ".join(sorted({p.model_id for p in pred.values()})) or "none"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        render(
            f"Error catalogue: {models}",
            entries,
            len(ids),
            {
                "Split": f"{args.split} of `{args.split_manifest}`",
                "Gold origin": _origin_note(gold[aid] for aid in ids),
                "Predictions": f"`{args.pred}`",
            },
        ),
        encoding="utf-8",
    )
    print(f"wrote {args.out}: {len(entries)} disagreements in {len(ids)} documents")
    return 0


def _app_sync(args: argparse.Namespace) -> int:
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.serve.storage import AdvisoryRecord, Store
    from triggermap.text.preprocessing import compose_raw

    docs = load_corpus(args.processed / CORPUS_FILE)
    store = Store(args.database)
    count = store.upsert_advisories(
        [
            (
                AdvisoryRecord(
                    d.advisory_id,
                    d.content_hash,
                    compose_raw(d.summary, d.details),
                    d.summary or d.advisory_id,
                    d.pypi_packages,
                    d.published,
                    d.source_commit,
                ),
                d.aliases,
            )
            for d in docs
        ]
    )
    if docs:
        store.set_meta("snapshot_commit", docs[0].source_commit)
    print(f"synced {count} advisories into {args.database} ({store.journal_mode()} journal)")
    return 0


def _app_create_user(args: argparse.Namespace) -> int:
    from triggermap.serve.storage import Store

    token = Store(args.database).create_user(args.name)
    print(f"created user {args.name}; API token (shown once, store it safely):\n{token}")
    return 0


def _app_run(args: argparse.Namespace) -> int:
    import logging
    import sys

    import uvicorn

    # One structured access log (method, route, status, timing; never bodies) on stdout.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    access = logging.getLogger("triggermap.access")
    access.addHandler(handler)
    access.setLevel(logging.INFO)
    access.propagate = False
    uvicorn.run(
        "triggermap.serve.app:create_app",
        factory=True,
        host=args.host,
        port=args.port,
        workers=1,
        log_level="info",
        access_log=False,
    )
    return 0


def _release(args: argparse.Namespace) -> int:
    from triggermap.serve import release as releases

    root = args.root
    if args.subcommand == "create":
        path = releases.create_release(
            root, args.release_id, args.image, args.model, args.model_dir, args.review_policy
        )
        print(json.dumps(releases.read_release(root, args.release_id), indent=2))
        print(f"created {path}")
    elif args.subcommand == "activate":
        manifest = releases.activate(root, args.release_id)
        print(f"active release: {manifest['release_id']} ({manifest['image']})")
    elif args.subcommand == "rollback":
        manifest = releases.rollback(root)
        print(f"rolled back to {manifest['release_id']} ({manifest['image']})")
    else:
        current = releases.current_release(root)
        print(f"current: {current}; previous: {releases.previous_release(root)}")
        print("history: " + " -> ".join(releases.history(root)))
    if args.subcommand in ("activate", "rollback") and args.apply:
        import subprocess

        compose = ["docker", "compose", "-f", str(args.compose), "--env-file", str(root / ".env")]
        try:
            subprocess.run([*compose, "up", "-d", "--force-recreate", "app"], check=True)
        except subprocess.CalledProcessError as exc:
            message = f"docker compose failed (exit {exc.returncode}); see output above"
            raise SystemExit(message) from exc
    return 0


def _app_verify(args: argparse.Namespace) -> int:
    from triggermap.serve.verify import VerificationError, verify

    release = json.loads(args.release.read_text(encoding="utf-8"))
    token = args.token or os.environ.get("TRIGGERMAP_VERIFY_TOKEN", "")
    if not token:
        raise SystemExit("pass --token or set TRIGGERMAP_VERIFY_TOKEN")
    try:
        for check in verify(args.url, release, token):
            print(f"ok  {check}")
    except VerificationError as exc:
        print(f"FAIL {exc}")
        return 1
    print(f"deployment verified: {release['release_id']}")
    return 0


def _export_onnx(args: argparse.Namespace) -> int:
    from triggermap.models.transformer.onnx_bundle import export_onnx, quantize_int8

    out = export_onnx(args.bundle, args.out, opset=args.opset)
    print(f"exported {out / 'model.onnx'}")
    if args.int8:
        quantized = quantize_int8(out, args.int8)
        print(f"quantized {quantized / 'model.int8.onnx'} (dynamic INT8)")
    return 0


def _bench(args: argparse.Namespace) -> int:
    if args.subcommand == "workload":
        from transformers import AutoTokenizer

        from triggermap.bench.workload import (
            REFERENCE_REVISION,
            REFERENCE_TOKENIZER,
            build_workload,
        )
        from triggermap.corpus.splits import load_split
        from triggermap.ingest.build import CORPUS_FILE, load_corpus, write_manifest

        tokenizer = AutoTokenizer.from_pretrained(REFERENCE_TOKENIZER, revision=REFERENCE_REVISION)
        workload = build_workload(
            load_corpus(args.processed / CORPUS_FILE),
            load_split(args.split_manifest),
            tokenizer,
            per_bucket=args.per_bucket,
            natural=args.natural,
        )
        write_manifest(workload, args.out)
        sizes = {k: len(v) for k, v in workload["buckets"].items()}
        print(f"wrote {args.out}: {sizes}")
    elif args.subcommand == "latency-bundle":
        from triggermap.bench.latency_bundle import build

        print(f"wrote latency-only bundle {build(args.base, args.revision, args.out)}")
    elif args.subcommand == "run":
        from triggermap.bench.environment import describe
        from triggermap.bench.report import render, run_configs
        from triggermap.bench.worker import parse_config

        configs = [parse_config(spec) for spec in args.config]
        checkpoint = args.out.with_suffix(".partial.jsonl")
        results = run_configs(configs, args.workload, args.processed, args.repeats, checkpoint)
        load = [json.loads(path.read_text()) for path in args.load_json or []]
        environment = json.loads(args.environment.read_text()) if args.environment else describe()
        workload = json.loads(args.workload.read_text())
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            render(args.title, environment, workload, results, load, args.note or []),
            encoding="utf-8",
        )
        args.out.with_suffix(".json").write_text(
            json.dumps({"environment": environment, "results": results, "load": load}, indent=2)
        )
        print(f"wrote {args.out} and {args.out.with_suffix('.json')}")
    else:
        from triggermap.bench.load import load_test
        from triggermap.ingest.build import CORPUS_FILE, load_corpus
        from triggermap.text.preprocessing import compose_raw

        workload = json.loads(args.workload.read_text())
        wanted = [i["advisory_id"] for i in workload["buckets"]["natural"]]
        corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
        texts = [compose_raw(corpus[a].summary, corpus[a].details) for a in wanted]
        result = load_test(args.url, texts, args.requests, args.concurrency) | {"label": args.label}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
    return 0


def _predict(args: argparse.Namespace) -> int:
    from triggermap.ingest.build import CORPUS_FILE, load_corpus
    from triggermap.models.registry import load_extractor
    from triggermap.schema.validate import validate_annotation
    from triggermap.text.preprocessing import compose_raw, preprocess

    corpus = {d.advisory_id: d for d in load_corpus(args.processed / CORPUS_FILE)}
    if args.sample:
        items = [
            item
            for sample in args.sample
            for item in json.loads(sample.read_text(encoding="utf-8"))["items"]
        ]
        ids = list(
            dict.fromkeys(i["advisory_id"] for i in items if args.use in ("all", i["intended_use"]))
        )
    else:
        ids = sorted(corpus)
    try:
        extractor = load_extractor(args.model, args.model_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    from triggermap.serve.policy import apply_policy, load_policy

    policy = load_policy(args.review_policy) if args.review_policy else None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as fh:
        for aid in ids:
            doc = preprocess(compose_raw(corpus[aid].summary, corpus[aid].details))
            extraction = extractor.extract(doc, aid)
            if policy is not None:
                extraction = apply_policy(extraction, doc, policy)
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
    if args.review_policy and args.review_policy.exists():
        from triggermap.serve.policy import apply_policy, load_policy

        extraction = apply_policy(extraction, doc, load_policy(args.review_policy))
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
            "automatically by `triggermap evaluate` and `triggermap compare` with "
            "`--split test`.\n\n"
            "| UTC time | Models | Gold | Reason |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    reason = args.release_evaluation.replace("|", "/")
    with TEST_ACCESS_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"| {stamp} | {', '.join(model_ids)} | {_gold_names(args)} | {reason} |\n")


def _origin_note(records: Iterable[Any]) -> str:
    """Origin counts of scored gold records, with the agreement caveat for model drafts."""
    counts = Counter(
        r.origin.value if getattr(r, "origin", None) else "unrecorded" for r in records
    )
    text = ", ".join(f"{origin} {n}" for origin, n in sorted(counts.items()))
    if set(counts) - {AnnotationOrigin.MANUAL.value}:
        text += (
            ". Records not labelled by hand measure agreement with the drafting model: "
            "a disagreement with them is not necessarily an error"
        )
    return text


def _gold_paths(args: argparse.Namespace) -> list[Path]:
    return [args.gold, *(getattr(args, "add_gold", None) or [])]


def _gold_names(args: argparse.Namespace) -> str:
    return ", ".join(f"`{path}`" for path in _gold_paths(args))


def _dev_gold_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--dev-subset",
        type=Path,
        help="JSON list of advisory ids: early stopping uses only these dev documents",
    )
    parser.add_argument(
        "--dev-gold",
        type=Path,
        nargs="+",
        help="gold file(s) whose dev records drive early stopping (default: --gold); keeps an "
        "evaluation slice out of model selection",
    )


def _scoring_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--subset",
        type=Path,
        help="JSON list of advisory ids: score only these documents (e.g. a held-out half)",
    )
    parser.add_argument(
        "--add-gold",
        type=Path,
        nargs="+",
        metavar="GOLD",
        help="further gold JSONL files scored together with GOLD (a repeated id is an error)",
    )
    parser.add_argument("--clusters", choices=["document", "project"], default="project")
    parser.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--release-evaluation", metavar="REASON", help="unlock the test split")
    _gold_origin_argument(parser, default="all")


def _gold_origin_argument(parser: argparse.ArgumentParser, default: str) -> None:
    parser.add_argument(
        "--gold-origin",
        choices=["all", "manual"],
        default=default,
        help=f"manual: only gold records labelled by hand (origin=manual); default: {default}",
    )


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
    dev_split = corpus_cmds.add_parser(
        "split-dev", help="split dev gold by leakage group into selection and held-out halves"
    )
    dev_split.add_argument("--gold", type=Path, nargs="+", required=True)
    dev_split.add_argument("--out-dir", type=Path, required=True)
    dev_split.add_argument("--fraction", type=float, default=0.5, help="share for selection")
    dev_split.add_argument("--seed", type=int, default=0)
    dev_split.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    dev_split.set_defaults(handler=_corpus_split_dev)

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
    imp.add_argument(
        "--reference",
        type=Path,
        nargs="+",
        help="earlier gold JSONL to compare the label mix with (test split excluded)",
    )
    imp.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    imp.set_defaults(handler=_annotate_import)

    gate_cmd = annotate_cmds.add_parser("gate", help="pilot decision gate: projected support")
    gate_cmd.add_argument("--gold", type=Path, default=Path("annotations/pilot/pilot-1.jsonl"))
    gate_cmd.add_argument("--sample", type=Path, default=DEFAULT_PILOT)
    gate_cmd.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    gate_cmd.add_argument("--export", type=Path, help="Label Studio JSON export (for pace)")
    gate_cmd.add_argument("--out", type=Path, default=Path("docs/pilot_gate.md"))
    gate_cmd.set_defaults(handler=_annotate_gate)

    evaluate = commands.add_parser("evaluate", help="score predictions against gold")
    evaluate.add_argument("gold", type=Path, help="gold AdvisoryAnnotation JSONL")
    evaluate.add_argument("pred", type=Path, help="predicted Extraction JSONL")
    _scoring_arguments(evaluate)
    evaluate.add_argument("--title", default="Evaluation report")
    evaluate.add_argument("--out", type=Path)
    evaluate.set_defaults(handler=_evaluate)

    compare = commands.add_parser(
        "compare", help="paired bootstrap comparison of two systems on the same gold"
    )
    compare.add_argument("gold", type=Path, help="gold AdvisoryAnnotation JSONL")
    compare.add_argument("baseline", type=Path, help="predictions of system A (baseline)")
    compare.add_argument("candidate", type=Path, help="predictions of system B (candidate)")
    _scoring_arguments(compare)
    compare.add_argument("--title", default="Paired comparison")
    compare.add_argument("--out", type=Path)
    compare.set_defaults(handler=_compare)

    multiref = commands.add_parser(
        "multiref", help="score systems against two references of the same dev documents"
    )
    multiref.add_argument("ref_a", type=Path, help="reference A (AdvisoryAnnotation JSONL)")
    multiref.add_argument("ref_b", type=Path, help="reference B, same documents")
    multiref.add_argument(
        "pred", type=Path, nargs="+", help="predictions; the first is the paired baseline"
    )
    multiref.add_argument("--clusters", choices=["document", "project"], default="project")
    multiref.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    multiref.add_argument("--samples", type=int, default=1000)
    multiref.add_argument("--seed", type=int, default=0)
    multiref.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    multiref.add_argument("--title", default="Scores against two references")
    multiref.add_argument("--out", type=Path)
    multiref.set_defaults(handler=_multiref)

    predict = commands.add_parser("predict", help="run an extraction system over documents")
    predict.add_argument("--model", choices=MODEL_KINDS, default="rules")
    predict.add_argument("--model-dir", type=Path, help="trained bundle (crf, transformer)")
    predict.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    predict.add_argument(
        "--sample", type=Path, nargs="+", help="sample manifest(s); default: whole corpus"
    )
    predict.add_argument(
        "--use", choices=["all", "training", "evaluation_candidate"], default="all"
    )
    predict.add_argument("--review-policy", type=Path, help="apply calibration and review flags")
    predict.add_argument("--out", type=Path, required=True)
    predict.set_defaults(handler=_predict)

    train = commands.add_parser("train", help="train a supervised baseline on gold records")
    train.add_argument("--model", choices=["crf", "transformer"], default="crf")
    train.add_argument("--config", type=Path, help="TOML experiment config (transformer)")
    train.add_argument("--gold", type=Path, nargs="+", required=True, help="gold JSONL file(s)")
    _dev_gold_argument(train)
    train.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    train.add_argument("--out", type=Path, required=True, help="bundle directory to write")
    train.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    train.add_argument("--model-id", default="crf-1")
    train.add_argument("--no-pos", action="store_true", help="skip spaCy part-of-speech features")
    train.add_argument(
        "--no-context", action="store_true", help="CRF ablation: no heading/list context features"
    )
    train.add_argument(
        "--max-train-documents",
        type=int,
        help="CRF learning curve: train on a random subset of this size (seeded by --seed)",
    )
    train.add_argument("--seed", type=int, help="overrides the config seed")
    train.add_argument(
        "--origin",
        action="append",
        choices=[*(o.value for o in AnnotationOrigin), "unrecorded"],
        help="train only on records of this label origin (repeatable; default: all)",
    )
    train.set_defaults(handler=_train)

    calibrate = commands.add_parser("calibrate", help="fit calibration and review thresholds")
    calibrate.add_argument("--gold", type=Path, nargs="+", required=True)
    calibrate.add_argument("--pred", type=Path, required=True, help="predictions covering dev")
    calibrate.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    _gold_origin_argument(calibrate, default="manual")
    calibrate.add_argument("--method", choices=["platt", "isotonic", "identity"], default="platt")
    calibrate.add_argument("--target-precision", type=float, default=0.95)
    calibrate.add_argument("--min-coverage", type=float, default=0.5)
    calibrate.add_argument("--version", default="review-policy-1")
    calibrate.add_argument("--seed", type=int, default=0)
    calibrate.add_argument("--out", type=Path, default=DEFAULT_POLICY)
    calibrate.set_defaults(handler=_calibrate)

    app = commands.add_parser("app", help="review application: data, users, server")
    app_cmds = app.add_subparsers(dest="subcommand", required=True)
    # The same database the server uses (TRIGGERMAP_DATABASE), so CLI and server agree.
    default_db = Path(os.environ.get("TRIGGERMAP_DATABASE", "data/app/triggermap.db"))
    sync = app_cmds.add_parser("sync", help="load the advisory snapshot into the app database")
    sync.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    sync.add_argument("--database", type=Path, default=default_db)
    sync.set_defaults(handler=_app_sync)
    create_user = app_cmds.add_parser("create-user", help="create a reviewer and API token")
    create_user.add_argument("name")
    create_user.add_argument("--database", type=Path, default=default_db)
    create_user.set_defaults(handler=_app_create_user)
    run = app_cmds.add_parser("run", help="serve the API (settings from TRIGGERMAP_* env vars)")
    run.add_argument("--host", default="127.0.0.1")
    run.add_argument("--port", type=int, default=8000)
    run.set_defaults(handler=_app_run)

    verify = app_cmds.add_parser("verify", help="check a running deployment against its release")
    verify.add_argument("--url", default="http://127.0.0.1:8000")
    verify.add_argument(
        "--release", type=Path, default=Path("deploy/releases/current/release.json")
    )
    verify.add_argument("--token", help="API token of a verification user")
    verify.set_defaults(handler=_app_verify)

    release = commands.add_parser("release", help="create, activate and roll back releases")
    release.add_argument("--root", type=Path, default=Path("deploy/releases"))
    release_cmds = release.add_subparsers(dest="subcommand", required=True)
    create = release_cmds.add_parser("create", help="assemble an immutable release directory")
    create.add_argument("release_id")
    create.add_argument("--image", required=True, help="image reference, ideally by digest")
    create.add_argument("--model", choices=MODEL_KINDS, default="rules")
    create.add_argument("--model-dir", type=Path)
    create.add_argument("--review-policy", type=Path, default=DEFAULT_POLICY)
    create.set_defaults(handler=_release)
    compose_default = Path("deploy/compose.yaml")
    for name, helptext in (
        ("activate", "point the active release at RELEASE_ID"),
        ("rollback", "re-activate the previous release (image and bundle together)"),
    ):
        sub = release_cmds.add_parser(name, help=helptext)
        if name == "activate":
            sub.add_argument("release_id")
        sub.add_argument("--apply", action="store_true", help="recreate the app container")
        sub.add_argument("--compose", type=Path, default=compose_default)
        sub.set_defaults(handler=_release)
    status = release_cmds.add_parser("status", help="show current, previous and history")
    status.set_defaults(handler=_release)

    bench = commands.add_parser("bench", help="CPU inference benchmarks and load tests")
    bench_cmds = bench.add_subparsers(dest="subcommand", required=True)
    default_workload = Path("reports/benchmarks/workload-v1.json")
    workload = bench_cmds.add_parser("workload", help="build the declared benchmark workload")
    workload.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    workload.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    workload.add_argument("--per-bucket", type=int, default=20)
    workload.add_argument("--natural", type=int, default=100)
    workload.add_argument("--out", type=Path, default=default_workload)
    workload.set_defaults(handler=_bench)
    latency = bench_cmds.add_parser("latency-bundle", help="pretrained encoder, untrained heads")
    latency.add_argument("--base", required=True)
    latency.add_argument("--revision")
    latency.add_argument("--out", type=Path, required=True)
    latency.set_defaults(handler=_bench)
    run_bench = bench_cmds.add_parser("run", help="benchmark configurations in fresh processes")
    run_bench.add_argument(
        "--config", action="append", required=True, help="kind=onnx,dir=PATH,threads=2,batch=4"
    )
    run_bench.add_argument("--workload", type=Path, default=default_workload)
    run_bench.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    run_bench.add_argument("--repeats", type=int, default=3)
    run_bench.add_argument("--load-json", type=Path, action="append")
    run_bench.add_argument(
        "--environment", type=Path, help="environment JSON (e.g. from a container)"
    )
    run_bench.add_argument("--note", action="append")
    run_bench.add_argument("--title", default="CPU inference benchmark")
    run_bench.add_argument("--out", type=Path, required=True)
    run_bench.set_defaults(handler=_bench)
    load_cmd = bench_cmds.add_parser("load", help="HTTP load test against a running service")
    load_cmd.add_argument("--url", default="http://127.0.0.1:8000")
    load_cmd.add_argument("--workload", type=Path, default=default_workload)
    load_cmd.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    load_cmd.add_argument("--requests", type=int, default=1000)
    load_cmd.add_argument("--concurrency", type=int, default=4)
    load_cmd.add_argument("--label", default="service")
    load_cmd.add_argument("--out", type=Path, required=True)
    load_cmd.set_defaults(handler=_bench)

    export = commands.add_parser("export", help="export model bundles")
    export_cmds = export.add_subparsers(dest="subcommand", required=True)
    onnx = export_cmds.add_parser("onnx", help="transformer bundle -> ONNX (and dynamic INT8)")
    onnx.add_argument("--bundle", type=Path, required=True)
    onnx.add_argument("--out", type=Path, required=True)
    onnx.add_argument("--int8", type=Path, help="also write a dynamically quantized bundle here")
    onnx.add_argument("--opset", type=int, default=18)
    onnx.set_defaults(handler=_export_onnx)

    errors = commands.add_parser("errors", help="write the error catalogue for a split")
    errors.add_argument("--gold", type=Path, nargs="+", required=True)
    errors.add_argument("--pred", type=Path, required=True)
    errors.add_argument("--split", choices=["dev", "test"], default="dev")
    errors.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    errors.add_argument("--release-evaluation", metavar="REASON")
    _gold_origin_argument(errors, default="manual")
    errors.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    errors.add_argument("--out", type=Path, default=Path("docs/error_catalogue.md"))
    errors.set_defaults(handler=_errors)

    robust = commands.add_parser("robustness", help="formatting-perturbation consistency")
    robust.add_argument("--model", choices=MODEL_KINDS, default="rules")
    robust.add_argument("--model-dir", type=Path)
    robust.add_argument("--n", type=int, default=300, help="advisories to sample")
    robust.add_argument("--seed", type=int, default=0)
    robust.add_argument("--perturbation", action="append", help="repeat to select a subset")
    robust.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    robust.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    robust.add_argument("--out", type=Path)
    robust.set_defaults(handler=_robustness)

    challenge = commands.add_parser("challenge", help="score the constructed challenge set")
    challenge.add_argument("--set", type=Path, default=Path("challenge/challenge_set.jsonl"))
    challenge.add_argument("--model", choices=MODEL_KINDS, default="rules")
    challenge.add_argument("--model-dir", type=Path)
    challenge.add_argument("--out", type=Path)
    challenge.set_defaults(handler=_challenge)

    experiment = commands.add_parser(
        "experiment", help="run a grid of trainings (transformer or CRF)"
    )
    experiment.add_argument("--config", type=Path, required=True)
    experiment.add_argument("--gold", type=Path, nargs="+", help="gold JSONL file(s)")
    _dev_gold_argument(experiment)
    experiment.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    experiment.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT)
    experiment.add_argument("--out-root", type=Path, default=Path("artifacts/experiments"))
    experiment.add_argument("--report", type=Path)
    experiment.add_argument("--samples", type=int, default=1000)
    experiment.add_argument("--dry-run", action="store_true", help="print the planned runs")
    experiment.add_argument(
        "--origin",
        action="append",
        choices=[*(o.value for o in AnnotationOrigin), "unrecorded"],
        help="train only on records of this label origin (repeatable; default: all)",
    )
    experiment.set_defaults(handler=_experiment)

    threshold = commands.add_parser(
        "threshold", help="keep only predictions at or above a confidence threshold"
    )
    threshold.add_argument("pred", type=Path, help="predicted Extraction JSONL")
    threshold.add_argument("--min-confidence", type=float, required=True)
    threshold.add_argument("--out", type=Path, required=True)
    threshold.set_defaults(handler=_threshold)

    view = commands.add_parser("view", help="render an evidence-linked review page")
    source = view.add_mutually_exclusive_group(required=True)
    source.add_argument("advisory", nargs="?", help="GHSA id from the processed corpus")
    source.add_argument("--text-file", type=Path, help="advisory text (Markdown) to review")
    view.add_argument("--model", choices=MODEL_KINDS, default="rules")
    view.add_argument("--model-dir", type=Path)
    view.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    view.add_argument("--review-policy", type=Path, default=DEFAULT_POLICY)
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
