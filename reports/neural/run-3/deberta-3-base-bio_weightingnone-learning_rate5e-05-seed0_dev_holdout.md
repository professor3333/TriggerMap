# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingnone-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate5e-05-seed0.jsonl` (deberta-3-base-bio_weightingnone-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.156 | [0.107, 0.213] |
| Exact span F1 | 0.184 | [0.137, 0.240] |
| Exact span precision | 0.151 | [0.108, 0.212] |
| Exact span recall | 0.236 | [0.182, 0.296] |
| Role macro-F1 (roles with gold support) | 0.106 | [0.058, 0.186] |
| Category macro-F1 | 0.132 | [0.097, 0.183] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.408 | [0.318, 0.488] |
| Reversed meaning rate (lower is better) | 0.042 | [0.010, 0.075] |
| Category accuracy on exactly matched spans | 0.909 | [0.806, 1.000] |
| Role accuracy on exactly matched spans | 0.939 | [0.833, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.166 | 0.233 | 0.194 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.188 | 0.300 | 0.231 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.088 | 0.167 | 0.115 | 18 |
| USAGE | 0.146 | 0.241 | 0.182 | 54 |
| ACCESS | 0.209 | 0.259 | 0.231 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.785 | 0.364 | 0.057 |
| 20% | 0.701 | 0.273 | 0.086 |
| 30% | 0.651 | 0.246 | 0.114 |
| 40% | 0.596 | 0.207 | 0.129 |
| 50% | 0.559 | 0.183 | 0.143 |
| 60% | 0.523 | 0.168 | 0.157 |
| 70% | 0.505 | 0.170 | 0.186 |
| 80% | 0.478 | 0.155 | 0.193 |
| 90% | 0.386 | 0.138 | 0.193 |
| 100% | 0.233 | 0.128 | 0.200 |
