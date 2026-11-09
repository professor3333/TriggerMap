# Agreement with model drafts (held-out half): ablation-1-docs-60-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed2.jsonl` (ablation-1-docs-60-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.107 | [0.077, 0.145] |
| Exact span F1 | 0.135 | [0.098, 0.185] |
| Exact span precision | 0.094 | [0.068, 0.132] |
| Exact span recall | 0.243 | [0.173, 0.318] |
| Role macro-F1 (roles with gold support) | 0.037 | [0.028, 0.055] |
| Category macro-F1 | 0.086 | [0.058, 0.122] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.584 | [0.518, 0.636] |
| Reversed meaning rate (lower is better) | 0.053 | [0.015, 0.093] |
| Category accuracy on exactly matched spans | 0.794 | [0.656, 0.931] |
| Role accuracy on exactly matched spans | 0.941 | [0.862, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.102 | 0.267 | 0.147 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.070 | 0.167 | 0.098 | 18 |
| USAGE | 0.061 | 0.241 | 0.097 | 54 |
| ACCESS | 0.118 | 0.204 | 0.150 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.614 | 0.167 | 0.043 |
| 20% | 0.564 | 0.137 | 0.071 |
| 30% | 0.521 | 0.128 | 0.100 |
| 40% | 0.489 | 0.103 | 0.107 |
| 50% | 0.462 | 0.104 | 0.136 |
| 60% | 0.437 | 0.096 | 0.150 |
| 70% | 0.397 | 0.083 | 0.150 |
| 80% | 0.351 | 0.079 | 0.164 |
| 90% | 0.282 | 0.080 | 0.186 |
| 100% | 0.156 | 0.074 | 0.193 |
