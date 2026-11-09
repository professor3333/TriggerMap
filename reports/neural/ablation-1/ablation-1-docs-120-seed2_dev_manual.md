# Hand-labelled dev: ablation-1-docs-120-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed2.jsonl` (ablation-1-docs-120-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.106 | [0.045, 0.170] |
| Exact span F1 | 0.124 | [0.075, 0.183] |
| Exact span precision | 0.073 | [0.043, 0.116] |
| Exact span recall | 0.412 | [0.273, 0.562] |
| Role macro-F1 (roles with gold support) | 0.067 | [0.043, 0.182] |
| Category macro-F1 | 0.053 | [0.019, 0.143] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.807 | [0.662, 0.880] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.857 | [0.500, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.080 | 0.438 | 0.135 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.066 | 0.556 | 0.118 | 9 |
| ACCESS | 0.062 | 0.200 | 0.095 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.557 | 0.300 | 0.176 |
| 20% | 0.508 | 0.211 | 0.235 |
| 30% | 0.474 | 0.172 | 0.294 |
| 40% | 0.456 | 0.158 | 0.353 |
| 50% | 0.411 | 0.125 | 0.353 |
| 60% | 0.390 | 0.103 | 0.353 |
| 70% | 0.363 | 0.090 | 0.353 |
| 80% | 0.322 | 0.078 | 0.353 |
| 90% | 0.270 | 0.070 | 0.353 |
| 100% | 0.162 | 0.062 | 0.353 |
