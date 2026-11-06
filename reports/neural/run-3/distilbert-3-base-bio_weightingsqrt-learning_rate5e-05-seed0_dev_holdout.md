# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.099 | [0.064, 0.142] |
| Exact span F1 | 0.118 | [0.074, 0.177] |
| Exact span precision | 0.088 | [0.054, 0.140] |
| Exact span recall | 0.179 | [0.113, 0.252] |
| Role macro-F1 (roles with gold support) | 0.069 | [0.030, 0.128] |
| Category macro-F1 | 0.081 | [0.049, 0.108] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 0.750 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.463 | [0.375, 0.545] |
| Reversed meaning rate (lower is better) | 0.044 | [0.009, 0.081] |
| Category accuracy on exactly matched spans | 0.880 | [0.750, 1.000] |
| Role accuracy on exactly matched spans | 0.960 | [0.864, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.096 | 0.175 | 0.124 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.069 | 0.200 | 0.103 | 10 |
| UNCERTAIN | 0.029 | 0.125 | 0.048 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.050 | 0.111 | 0.069 | 18 |
| USAGE | 0.049 | 0.130 | 0.071 | 54 |
| ACCESS | 0.149 | 0.241 | 0.184 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.895 | 0.214 | 0.043 |
| 20% | 0.816 | 0.175 | 0.071 |
| 30% | 0.710 | 0.153 | 0.093 |
| 40% | 0.650 | 0.142 | 0.114 |
| 50% | 0.603 | 0.120 | 0.121 |
| 60% | 0.558 | 0.118 | 0.143 |
| 70% | 0.527 | 0.101 | 0.143 |
| 80% | 0.494 | 0.088 | 0.143 |
| 90% | 0.415 | 0.082 | 0.150 |
| 100% | 0.195 | 0.074 | 0.150 |
