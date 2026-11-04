# Pilot-2 dev: crf-pilot-2-manual, gold origin manual

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/training-origin/predictions/crf-pilot-2-manual.jsonl` (crf-pilot-2-manual)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.300 | [0.000, 0.556] |
| Exact span F1 | 0.300 | [0.000, 0.556] |
| Exact span precision | 1.000 | [0.000, 1.000] |
| Exact span recall | 0.176 | [0.000, 0.385] |
| Role macro-F1 (roles with gold support) | 0.158 | [0.000, 0.500] |
| Category macro-F1 | 0.193 | [0.000, 0.389] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.375] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.000 | [0.000, 0.000] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 1.000 | 0.188 | 0.316 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 1.000 | 0.111 | 0.200 | 9 |
| ACCESS | 1.000 | 0.400 | 0.571 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 33% | 0.567 | 1.000 | 0.059 |
| 33% | 0.567 | 1.000 | 0.059 |
| 33% | 0.567 | 1.000 | 0.059 |
| 33% | 0.567 | 1.000 | 0.059 |
| 67% | 0.508 | 1.000 | 0.118 |
| 67% | 0.508 | 1.000 | 0.118 |
| 67% | 0.508 | 1.000 | 0.118 |
| 67% | 0.508 | 1.000 | 0.118 |
| 100% | 0.389 | 1.000 | 0.176 |
| 100% | 0.389 | 1.000 | 0.176 |
