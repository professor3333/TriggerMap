# Hand-labelled dev: ablation-1-docs-60-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed0.jsonl` (ablation-1-docs-60-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.029 | [0.000, 0.122] |
| Exact span F1 | 0.058 | [0.000, 0.156] |
| Exact span precision | 0.038 | [0.000, 0.111] |
| Exact span recall | 0.118 | [0.000, 0.308] |
| Role macro-F1 (roles with gold support) | 0.035 | [0.000, 0.151] |
| Category macro-F1 | 0.029 | [0.000, 0.133] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.537 | [0.300, 0.683] |
| Reversed meaning rate (lower is better) | 0.050 | [0.000, 0.125] |
| Category accuracy on exactly matched spans | 0.500 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.049 | 0.125 | 0.070 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.000 | 0.000 | 0.000 | 9 |
| ACCESS | 0.083 | 0.200 | 0.118 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.592 | 0.000 | 0.000 |
| 19% | 0.558 | 0.100 | 0.059 |
| 31% | 0.475 | 0.062 | 0.059 |
| 40% | 0.427 | 0.048 | 0.059 |
| 50% | 0.376 | 0.038 | 0.059 |
| 60% | 0.316 | 0.032 | 0.059 |
| 69% | 0.304 | 0.028 | 0.059 |
| 81% | 0.280 | 0.024 | 0.059 |
| 90% | 0.250 | 0.021 | 0.059 |
| 100% | 0.136 | 0.019 | 0.059 |
