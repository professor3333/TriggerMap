# Acceptance targets

**Declared 2026-11-02, after the pilot and before any test-set result exists.** The
[test-access log](test-access-log.md) has no entries at the time of writing. Every number on
this page is a **target**, not a result. Measured results are reported separately, with support
counts and confidence intervals.

Changing a target after this date requires a changelog entry with its reason, and is not
allowed once a release evaluation on the test split has been run for the release concerned.

## Status (2026-11-05): gates cannot be judged as declared

Every annotation batch after the pilot (batches 01, 02, 03 and 06) was submitted from model
drafts, and the owner decided on 2026-11-05 to continue with model-drafted labels rather than
hand labelling. The gates below are judged on hand-labelled (`origin: manual`) test records,
and only 4 test records are hand-labelled, so **no release can be shown to meet them**. The
targets themselves are unchanged.

Until hand-labelled records exist, results are reported as **agreement with the drafting
model** (scored with `--gold-origin all` against model-drafted records). Agreement is never
presented as accuracy, and it is never used to claim that a gate is met.

## What the targets are judged on

- **Split.** The locked test split (`splits/pool-v1.json`), in a declared release evaluation
  (`triggermap evaluate --split test --release-evaluation "<reason>"`). Tuning, thresholds and
  calibration use dev only.
- **Gold.** Only records labelled by hand (`origin: manual`, `--gold-origin manual`). Test
  records whose labels came from a model draft (8 in the pilot, origin `model_draft_accepted`
  or `model_draft_revised`) are excluded from the headline and their count is reported.
  Scores against model-made labels measure agreement with that model, not accuracy.
- **Intervals.** 95% paired project-group bootstrap intervals (1,000 resamples). A target is
  met on the **point estimate**. The interval is always reported alongside it.
- **Support.** A per-class number is reported as *insufficient support* when the test slice
  has fewer than 20 gold examples of that class. Unsupported classes are never gated.
- **Correctness.** A condition is correct only when exact span, category and role all match.
  A group is correct only when membership and operator both match.

## Quality gates for a release model

A model becomes the default serving model only if it meets every **gate**. The **aim** is the
plan's ambition and is reported, but it does not block a release.

| Metric | Gate | Aim | Why this level |
|---|---:|---:|---|
| False-prerequisite rate (lower is better) | ≤ 0.15 | ≤ 0.05 | Invented prerequisites are the most damaging error. The rules baseline is at 0.135 on the all-origins pilot dev slice, so 0.15 rules out regressions to CRF-like levels (0.36–0.44). |
| Reversed-meaning rate (lower is better) | ≤ 0.05 | 0.00 | The second most damaging error. |
| Typed-condition micro-F1 | ≥ 0.60 | ≥ 0.80 | Pilot dev baselines (10 hand-labelled docs) are 0.10–0.23. |
| Improvement over the strongest baseline | paired 95% CI lower bound > 0 | n/a | A neural model must beat rules and CRF on the same documents, not only clear a fixed bar. |
| Exact span F1 | ≥ 0.65 | ≥ 0.85 | Span errors bound every other metric. |
| Role macro-F1 (supported roles with test support) | ≥ 0.60 | ≥ 0.75 | Negation and exception handling. |
| Group exact-match F1 (`ALL`, `ANY`) | ≥ 0.50 | ≥ 0.70 | Groups are judged strictly (membership and operator). |
| Complete-document exact match, documents without conditions | ≥ 0.80 | ≥ 0.90 | The model must not invent conditions where the advisory states none. |
| Complete-document exact match, documents with conditions | reported | ≥ 0.40 | Very strict; reported, not gated. |
| Expected calibration error after calibration | ≤ 0.10 | ≤ 0.05 | Review thresholds depend on calibrated confidence. |
| Typed precision of predictions shown without a *Review required* flag | ≥ 0.85 | ≥ 0.90 | What a reviewer sees unflagged should be trustworthy. |

From the pilot gate ([`pilot_gate.md`](pilot_gate.md)):

- `UNCERTAIN` and `UNRESOLVED` are unsupported. They are not gated, and every prediction of
  either is routed to *Review required*. A test checks this routing.
- `EXCEPTION` had no natural pilot examples, so test support is expected below 20. It is
  reported per class but not gated unless the test slice reaches 20 examples.
- `ANY` is only just supported (51 projected). It is gated within group F1, and its per-class
  number is reported with its support.

## Robustness and slices (reported, not gated)

- Formatting robustness (`triggermap robustness`): the share of documents whose predictions
  are unchanged under formatting-only perturbations. Aim ≥ 0.95.
- Challenge set (`triggermap challenge`, constructed, stored separately): reported per
  phenomenon (negation flips, conjunction flips, required vs unnecessary, prerequisite vs
  workaround, keyword-free paraphrase).
- Prospective batch: reported separately from the test split.

## Release-to-release regression tolerances

A candidate that replaces the current release is compared on the **dev** split
(`origin: manual`):

| Metric | Allowed change against the current release |
|---|---|
| Typed-condition micro-F1 | no drop of more than 1.0 point |
| False-prerequisite rate | no rise of more than 1.0 point |
| Reversed-meaning rate | no rise |
| Exported runtime (ONNX/INT8) vs PyTorch, typed-condition F1 | no drop of more than 1.0 point |

## Serving targets

The CPU serving targets for the documented 2 vCPU / 4 GB x86-64 host are in
[`benchmarks.md`](benchmarks.md#targets-engineering-targets-not-results): warm p95 ≤ 2.5 s at
about 512 tokens, ≤ 8 s at about 2,000 tokens, peak memory ≤ 3 GB, throughput ≥ 0.25 docs/s,
≥ 99.5% successful requests out of 1,000. They are judged only on that host.

## Changelog

| Date | Change |
|---|---|
| 2026-11-02 | First declaration, after the pilot and before any test results. |
| 2026-11-05 | Status note added: labels after the pilot are model drafts, so the gates cannot be judged as declared. No target changed; the test-access log still has no entries. |
