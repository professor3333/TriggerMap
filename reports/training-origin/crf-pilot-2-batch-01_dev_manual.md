# Pilot-2 dev: crf-pilot-2-batch-01, gold origin manual

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/training-origin/predictions/crf-pilot-2-batch-01.jsonl` (crf-pilot-2-batch-01)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.444 | [0.133, 0.667] |
| Exact span F1 | 0.444 | [0.133, 0.667] |
| Exact span precision | 0.600 | [0.250, 1.000] |
| Exact span recall | 0.353 | [0.077, 0.611] |
| Role macro-F1 (roles with gold support) | 0.231 | [0.083, 0.619] |
| Category macro-F1 | 0.267 | [0.100, 0.556] |
| Group exact-match F1 | 0.500 | [0.000, 1.000] |
| Complete-document exact match, documents with conditions | 0.222 | [0.000, 0.455] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.300 | [0.000, 0.750] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.600 | 0.375 | 0.462 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.500 | 0.333 | 0.400 | 9 |
| ACCESS | 0.750 | 0.600 | 0.667 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.930 | 0.000 | 0.000 |
| 20% | 0.836 | 0.000 | 0.000 |
| 30% | 0.833 | 0.333 | 0.059 |
| 40% | 0.735 | 0.500 | 0.118 |
| 50% | 0.731 | 0.600 | 0.176 |
| 60% | 0.703 | 0.667 | 0.235 |
| 70% | 0.652 | 0.714 | 0.294 |
| 80% | 0.640 | 0.750 | 0.353 |
| 90% | 0.550 | 0.667 | 0.353 |
| 100% | 0.449 | 0.600 | 0.353 |
