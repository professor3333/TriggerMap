# Hand-labelled dev: crf-batches-01-02

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.370 | [0.000, 0.640] |
| Exact span F1 | 0.370 | [0.000, 0.640] |
| Exact span precision | 0.500 | [0.000, 0.818] |
| Exact span recall | 0.294 | [0.000, 0.571] |
| Role macro-F1 (roles with gold support) | 0.200 | [0.000, 0.600] |
| Category macro-F1 | 0.237 | [0.000, 0.524] |
| Group exact-match F1 | 0.500 | [0.000, 1.000] |
| Complete-document exact match, documents with conditions | 0.222 | [0.000, 0.455] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.333 | [0.000, 1.000] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.556 | 0.312 | 0.400 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.429 | 0.333 | 0.375 | 9 |
| ACCESS | 1.000 | 0.400 | 0.571 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.905 | 0.000 | 0.000 |
| 20% | 0.871 | 0.500 | 0.059 |
| 30% | 0.815 | 0.667 | 0.118 |
| 40% | 0.791 | 0.750 | 0.176 |
| 50% | 0.755 | 0.800 | 0.235 |
| 60% | 0.666 | 0.667 | 0.235 |
| 70% | 0.644 | 0.571 | 0.235 |
| 80% | 0.589 | 0.500 | 0.235 |
| 90% | 0.441 | 0.444 | 0.235 |
| 100% | 0.393 | 0.500 | 0.294 |
