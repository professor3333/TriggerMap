# Agreement with model drafts (held-out half): ablation-1-docs-60-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed1.jsonl` (ablation-1-docs-60-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.072 | [0.048, 0.107] |
| Exact span F1 | 0.075 | [0.048, 0.110] |
| Exact span precision | 0.047 | [0.030, 0.071] |
| Exact span recall | 0.193 | [0.128, 0.269] |
| Role macro-F1 (roles with gold support) | 0.027 | [0.018, 0.043] |
| Category macro-F1 | 0.050 | [0.033, 0.072] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.677 | [0.623, 0.725] |
| Reversed meaning rate (lower is better) | 0.059 | [0.014, 0.106] |
| Category accuracy on exactly matched spans | 0.963 | [0.889, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.053 | 0.217 | 0.085 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.013 | 0.125 | 0.023 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.028 | 0.111 | 0.044 | 18 |
| USAGE | 0.051 | 0.296 | 0.087 | 54 |
| ACCESS | 0.045 | 0.148 | 0.069 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.554 | 0.052 | 0.021 |
| 20% | 0.507 | 0.060 | 0.050 |
| 30% | 0.472 | 0.052 | 0.064 |
| 40% | 0.437 | 0.052 | 0.086 |
| 50% | 0.416 | 0.059 | 0.121 |
| 60% | 0.386 | 0.057 | 0.143 |
| 70% | 0.360 | 0.059 | 0.171 |
| 80% | 0.318 | 0.054 | 0.179 |
| 90% | 0.277 | 0.048 | 0.179 |
| 100% | 0.161 | 0.045 | 0.186 |
