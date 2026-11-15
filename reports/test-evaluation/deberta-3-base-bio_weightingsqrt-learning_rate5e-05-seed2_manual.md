# Test split, 4 hand-labelled records: deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: manual; 4 documents)
- Predictions: `reports/test-evaluation/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 4 (3 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.133 | [0.000, 0.235] |
| Exact span F1 | 0.200 | [0.000, 0.545] |
| Exact span precision | 0.130 | [0.000, 0.375] |
| Exact span recall | 0.429 | [0.000, 1.000] |
| Role macro-F1 (roles with gold support) | 0.413 | [0.000, 0.545] |
| Category macro-F1 | 0.206 | [0.000, 0.343] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.684 | [0.500, 0.889] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.667 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.105 | 0.333 | 0.160 | 6 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.500 | 1.000 | 0.667 | 1 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 0 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 0 |
| USAGE | 0.000 | 0.000 | 0.000 | 3 |
| ACCESS | 0.200 | 1.000 | 0.333 | 1 |
| PLATFORM | 0.250 | 0.333 | 0.286 | 3 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.961 | 0.000 | 0.000 |
| 22% | 0.777 | 0.000 | 0.000 |
| 30% | 0.693 | 0.000 | 0.000 |
| 39% | 0.646 | 0.000 | 0.000 |
| 52% | 0.574 | 0.083 | 0.143 |
| 61% | 0.562 | 0.071 | 0.143 |
| 70% | 0.522 | 0.062 | 0.143 |
| 78% | 0.512 | 0.056 | 0.143 |
| 91% | 0.481 | 0.048 | 0.143 |
| 100% | 0.393 | 0.087 | 0.286 |
