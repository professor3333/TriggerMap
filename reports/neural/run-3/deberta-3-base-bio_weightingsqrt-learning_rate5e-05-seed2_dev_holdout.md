# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.185 | [0.145, 0.235] |
| Exact span F1 | 0.221 | [0.174, 0.277] |
| Exact span precision | 0.162 | [0.125, 0.209] |
| Exact span recall | 0.350 | [0.271, 0.430] |
| Role macro-F1 (roles with gold support) | 0.100 | [0.066, 0.171] |
| Category macro-F1 | 0.149 | [0.108, 0.182] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.483 | [0.418, 0.544] |
| Reversed meaning rate (lower is better) | 0.047 | [0.014, 0.088] |
| Category accuracy on exactly matched spans | 0.857 | [0.732, 0.963] |
| Role accuracy on exactly matched spans | 0.959 | [0.902, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.183 | 0.367 | 0.244 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.103 | 0.300 | 0.154 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.059 | 0.167 | 0.087 | 18 |
| USAGE | 0.148 | 0.370 | 0.212 | 54 |
| ACCESS | 0.194 | 0.333 | 0.245 | 54 |
| PLATFORM | 0.042 | 0.071 | 0.053 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.973 | 0.500 | 0.107 |
| 20% | 0.892 | 0.344 | 0.150 |
| 30% | 0.824 | 0.319 | 0.207 |
| 40% | 0.745 | 0.289 | 0.250 |
| 50% | 0.653 | 0.237 | 0.257 |
| 60% | 0.597 | 0.198 | 0.257 |
| 70% | 0.558 | 0.175 | 0.264 |
| 80% | 0.515 | 0.165 | 0.286 |
| 90% | 0.443 | 0.150 | 0.293 |
| 100% | 0.236 | 0.135 | 0.293 |
