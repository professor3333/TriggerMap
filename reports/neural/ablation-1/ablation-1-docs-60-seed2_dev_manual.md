# Hand-labelled dev: ablation-1-docs-60-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed2.jsonl` (ablation-1-docs-60-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.136 | [0.043, 0.245] |
| Exact span F1 | 0.169 | [0.075, 0.304] |
| Exact span precision | 0.119 | [0.053, 0.227] |
| Exact span recall | 0.294 | [0.118, 0.533] |
| Role macro-F1 (roles with gold support) | 0.073 | [0.026, 0.238] |
| Category macro-F1 | 0.228 | [0.061, 0.507] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.375] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.538 | [0.379, 0.720] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.800 | [0.375, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.103 | 0.250 | 0.145 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.333 | 1.000 | 0.500 | 1 |
| USAGE | 0.067 | 0.222 | 0.103 | 9 |
| ACCESS | 0.250 | 0.400 | 0.308 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.704 | 0.250 | 0.059 |
| 19% | 0.642 | 0.250 | 0.118 |
| 31% | 0.590 | 0.308 | 0.235 |
| 40% | 0.539 | 0.235 | 0.235 |
| 50% | 0.503 | 0.190 | 0.235 |
| 60% | 0.451 | 0.160 | 0.235 |
| 69% | 0.427 | 0.138 | 0.235 |
| 81% | 0.374 | 0.118 | 0.235 |
| 90% | 0.319 | 0.105 | 0.235 |
| 100% | 0.149 | 0.095 | 0.235 |
