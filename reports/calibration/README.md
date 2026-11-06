# Calibration and review thresholds (dev split only)

This report compares `crf-batches-01-02` and the best DeBERTa-v3-small run of neural run 3
(`deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2`) after confidence calibration and
review thresholds, as a reviewer would see them.

- **Selection half:** calibration and every threshold were fitted on the selection half of the
  model-drafted dev records (`splits/selection-v1/selection.json`, 111 documents).
- **Held-out half:** every number below is measured on the held-out half (61 documents in 46
  other project groups). `calibrate` splits the dev records into exactly these two halves;
  this was checked.
- **Agreement, not accuracy:** all gold here is model-drafted (`batch-03` + `batch-06`), so the
  scores measure agreement with the drafting model.
- **Untouched:** the test split, and the live review policy (`configs/review_policy.yaml`,
  `review-policy-0`).

## Calibration before and after (held-out half)

Platt scaling fitted on the selection half. ECE is the expected calibration error: 10 bins,
with typed correctness as the outcome.

| Model | ECE, raw confidence | ECE, calibrated | Platt `a`, `b` |
|---|---:|---:|---|
| CRF | 0.305 | 0.101 | 0.415, −1.439 |
| DeBERTa | 0.548 | 0.059 | 0.610, −2.849 |

Both models are badly over-confident before calibration. Fitting DeBERTa first exposed a bug:
undamped Newton steps diverged (`a` ≈ 1.75 × 10⁵, `b` ≈ −2.9 × 10¹¹), and the sigmoid
overflowed. The fit now halves each step until the loss decreases and uses an overflow-free
sigmoid. The CRF's parameters are unchanged by the fix.

Neither model reaches the plan's target precision (0.95, or 0.85 for unflagged predictions in
[`targets.md`](../../docs/targets.md)) on model-drafted gold. At a 0.50 target, DeBERTa keeps
5.9% of its predictions on the selection half and reaches 0.565 precision on 7.6% coverage
held-out. The CRF cannot reach 0.45 on the selection half at any threshold.

## Matched precision targets (held-out half)

For each target precision, `calibrate --method identity` picks the lowest confidence threshold
that reaches it on the selection half. `threshold` then keeps only predictions at or above it:
what a reviewer would see without a low-confidence flag. 95% project-group bootstrap
intervals, 1,000 resamples.

| Target | Model | Threshold | Kept per document | Exact span precision | Exact span recall | Typed F1 | False-prerequisite rate |
|---|---|---:|---:|---:|---:|---:|---:|
| 0.30 | CRF | 0.484 | 0.48 | 0.379 [0.179, 0.607] | 0.079 [0.035, 0.120] | 0.107 [0.041, 0.169] | 0.280 [0.111, 0.500] |
| 0.30 | DeBERTa | 0.858 | 1.20 | 0.329 [0.232, 0.418] | 0.171 [0.110, 0.237] | 0.207 [0.141, 0.275] | 0.391 [0.284, 0.500] |
| 0.35 | CRF | 0.615 | 0.30 | 0.444 [0.188, 0.733] | 0.057 [0.024, 0.090] | 0.101 [0.042, 0.157] | 0.214 [0.000, 0.500] |
| 0.35 | DeBERTa | 0.896 | 0.97 | 0.373 [0.259, 0.473] | 0.157 [0.095, 0.222] | 0.201 [0.129, 0.271] | 0.379 [0.264, 0.500] |
| 0.40 | CRF | 0.660 | 0.28 | 0.471 [0.200, 0.750] | 0.057 [0.024, 0.090] | 0.102 [0.042, 0.157] | 0.231 [0.000, 0.545] |
| 0.40 | DeBERTa | 0.962 | 0.59 | 0.472 [0.290, 0.625] | 0.121 [0.062, 0.184] | 0.182 [0.101, 0.262] | 0.333 [0.200, 0.487] |

Paired differences, DeBERTa − CRF:

| Target | Typed F1 | Exact span precision | False-prerequisite rate (lower is better) |
|---|---:|---:|---:|
| 0.30 | **+0.100 [+0.034, +0.172]** | −0.051 [−0.266, +0.118] | +0.111 [−0.117, +0.317] |
| 0.35 | **+0.100 [+0.024, +0.171]** | −0.072 [−0.348, +0.145] | +0.165 [−0.108, +0.382] |
| 0.40 | +0.080 [−0.003, +0.162] | +0.002 [−0.252, +0.232] | +0.103 [−0.178, +0.318] |

Bold marks a clear difference.

## Decision

The decision rule was set before this comparison: DeBERTa replaces the CRF as the default model
only if, after calibration, it is clearly better on held-out **precision or invented
prerequisites**.

- **Recall:** at the same precision target, DeBERTa keeps two to three times as many agreeing
  conditions. Its typed F1 is clearly higher at the 0.30 and 0.35 targets.
- **Precision:** not clearly different at any target.
- **Invented prerequisites:** DeBERTa's rate is higher at every target (+0.10 to +0.17). None of
  these differences is clear, but none favours DeBERTa.

**The CRF stays the default model.** DeBERTa is the leading candidate: it finds more of what the
drafts mark, at a similar precision, but it has not been shown to invent fewer prerequisites.
Every number here is agreement with model drafts on 61 documents, and the release gates in
[`targets.md`](../../docs/targets.md) still cannot be judged.

## Reproduce

```bash
uv run triggermap calibrate --gold annotations/batches/batch-03.jsonl annotations/batches/batch-06.jsonl \
    --pred reports/neural/run-3/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl \
    --gold-origin all --target-precision 0.5 --out reports/calibration/deberta-platt.yaml
bash scripts/calibration/compare_thresholds.sh   # matched targets, thresholded predictions, comparisons
```
