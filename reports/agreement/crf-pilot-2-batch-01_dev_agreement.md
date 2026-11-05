# Agreement with model drafts: crf-pilot-2-batch-01

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/agreement/predictions/crf-pilot-2-batch-01.jsonl` (crf-pilot-2-batch-01)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.128 | [0.095, 0.168] |
| Exact span F1 | 0.174 | [0.134, 0.215] |
| Exact span precision | 0.277 | [0.215, 0.372] |
| Exact span recall | 0.127 | [0.090, 0.162] |
| Role macro-F1 (roles with gold support) | 0.089 | [0.041, 0.136] |
| Category macro-F1 | 0.122 | [0.082, 0.161] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.058 | [0.025, 0.097] |
| Complete-document exact match, documents without conditions | 0.941 | [0.800, 1.000] |
| False prerequisite rate (lower is better) | 0.416 | [0.294, 0.493] |
| Reversed meaning rate (lower is better) | 0.090 | [0.035, 0.154] |
| Category accuracy on exactly matched spans | 0.857 | [0.744, 0.944] |
| Role accuracy on exactly matched spans | 0.878 | [0.776, 0.978] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.260 | 0.124 | 0.168 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.214 | 0.167 | 0.188 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.125 | 0.056 | 0.077 | 36 |
| USAGE | 0.167 | 0.086 | 0.113 | 186 |
| ACCESS | 0.365 | 0.172 | 0.234 | 134 |
| PLATFORM | 0.500 | 0.033 | 0.062 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.780 | 0.556 | 0.026 |
| 20% | 0.733 | 0.371 | 0.034 |
| 30% | 0.641 | 0.340 | 0.047 |
| 40% | 0.580 | 0.324 | 0.060 |
| 50% | 0.529 | 0.295 | 0.067 |
| 60% | 0.484 | 0.264 | 0.073 |
| 70% | 0.450 | 0.242 | 0.078 |
| 80% | 0.384 | 0.218 | 0.080 |
| 90% | 0.331 | 0.214 | 0.088 |
| 100% | 0.206 | 0.203 | 0.093 |
