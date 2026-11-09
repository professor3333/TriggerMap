# Agreement with model drafts (held-out half): ablation-1-docs-120-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed0.jsonl` (ablation-1-docs-120-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.089 | [0.057, 0.122] |
| Exact span F1 | 0.109 | [0.072, 0.148] |
| Exact span precision | 0.068 | [0.044, 0.094] |
| Exact span recall | 0.271 | [0.194, 0.339] |
| Role macro-F1 (roles with gold support) | 0.049 | [0.021, 0.100] |
| Category macro-F1 | 0.070 | [0.042, 0.100] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.668 | [0.602, 0.723] |
| Reversed meaning rate (lower is better) | 0.033 | [0.006, 0.063] |
| Category accuracy on exactly matched spans | 0.842 | [0.717, 0.951] |
| Role accuracy on exactly matched spans | 0.974 | [0.905, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.070 | 0.292 | 0.113 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.053 | 0.200 | 0.083 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.014 | 0.056 | 0.023 | 18 |
| USAGE | 0.064 | 0.315 | 0.106 | 54 |
| ACCESS | 0.067 | 0.241 | 0.105 | 54 |
| PLATFORM | 0.033 | 0.071 | 0.045 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.559 | 0.089 | 0.036 |
| 20% | 0.519 | 0.089 | 0.071 |
| 30% | 0.490 | 0.089 | 0.107 |
| 40% | 0.463 | 0.089 | 0.143 |
| 50% | 0.438 | 0.079 | 0.157 |
| 60% | 0.413 | 0.083 | 0.200 |
| 70% | 0.387 | 0.077 | 0.214 |
| 80% | 0.346 | 0.067 | 0.214 |
| 90% | 0.283 | 0.062 | 0.221 |
| 100% | 0.150 | 0.055 | 0.221 |
