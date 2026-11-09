# Agreement with model drafts (held-out half): ablation-1-docs-60-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed0.jsonl` (ablation-1-docs-60-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.046 | [0.028, 0.069] |
| Exact span F1 | 0.060 | [0.037, 0.087] |
| Exact span precision | 0.039 | [0.023, 0.058] |
| Exact span recall | 0.129 | [0.081, 0.177] |
| Role macro-F1 (roles with gold support) | 0.017 | [0.011, 0.026] |
| Category macro-F1 | 0.035 | [0.019, 0.048] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.637 | [0.573, 0.693] |
| Reversed meaning rate (lower is better) | 0.031 | [0.008, 0.062] |
| Category accuracy on exactly matched spans | 0.778 | [0.529, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.045 | 0.150 | 0.070 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.022 | 0.056 | 0.032 | 18 |
| USAGE | 0.034 | 0.148 | 0.055 | 54 |
| ACCESS | 0.036 | 0.093 | 0.052 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.528 | 0.022 | 0.007 |
| 20% | 0.485 | 0.022 | 0.014 |
| 30% | 0.456 | 0.029 | 0.029 |
| 40% | 0.429 | 0.043 | 0.057 |
| 50% | 0.407 | 0.039 | 0.064 |
| 60% | 0.378 | 0.036 | 0.071 |
| 70% | 0.343 | 0.040 | 0.093 |
| 80% | 0.294 | 0.038 | 0.100 |
| 90% | 0.251 | 0.034 | 0.100 |
| 100% | 0.145 | 0.030 | 0.100 |
