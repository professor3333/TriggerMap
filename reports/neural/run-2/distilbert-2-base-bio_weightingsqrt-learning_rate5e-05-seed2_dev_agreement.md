# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.075 | [0.051, 0.105] |
| Exact span F1 | 0.101 | [0.077, 0.131] |
| Exact span precision | 0.072 | [0.054, 0.096] |
| Exact span recall | 0.171 | [0.131, 0.215] |
| Role macro-F1 (roles with gold support) | 0.060 | [0.035, 0.092] |
| Category macro-F1 | 0.066 | [0.046, 0.090] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.013 | [0.000, 0.034] |
| Complete-document exact match, documents without conditions | 0.882 | [0.700, 1.000] |
| False prerequisite rate (lower is better) | 0.541 | [0.478, 0.601] |
| Reversed meaning rate (lower is better) | 0.046 | [0.022, 0.074] |
| Category accuracy on exactly matched spans | 0.848 | [0.759, 0.927] |
| Role accuracy on exactly matched spans | 0.879 | [0.756, 0.983] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.074 | 0.158 | 0.101 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.070 | 0.222 | 0.107 | 18 |
| UNCERTAIN | 0.019 | 0.107 | 0.032 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.019 | 0.056 | 0.028 | 36 |
| USAGE | 0.050 | 0.124 | 0.071 | 186 |
| ACCESS | 0.106 | 0.224 | 0.144 | 134 |
| PLATFORM | 0.015 | 0.033 | 0.020 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.825 | 0.130 | 0.031 |
| 20% | 0.734 | 0.103 | 0.049 |
| 30% | 0.657 | 0.083 | 0.060 |
| 40% | 0.608 | 0.070 | 0.067 |
| 50% | 0.562 | 0.065 | 0.078 |
| 60% | 0.525 | 0.071 | 0.101 |
| 70% | 0.492 | 0.062 | 0.104 |
| 80% | 0.444 | 0.058 | 0.111 |
| 90% | 0.381 | 0.057 | 0.122 |
| 100% | 0.196 | 0.053 | 0.127 |
