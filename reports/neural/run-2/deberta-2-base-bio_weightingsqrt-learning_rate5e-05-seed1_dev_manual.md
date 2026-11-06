# Hand-labelled dev: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.241 | [0.083, 0.429] |
| Exact span F1 | 0.310 | [0.189, 0.481] |
| Exact span precision | 0.220 | [0.125, 0.389] |
| Exact span recall | 0.529 | [0.375, 0.700] |
| Role macro-F1 (roles with gold support) | 0.170 | [0.103, 0.453] |
| Category macro-F1 | 0.213 | [0.108, 0.548] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.452 | [0.278, 0.647] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.889 | [0.571, 1.000] |
| Role accuracy on exactly matched spans | 0.889 | [0.600, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.258 | 0.500 | 0.340 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.125 | 1.000 | 0.222 | 1 |
| USAGE | 0.227 | 0.556 | 0.323 | 9 |
| ACCESS | 0.250 | 0.400 | 0.308 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.942 | 0.750 | 0.176 |
| 20% | 0.873 | 0.375 | 0.176 |
| 29% | 0.781 | 0.333 | 0.235 |
| 39% | 0.701 | 0.312 | 0.294 |
| 49% | 0.638 | 0.350 | 0.412 |
| 61% | 0.507 | 0.280 | 0.412 |
| 71% | 0.473 | 0.241 | 0.412 |
| 80% | 0.430 | 0.212 | 0.412 |
| 90% | 0.380 | 0.189 | 0.412 |
| 100% | 0.250 | 0.171 | 0.412 |
