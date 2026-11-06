# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.133 | [0.108, 0.164] |
| Exact span F1 | 0.165 | [0.142, 0.194] |
| Exact span precision | 0.108 | [0.090, 0.131] |
| Exact span recall | 0.355 | [0.314, 0.397] |
| Role macro-F1 (roles with gold support) | 0.087 | [0.059, 0.120] |
| Category macro-F1 | 0.129 | [0.100, 0.161] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.026 | [0.006, 0.051] |
| Complete-document exact match, documents without conditions | 0.176 | [0.000, 0.400] |
| False prerequisite rate (lower is better) | 0.607 | [0.565, 0.640] |
| Reversed meaning rate (lower is better) | 0.053 | [0.016, 0.101] |
| Category accuracy on exactly matched spans | 0.898 | [0.836, 0.949] |
| Role accuracy on exactly matched spans | 0.905 | [0.829, 0.970] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.117 | 0.359 | 0.177 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.105 | 0.444 | 0.170 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.073 | 0.250 | 0.113 | 36 |
| USAGE | 0.096 | 0.366 | 0.152 | 186 |
| ACCESS | 0.147 | 0.306 | 0.199 | 134 |
| PLATFORM | 0.030 | 0.167 | 0.051 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.727 | 0.276 | 0.091 |
| 20% | 0.635 | 0.192 | 0.127 |
| 30% | 0.579 | 0.165 | 0.163 |
| 40% | 0.543 | 0.139 | 0.184 |
| 50% | 0.504 | 0.130 | 0.215 |
| 60% | 0.478 | 0.122 | 0.241 |
| 70% | 0.434 | 0.109 | 0.251 |
| 80% | 0.381 | 0.102 | 0.269 |
| 90% | 0.315 | 0.094 | 0.280 |
| 100% | 0.146 | 0.086 | 0.285 |
