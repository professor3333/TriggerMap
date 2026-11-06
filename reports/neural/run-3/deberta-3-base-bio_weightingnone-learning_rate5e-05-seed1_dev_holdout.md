# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1.jsonl` (deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.150 | [0.100, 0.210] |
| Exact span F1 | 0.172 | [0.120, 0.236] |
| Exact span precision | 0.141 | [0.096, 0.197] |
| Exact span recall | 0.221 | [0.154, 0.297] |
| Role macro-F1 (roles with gold support) | 0.082 | [0.038, 0.142] |
| Category macro-F1 | 0.118 | [0.079, 0.165] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.060] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.479 | [0.402, 0.554] |
| Reversed meaning rate (lower is better) | 0.054 | [0.011, 0.094] |
| Category accuracy on exactly matched spans | 0.935 | [0.833, 1.000] |
| Role accuracy on exactly matched spans | 0.935 | [0.839, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.142 | 0.225 | 0.174 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.125 | 0.200 | 0.154 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.074 | 0.111 | 0.089 | 18 |
| USAGE | 0.143 | 0.296 | 0.193 | 54 |
| ACCESS | 0.180 | 0.204 | 0.191 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.762 | 0.227 | 0.036 |
| 20% | 0.697 | 0.250 | 0.079 |
| 30% | 0.637 | 0.242 | 0.114 |
| 40% | 0.597 | 0.205 | 0.129 |
| 50% | 0.556 | 0.182 | 0.143 |
| 60% | 0.523 | 0.159 | 0.150 |
| 70% | 0.497 | 0.143 | 0.157 |
| 80% | 0.462 | 0.136 | 0.171 |
| 90% | 0.408 | 0.131 | 0.186 |
| 100% | 0.229 | 0.123 | 0.193 |
