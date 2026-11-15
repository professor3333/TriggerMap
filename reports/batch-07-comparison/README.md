# Systems on batch-07, scored against both model drafts (dev)

The 100 `batch-07` dev documents have two independent model drafts:
- **Draft 1:** `annotations/batches/batch-07.jsonl`, 182 conditions.
- **Draft 2:** `annotations/second-drafts/batch-07.jsonl`, 319 conditions.

The drafts agree with each other at only 0.375 typed F1 (see
[`../drafter-consistency/`](../drafter-consistency/README.md)). This report checks whether a
system comparison depends on which draft is used as the reference. It also checks how a system
does on the 94 conditions that both drafts mark identically.

No system was trained, tuned or selected on batch-07, and the test split was not touched. Every
score here measures **agreement with model drafts, not accuracy**.

| System | Bundle | Conditions predicted | REQUIRED |
|---|---|---:|---:|
| `crf-batches-01-02` (default, v0.1.0) | `artifacts/crf-batches-01-02` | 109 | 100 |
| `rules-2` | deterministic rules | 53 | 53 |
| DeBERTa-v3-small, run 3 candidate (`deberta-3-…sqrt…5e-05-seed2`) | best run-3 bundle (weights not committed) | 409 | 343 |
| DeBERTa-v3-small, ablation 1 without the group objective (`ablation-1-no-group-seed1`) | best bundle of the ablation grid (weights not committed) | 404 | 344 |
| DeBERTa-v3-small, run 2 (`deberta-2-…sqrt…5e-05-seed0`) | best run-2 bundle (weights not committed) | 659 | 536 |

- **Run 3 candidate:** the DeBERTa that [`../calibration/`](../calibration/README.md) names the
  leading candidate. On the 60 `batch-06` documents it reproduces its committed run-3
  predictions with identical conditions; confidences differ by at most 0.0001 (Kaggle GPU
  against CPU).
- **Ablation 1, no group:** the same recipe with the group loss switched off. Its conditions are
  identical on the same check, with one confidence differing by 0.0001.
- **Run 2:** an older recipe. It reproduces its committed predictions exactly.

Early stopping for all three used only the selection half of `batch-03` and `batch-06`, and none
saw batch-07.

Full tables: [`batch-07.md`](batch-07.md). Reproduce, or add a bundle, with
`bash scripts/experiments/batch07_comparison.sh [BUNDLE_DIR ...]`. The intervals are 95%
project-group bootstrap intervals (1,000 resamples, seed 0), and differences are paired.

## Metrics

- **Typed / span F1 vs A or B:** exact match against draft 1 or draft 2 alone.
- **Recall on consensus conditions:** the share of the 94 conditions that both drafts mark
  identically (same span, category and role) which the system predicts exactly.
- **Predictions in both / at least one reference:** the share of the system's typed predictions
  that the drafts contain.
- **Invented prerequisites vs both:** the share of predicted REQUIRED conditions that overlap
  no condition in *either* draft. This is a stricter test than the single-draft rate, because
  a span that one drafting run missed but the other found does not count against the system.

## Results

| | `crf-batches-01-02` | `rules-2` | DeBERTa run 3 | DeBERTa ablation 1, no group | DeBERTa run 2 |
|---|---:|---:|---:|---:|---:|
| Typed F1 vs draft 1 | 0.158 [0.101, 0.220] | 0.060 [0.009, 0.125] | 0.186 [0.145, 0.235] | 0.198 [0.149, 0.257] | 0.138 [0.102, 0.176] |
| Typed F1 vs draft 2 | 0.136 [0.090, 0.189] | 0.054 [0.017, 0.101] | 0.245 [0.187, 0.303] | 0.241 [0.189, 0.297] | 0.149 [0.116, 0.184] |
| Recall on consensus conditions | 0.181 [0.106, 0.264] | 0.064 [0.010, 0.139] | 0.426 [0.320, 0.531] | 0.457 [0.344, 0.573] | 0.394 [0.293, 0.489] |
| Predictions in at least one draft | 0.321 [0.240, 0.412] | 0.208 [0.070, 0.395] | 0.254 [0.203, 0.309] | 0.252 [0.197, 0.314] | 0.143 [0.108, 0.177] |
| Invented prerequisites vs both (lower is better) | 0.380 [0.291, 0.471] | 0.208 [0.091, 0.342] | 0.327 [0.258, 0.394] | 0.340 [0.271, 0.405] | 0.504 [0.437, 0.563] |

Paired differences from the CRF:

| | `rules-2` − CRF | DeBERTa run 3 − CRF | DeBERTa ablation 1, no group − CRF | DeBERTa run 2 − CRF |
|---|---:|---:|---:|---:|
| Typed F1 vs draft 1 | −0.099 [−0.155, −0.026] clearly worse | +0.028 [−0.037, +0.098] unclear | +0.040 [−0.023, +0.105] unclear | −0.020 [−0.079, +0.035] unclear |
| Typed F1 vs draft 2 | −0.082 [−0.127, −0.029] clearly worse | +0.109 [+0.049, +0.177] clearly better | +0.105 [+0.049, +0.162] clearly better | +0.014 [−0.036, +0.063] unclear |
| Recall on consensus conditions | −0.117 [−0.200, −0.020] clearly worse | +0.245 [+0.125, +0.364] clearly better | +0.277 [+0.169, +0.380] clearly better | +0.213 [+0.091, +0.319] clearly better |
| Predictions in at least one draft | −0.114 [−0.240, +0.053] unclear | −0.067 [−0.151, +0.011] unclear | −0.069 [−0.153, +0.014] unclear | −0.178 [−0.251, −0.108] clearly worse |
| Invented prerequisites vs both | −0.172 [−0.311, −0.014] clearly better | −0.053 [−0.149, +0.040] unclear | −0.040 [−0.142, +0.061] unclear | +0.124 [+0.027, +0.215] clearly worse |

## Reading

- **CRF over rules holds under both drafts.** The CRF is clearly better on typed and span F1
  against each draft, and on consensus recall. Rules invent clearly fewer prerequisites
  measured against the union of the drafts, though not against either draft alone, mainly
  because they predict half as many conditions (53).
- **The run-3 DeBERTa candidate leads the CRF under both drafts.** It is ahead on typed F1
  against draft 1 (+0.028, not clear) and against draft 2 (+0.109, clear), and on span F1
  likewise. It recovers 2.4 times as many consensus conditions (0.426 against 0.181, clear). It
  invents no more prerequisites than the CRF: 0.327 against 0.380 of REQUIRED predictions
  overlap nothing in either draft, a difference that is not clear. The ablation bundle (same
  recipe, no group loss) gives nearly the same numbers, so this is not a one-bundle accident.
- **It still would not replace the CRF under the pre-set rule.** That rule switches only when the
  candidate is clearly better on precision or on invented prerequisites. Neither difference is
  clear: the share of its predictions backed by at least one draft is 0.254 against 0.321, and
  invention is 0.327 against 0.380. This matches the held-out calibration result
  ([`../calibration/`](../calibration/README.md)): DeBERTa keeps clearly more agreeing
  conditions, but without a clear precision gain.
- **DeBERTa run 2 vs CRF depends on the reference.** On typed and span F1 it is slightly behind
  against draft 1 and slightly ahead against draft 2, and none of these differences is clear.
  Draft 2 marks more conditions, so it favours the system that predicts more. It finds clearly
  more consensus conditions (0.394), but half of its REQUIRED predictions overlap nothing in
  either draft (0.504, clearly worse than the CRF). The ablation bundle does not show that problem.
- **The CRF predicts far fewer conditions than either draft** (109 against 182 and 319) and
  finds only 18% of the consensus conditions. Its main weakness on batch-07 is recall, not
  invention: 62% of its REQUIRED predictions touch a condition in at least one draft.
- These are agreement scores on one dev batch of 100 documents. They say nothing about
  accuracy, which only hand labels can measure.
