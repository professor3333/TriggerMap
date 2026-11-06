# Hand-labelled dev: deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.157 | [0.069, 0.259] |
| Exact span F1 | 0.157 | [0.069, 0.259] |
| Exact span precision | 0.097 | [0.041, 0.172] |
| Exact span recall | 0.412 | [0.214, 0.636] |
| Role macro-F1 (roles with gold support) | 0.092 | [0.045, 0.275] |
| Category macro-F1 | 0.129 | [0.070, 0.261] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.650 | [0.492, 0.774] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.117 | 0.438 | 0.184 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.114 | 0.444 | 0.182 | 9 |
| ACCESS | 0.231 | 0.600 | 0.333 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.548 | 0.286 | 0.118 |
| 19% | 0.504 | 0.286 | 0.235 |
| 31% | 0.478 | 0.227 | 0.294 |
| 40% | 0.447 | 0.172 | 0.294 |
| 50% | 0.405 | 0.167 | 0.353 |
| 60% | 0.386 | 0.163 | 0.412 |
| 69% | 0.369 | 0.140 | 0.412 |
| 81% | 0.329 | 0.121 | 0.412 |
| 90% | 0.264 | 0.108 | 0.412 |
| 100% | 0.169 | 0.097 | 0.412 |
