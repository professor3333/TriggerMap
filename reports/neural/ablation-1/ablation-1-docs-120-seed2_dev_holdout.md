# Agreement with model drafts (held-out half): ablation-1-docs-120-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed2.jsonl` (ablation-1-docs-120-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.061 | [0.038, 0.090] |
| Exact span F1 | 0.085 | [0.058, 0.114] |
| Exact span precision | 0.050 | [0.034, 0.068] |
| Exact span recall | 0.286 | [0.203, 0.372] |
| Role macro-F1 (roles with gold support) | 0.026 | [0.017, 0.041] |
| Category macro-F1 | 0.061 | [0.034, 0.087] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.793 | [0.751, 0.827] |
| Reversed meaning rate (lower is better) | 0.043 | [0.008, 0.085] |
| Category accuracy on exactly matched spans | 0.775 | [0.622, 0.897] |
| Role accuracy on exactly matched spans | 0.900 | [0.800, 0.976] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.050 | 0.292 | 0.085 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.011 | 0.125 | 0.020 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.058 | 0.222 | 0.092 | 18 |
| USAGE | 0.029 | 0.278 | 0.053 | 54 |
| ACCESS | 0.063 | 0.222 | 0.098 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.539 | 0.087 | 0.050 |
| 20% | 0.487 | 0.062 | 0.071 |
| 30% | 0.455 | 0.062 | 0.107 |
| 40% | 0.435 | 0.059 | 0.136 |
| 50% | 0.409 | 0.057 | 0.164 |
| 60% | 0.380 | 0.052 | 0.179 |
| 70% | 0.356 | 0.048 | 0.193 |
| 80% | 0.317 | 0.044 | 0.200 |
| 90% | 0.266 | 0.040 | 0.207 |
| 100% | 0.161 | 0.036 | 0.207 |
