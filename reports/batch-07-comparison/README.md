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
| DeBERTa-v3-small, run 2 (`deberta-2-…sqrt…5e-05-seed0`) | best run-2 bundle (weights not committed) | 659 | 536 |

The run-3 DeBERTa candidate (`deberta-3-…sqrt…5e-05-seed2`) is not included, because its
weights were never downloaded from the GPU run. The run-2 bundle stands in for it. It
reproduces its committed run-2 predictions exactly on the 60 `batch-06` documents, including
confidences.

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

| | `crf-batches-01-02` | `rules-2` | DeBERTa run 2 |
|---|---:|---:|---:|
| Typed F1 vs draft 1 | 0.158 [0.101, 0.220] | 0.060 [0.009, 0.125] | 0.138 [0.102, 0.176] |
| Typed F1 vs draft 2 | 0.136 [0.090, 0.189] | 0.054 [0.017, 0.101] | 0.149 [0.116, 0.184] |
| Recall on consensus conditions | 0.181 [0.106, 0.264] | 0.064 [0.010, 0.139] | 0.394 [0.293, 0.489] |
| Predictions in at least one draft | 0.321 [0.240, 0.412] | 0.208 [0.070, 0.395] | 0.143 [0.108, 0.177] |
| Invented prerequisites vs both (lower is better) | 0.380 [0.291, 0.471] | 0.208 [0.091, 0.342] | 0.504 [0.437, 0.563] |

Paired differences from the CRF:

| | `rules-2` − CRF | DeBERTa run 2 − CRF |
|---|---:|---:|
| Typed F1 vs draft 1 | −0.099 [−0.155, −0.026] clearly worse | −0.020 [−0.079, +0.035] unclear |
| Typed F1 vs draft 2 | −0.082 [−0.127, −0.029] clearly worse | +0.014 [−0.036, +0.063] unclear |
| Recall on consensus conditions | −0.117 [−0.200, −0.020] clearly worse | +0.213 [+0.091, +0.319] clearly better |
| Invented prerequisites vs both | −0.172 [−0.311, −0.014] clearly better | +0.124 [+0.027, +0.215] clearly worse |

## Reading

- **CRF over rules holds under both drafts.** The CRF is clearly better on typed and span F1
  against each draft, and on consensus recall. Rules invent clearly fewer prerequisites
  measured against the union of the drafts, though not against either draft alone, mainly
  because they predict half as many conditions (53).
- **DeBERTa vs CRF depends on the reference.** On typed and span F1, DeBERTa is slightly behind
  against draft 1 and slightly ahead against draft 2. None of these differences is clear.
  Draft 2 marks more conditions, so it favours the system that predicts more. Single-reference
  F1 cannot rank these two systems.
- **The clear differences are about recall and invention.** DeBERTa predicts six times as many
  conditions as the CRF. It recovers twice as many consensus conditions (0.394 against 0.181),
  but half of its REQUIRED predictions overlap nothing in either draft (0.504 against 0.380).
  Invented prerequisites are one of the two errors this project weighs most. So under the
  pre-set rule (switch only if clearly better on precision or invented prerequisites), the run-2
  model would not replace the CRF.
- **The CRF predicts far fewer conditions than either draft** (109 against 182 and 319) and
  finds only 18% of the consensus conditions. Its main weakness on batch-07 is recall, not
  invention: 62% of its REQUIRED predictions touch a condition in at least one draft.
- These are agreement scores on one dev batch of 100 documents. They say nothing about
  accuracy, which only hand labels can measure.
