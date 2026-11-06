# Hand-labelled dev: distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.082 | [0.016, 0.174] |
| Exact span F1 | 0.082 | [0.016, 0.174] |
| Exact span precision | 0.050 | [0.009, 0.111] |
| Exact span recall | 0.235 | [0.043, 0.500] |
| Role macro-F1 (roles with gold support) | 0.052 | [0.011, 0.185] |
| Category macro-F1 | 0.062 | [0.014, 0.164] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.721 | [0.556, 0.877] |
| Reversed meaning rate (lower is better) | 0.130 | [0.000, 0.310] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.066 | 0.250 | 0.104 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.049 | 0.222 | 0.080 | 9 |
| ACCESS | 0.105 | 0.400 | 0.167 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.520 | 0.125 | 0.059 |
| 20% | 0.478 | 0.188 | 0.176 |
| 30% | 0.457 | 0.125 | 0.176 |
| 40% | 0.433 | 0.094 | 0.176 |
| 50% | 0.391 | 0.100 | 0.235 |
| 60% | 0.354 | 0.083 | 0.235 |
| 70% | 0.335 | 0.071 | 0.235 |
| 80% | 0.291 | 0.062 | 0.235 |
| 90% | 0.265 | 0.056 | 0.235 |
| 100% | 0.200 | 0.050 | 0.235 |
