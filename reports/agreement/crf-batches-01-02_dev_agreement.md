# Agreement with model drafts: crf-batches-01-02

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.145 | [0.105, 0.185] |
| Exact span F1 | 0.221 | [0.171, 0.268] |
| Exact span precision | 0.332 | [0.273, 0.400] |
| Exact span recall | 0.166 | [0.122, 0.216] |
| Role macro-F1 (roles with gold support) | 0.115 | [0.065, 0.160] |
| Category macro-F1 | 0.137 | [0.094, 0.174] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.065 | [0.030, 0.104] |
| Complete-document exact match, documents without conditions | 0.882 | [0.714, 1.000] |
| False prerequisite rate (lower is better) | 0.353 | [0.260, 0.416] |
| Reversed meaning rate (lower is better) | 0.074 | [0.029, 0.131] |
| Category accuracy on exactly matched spans | 0.797 | [0.667, 0.880] |
| Role accuracy on exactly matched spans | 0.859 | [0.758, 0.976] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.305 | 0.158 | 0.208 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.286 | 0.222 | 0.250 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.095 | 0.056 | 0.070 | 36 |
| USAGE | 0.189 | 0.097 | 0.128 | 186 |
| ACCESS | 0.405 | 0.224 | 0.288 | 134 |
| PLATFORM | 0.333 | 0.033 | 0.061 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.834 | 0.316 | 0.016 |
| 20% | 0.736 | 0.385 | 0.039 |
| 30% | 0.670 | 0.431 | 0.065 |
| 40% | 0.591 | 0.351 | 0.070 |
| 50% | 0.505 | 0.323 | 0.080 |
| 60% | 0.464 | 0.276 | 0.083 |
| 70% | 0.421 | 0.267 | 0.093 |
| 80% | 0.385 | 0.253 | 0.101 |
| 90% | 0.333 | 0.236 | 0.106 |
| 100% | 0.186 | 0.218 | 0.109 |
