# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.207 | [0.149, 0.272] |
| Exact span F1 | 0.243 | [0.191, 0.304] |
| Exact span precision | 0.178 | [0.136, 0.229] |
| Exact span recall | 0.386 | [0.309, 0.467] |
| Role macro-F1 (roles with gold support) | 0.127 | [0.076, 0.218] |
| Category macro-F1 | 0.192 | [0.143, 0.240] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.053 | [0.000, 0.131] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.431 | [0.343, 0.512] |
| Reversed meaning rate (lower is better) | 0.046 | [0.013, 0.087] |
| Category accuracy on exactly matched spans | 0.926 | [0.848, 0.984] |
| Role accuracy on exactly matched spans | 0.926 | [0.822, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.215 | 0.375 | 0.274 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.152 | 0.500 | 0.233 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.146 | 0.389 | 0.212 | 18 |
| USAGE | 0.157 | 0.370 | 0.221 | 54 |
| ACCESS | 0.227 | 0.407 | 0.291 | 54 |
| PLATFORM | 0.031 | 0.071 | 0.043 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.972 | 0.467 | 0.100 |
| 20% | 0.913 | 0.377 | 0.164 |
| 30% | 0.809 | 0.308 | 0.200 |
| 40% | 0.750 | 0.279 | 0.243 |
| 50% | 0.674 | 0.243 | 0.264 |
| 60% | 0.606 | 0.225 | 0.293 |
| 70% | 0.551 | 0.202 | 0.307 |
| 80% | 0.502 | 0.185 | 0.321 |
| 90% | 0.431 | 0.168 | 0.329 |
| 100% | 0.250 | 0.151 | 0.329 |
