# Evaluation

How TriggerMap systems are scored, which data each score may use, and how to read the
reports. The metrics are implemented in `src/triggermap/eval/metrics.py`. The acceptance
targets a release must meet are in [`targets.md`](targets.md).

## What is being judged

TriggerMap suggests checklist items for a reviewer. An evaluation measures how closely those
suggestions match human annotations of the advisory text. It does **not** measure whether a
deployment is vulnerable. "No explicit conditions found" is a model output, and it is never
read as "the conditions do not apply".

## Correctness

All matching is **exact**, on zero-based, half-open `[start, end)` offsets into the canonical
text.

- A **condition** is correct only when its span, category and role all match a gold
  condition.
- A **group** is correct only when its operator and the set of its member spans both match a
  gold group.
- A **document** is an exact match only when its typed conditions and its groups both match
  the gold record exactly.

There is no partial credit in the headline metrics. Overlap is used only by the two
error-rate diagnostics below.

## Metrics

| Metric | Definition |
|---|---|
| Typed-condition micro-F1 | Primary metric. Micro-F1 over `(span, category, role)` tuples. |
| Exact span P/R/F1 | Micro P/R/F1 over spans, ignoring labels. |
| Role macro-F1 | Mean F1 of `(span, role)` over roles that have gold support in the scored slice. |
| Category macro-F1 | The same over categories. |
| Group exact-match F1 | Micro-F1 over `(operator, member spans)` signatures. |
| Complete-document exact match | Share of documents scored exactly right, reported **separately** for documents whose gold has conditions and for those without. |
| False-prerequisite rate | Predicted `REQUIRED` conditions that overlap no gold condition, divided by all predicted `REQUIRED` conditions. This counts invented prerequisites, the most damaging error. |
| Reversed-meaning rate | Predicted conditions whose best-overlapping gold condition has the opposite polarity (`REQUIRED` against `EXCEPTION` or `NOT_REQUIRED`), divided by predicted conditions that overlap any gold condition. |
| Attribute accuracy on matched spans | Category and role accuracy on predicted spans that exactly match a gold span. This isolates attribute errors from span errors. |
| Precision versus coverage | Predictions sorted by confidence. At each coverage level: typed precision of the kept predictions, and retained recall (kept correct ÷ all gold typed conditions). |
| Expected calibration error | 10 equal-width confidence bins, the count-weighted mean of \|mean confidence − accuracy\|, where accuracy means typed-correct. Reported before and after calibration. |

Every per-class number is reported with its gold support. `UNCERTAIN` and `UNRESOLVED` are
unsupported classes ([`pilot_gate.md`](pilot_gate.md)): they are scored and shown, but never
gated.

## Intervals and comparisons

- **Cluster bootstrap.** 95% intervals come from 1,000 resamples of **project groups** (the
  leakage groups used for the splits), so related advisories move together and intervals are
  not falsely narrow. `--clusters document` resamples single documents instead.
- **Paired comparison.** `triggermap compare GOLD A.jsonl B.jsonl` scores both systems on the
  same documents with identical resamples and reports B − A with its interval. A difference is
  called *clear* only when the whole interval lies on one side of zero. The release gate
  "improvement over the strongest baseline" needs a paired interval with a lower bound above
  zero.

## Which data a score may use

| Split | Used for | Rule |
|---|---|---|
| train | training | Never scored as a result. |
| dev | model selection, thresholds, calibration (on a held-out half) | Every reported number so far is dev. |
| test | final release evaluation only | Locked. `--split test` refuses to run without `--release-evaluation "<reason>"`, and every such run is appended to [`test-access-log.md`](test-access-log.md) (no entries so far). |
| challenge set, prospective batch | reported separately | Never mixed into test numbers. |

**Gold origin.** Each annotation records how its labels were made (`origin`, see
[`annotations/README.md`](../annotations/README.md)). Only `manual` records measure accuracy;
scores against model-drafted records (`model_draft_accepted`, `model_draft_revised`) measure
agreement with the drafting model. Reports state the slice in their header, and
`--gold-origin manual` selects hand-made records only. `calibrate` and `errors` use `manual` by
default, so review thresholds and the error catalogue are never built from model drafts by
accident. `--gold-origin all` includes them, and the output records the slice either way.
Training data can be restricted the
same way (`train --origin manual`), and each model bundle records the origins it was trained
on (`training_origins` in `metadata.json`).

**Current status (2026-11-05).** Only 22 records are `manual` (10 in dev, 4 in test). Every
batch after the pilot is model-drafted, by the owner's decision, so new results are reported as
agreement with the drafting model, labelled as such, and the release gates in
[`targets.md`](targets.md) cannot be judged as declared.

Synthetic, template-generated data (`tests/synthetic.py`) exists only to test the learners.
Its scores are never reported as results.

## Review policy

`configs/review_policy.yaml` (versioned, written by `triggermap calibrate` from the dev
calibration half) decides which predictions are shown as *Review required*:

- a prediction below the calibrated confidence threshold. While no threshold is calibrated
  (the committed policy is `review-policy-0`), **every** prediction is flagged `uncalibrated`;
- any `EXCEPTION`, `NOT_REQUIRED` or `UNCERTAIN` role;
- a negation word inside the span or in the three words before it;
- a condition inside a workaround or mitigation section;
- `UNRESOLVED` groups and `UNSUPPORTED_STRUCTURE` documents, always.

Conditions a reviewer adds are marked `source: human`. The targets gate the typed precision of
the predictions shown **without** a flag.

## Commands

```bash
uv run triggermap evaluate GOLD.jsonl PRED.jsonl --split dev --gold-origin manual --out report.md
uv run triggermap compare GOLD.jsonl A.jsonl B.jsonl --split dev --gold-origin manual --out compare.md
uv run triggermap calibrate --gold GOLD.jsonl --pred PRED.jsonl     # dev halves → review policy (manual gold)
uv run triggermap errors --gold GOLD.jsonl --pred PRED.jsonl        # error catalogue, dev only (manual gold)
```

Current measured results are in [`reports/pilot/`](../reports/pilot/README.md) and
[`reports/training-origin/`](../reports/training-origin/README.md). All of them are preliminary
dev-split numbers on 10 hand-labelled documents.
