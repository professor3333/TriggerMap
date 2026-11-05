# Agreement with model drafts: deberta-1-base-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate2e-05-seed0.jsonl` (deberta-1-base-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.006 | [0.004, 0.009] |
| Exact span F1 | 0.010 | [0.007, 0.013] |
| Exact span precision | 0.005 | [0.003, 0.007] |
| Exact span recall | 0.122 | [0.087, 0.158] |
| Role macro-F1 (roles with gold support) | 0.005 | [0.003, 0.009] |
| Category macro-F1 | 0.008 | [0.005, 0.011] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.854 | [0.836, 0.869] |
| Reversed meaning rate (lower is better) | 0.064 | [0.036, 0.094] |
| Category accuracy on exactly matched spans | 0.830 | [0.685, 0.956] |
| Role accuracy on exactly matched spans | 0.787 | [0.667, 0.897] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.006 | 0.105 | 0.011 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.005 | 0.167 | 0.010 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.001 | 0.028 | 0.001 | 36 |
| USAGE | 0.004 | 0.108 | 0.008 | 186 |
| ACCESS | 0.010 | 0.119 | 0.019 | 134 |
| PLATFORM | 0.002 | 0.067 | 0.003 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.402 | 0.013 | 0.031 |
| 20% | 0.346 | 0.009 | 0.041 |
| 30% | 0.310 | 0.007 | 0.052 |
| 40% | 0.279 | 0.006 | 0.060 |
| 50% | 0.253 | 0.006 | 0.073 |
| 60% | 0.230 | 0.005 | 0.073 |
| 70% | 0.210 | 0.005 | 0.078 |
| 80% | 0.189 | 0.004 | 0.078 |
| 90% | 0.165 | 0.004 | 0.080 |
| 100% | 0.102 | 0.003 | 0.080 |
