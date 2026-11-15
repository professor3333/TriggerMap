# Test split, agreement with 146 model-drafted records: deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: all; subset `reports/test-evaluation/model_drafted_test_ids.json`; 146 documents)
- Predictions: `reports/test-evaluation/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 146 (139 with gold conditions, 7 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.154 | [0.125, 0.186] |
| Exact span F1 | 0.177 | [0.146, 0.207] |
| Exact span precision | 0.114 | [0.092, 0.137] |
| Exact span recall | 0.393 | [0.337, 0.444] |
| Role macro-F1 (roles with gold support) | 0.125 | [0.087, 0.171] |
| Category macro-F1 | 0.158 | [0.126, 0.197] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.043 | [0.014, 0.075] |
| Complete-document exact match, documents without conditions | 0.571 | [0.167, 1.000] |
| False prerequisite rate (lower is better) | 0.650 | [0.605, 0.691] |
| Reversed meaning rate (lower is better) | 0.005 | [0.000, 0.014] |
| Category accuracy on exactly matched spans | 0.893 | [0.835, 0.946] |
| Role accuracy on exactly matched spans | 0.979 | [0.955, 0.994] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.135 | 0.401 | 0.202 | 299 |
| EXCEPTION | 0.088 | 0.273 | 0.133 | 11 |
| NOT_REQUIRED | 0.063 | 0.562 | 0.114 | 16 |
| UNCERTAIN | 0.031 | 0.167 | 0.053 | 30 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.133 | 0.316 | 0.188 | 57 |
| USAGE | 0.095 | 0.343 | 0.149 | 166 |
| ACCESS | 0.112 | 0.429 | 0.177 | 91 |
| PLATFORM | 0.077 | 0.262 | 0.119 | 42 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.953 | 0.382 | 0.132 |
| 20% | 0.886 | 0.286 | 0.197 |
| 30% | 0.803 | 0.220 | 0.228 |
| 40% | 0.732 | 0.185 | 0.256 |
| 50% | 0.669 | 0.161 | 0.278 |
| 60% | 0.616 | 0.145 | 0.301 |
| 70% | 0.569 | 0.132 | 0.317 |
| 80% | 0.520 | 0.120 | 0.331 |
| 90% | 0.447 | 0.110 | 0.340 |
| 100% | 0.203 | 0.099 | 0.343 |
