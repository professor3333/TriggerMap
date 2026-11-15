# Test split, agreement with 146 model-drafted records: rules-2

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: all; subset `reports/test-evaluation/model_drafted_test_ids.json`; 146 documents)
- Predictions: `reports/test-evaluation/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 146 (139 with gold conditions, 7 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.048 | [0.021, 0.082] |
| Exact span F1 | 0.070 | [0.035, 0.110] |
| Exact span precision | 0.101 | [0.051, 0.168] |
| Exact span recall | 0.053 | [0.027, 0.081] |
| Role macro-F1 (roles with gold support) | 0.017 | [0.008, 0.028] |
| Category macro-F1 | 0.060 | [0.024, 0.103] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.857 | [0.500, 1.000] |
| False prerequisite rate (lower is better) | 0.646 | [0.500, 0.762] |
| Reversed meaning rate (lower is better) | 0.043 | [0.000, 0.102] |
| Category accuracy on exactly matched spans | 0.842 | [0.615, 1.000] |
| Role accuracy on exactly matched spans | 0.789 | [0.600, 0.947] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.115 | 0.050 | 0.070 | 299 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 11 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 16 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 30 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.119 | 0.123 | 0.121 | 57 |
| USAGE | 0.111 | 0.036 | 0.055 | 166 |
| ACCESS | 0.030 | 0.022 | 0.025 | 91 |
| PLATFORM | 0.125 | 0.024 | 0.040 | 42 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.600 | 0.053 | 0.003 |
| 20% | 0.600 | 0.053 | 0.006 |
| 30% | 0.600 | 0.054 | 0.008 |
| 40% | 0.550 | 0.040 | 0.008 |
| 50% | 0.550 | 0.053 | 0.014 |
| 60% | 0.550 | 0.062 | 0.020 |
| 70% | 0.550 | 0.083 | 0.031 |
| 80% | 0.400 | 0.080 | 0.034 |
| 90% | 0.350 | 0.071 | 0.034 |
| 100% | 0.350 | 0.069 | 0.037 |
