# Pilot dev: crf, gold origin manual

- Gold: `annotations/pilot/pilot-1.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/pilot/predictions/crf-pilot-1.jsonl` (crf-1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.154 | [0.000, 0.385] |
| Exact span F1 | 0.154 | [0.000, 0.385] |
| Exact span precision | 0.222 | [0.000, 0.571] |
| Exact span recall | 0.118 | [0.000, 0.333] |
| Role macro-F1 (roles with gold support) | 0.080 | [0.000, 0.320] |
| Category macro-F1 | 0.143 | [0.000, 0.278] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.375] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.556 | [0.200, 0.750] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.222 | 0.125 | 0.160 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.000 | 0.000 | 0.000 | 9 |
| ACCESS | 1.000 | 0.400 | 0.571 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.951 | 0.000 | 0.000 |
| 22% | 0.918 | 0.500 | 0.059 |
| 33% | 0.733 | 0.667 | 0.118 |
| 44% | 0.570 | 0.500 | 0.118 |
| 44% | 0.570 | 0.500 | 0.118 |
| 56% | 0.550 | 0.400 | 0.118 |
| 67% | 0.531 | 0.333 | 0.118 |
| 78% | 0.496 | 0.286 | 0.118 |
| 89% | 0.425 | 0.250 | 0.118 |
| 100% | 0.340 | 0.222 | 0.118 |
