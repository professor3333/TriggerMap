# Agreement with model drafts (held-out half): ablation-1-no-group-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed1.jsonl` (ablation-1-no-group-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.228 | [0.180, 0.288] |
| Exact span F1 | 0.287 | [0.237, 0.349] |
| Exact span precision | 0.220 | [0.179, 0.276] |
| Exact span recall | 0.414 | [0.342, 0.496] |
| Role macro-F1 (roles with gold support) | 0.127 | [0.091, 0.195] |
| Category macro-F1 | 0.217 | [0.163, 0.286] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.070 | [0.017, 0.148] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.498 | [0.423, 0.573] |
| Reversed meaning rate (lower is better) | 0.065 | [0.024, 0.110] |
| Category accuracy on exactly matched spans | 0.879 | [0.776, 0.963] |
| Role accuracy on exactly matched spans | 0.914 | [0.821, 0.982] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.234 | 0.408 | 0.298 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.143 | 0.400 | 0.211 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.171 | 0.389 | 0.237 | 18 |
| USAGE | 0.160 | 0.389 | 0.227 | 54 |
| ACCESS | 0.293 | 0.407 | 0.341 | 54 |
| PLATFORM | 0.059 | 0.071 | 0.065 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.990 | 0.538 | 0.100 |
| 20% | 0.949 | 0.472 | 0.179 |
| 30% | 0.895 | 0.380 | 0.214 |
| 40% | 0.801 | 0.340 | 0.257 |
| 50% | 0.750 | 0.295 | 0.279 |
| 60% | 0.648 | 0.253 | 0.286 |
| 70% | 0.573 | 0.227 | 0.300 |
| 80% | 0.518 | 0.213 | 0.321 |
| 90% | 0.454 | 0.193 | 0.329 |
| 100% | 0.159 | 0.174 | 0.329 |
