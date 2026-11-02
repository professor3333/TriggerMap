# Pilot dev: rules, gold origin manual

- Gold: `annotations/pilot/pilot-1.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/pilot/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.095 | [0.000, 0.333] |
| Exact span F1 | 0.095 | [0.000, 0.333] |
| Exact span precision | 0.250 | [0.000, 1.000] |
| Exact span recall | 0.059 | [0.000, 0.231] |
| Role macro-F1 (roles with gold support) | 0.050 | [0.000, 0.261] |
| Category macro-F1 | 0.071 | [0.000, 0.250] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.375] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.750 | [0.000, 1.000] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.250 | 0.062 | 0.100 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.000 | 0.000 | 0.000 | 9 |
| ACCESS | 0.500 | 0.200 | 0.286 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 25% | 0.600 | 1.000 | 0.059 |
| 25% | 0.600 | 1.000 | 0.059 |
| 25% | 0.600 | 1.000 | 0.059 |
| 50% | 0.550 | 0.500 | 0.059 |
| 50% | 0.550 | 0.500 | 0.059 |
| 50% | 0.550 | 0.500 | 0.059 |
| 75% | 0.550 | 0.333 | 0.059 |
| 75% | 0.550 | 0.333 | 0.059 |
| 100% | 0.550 | 0.250 | 0.059 |
| 100% | 0.550 | 0.250 | 0.059 |
