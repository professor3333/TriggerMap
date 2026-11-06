# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.105 | [0.074, 0.149] |
| Exact span F1 | 0.137 | [0.101, 0.186] |
| Exact span precision | 0.086 | [0.063, 0.122] |
| Exact span recall | 0.336 | [0.255, 0.430] |
| Role macro-F1 (roles with gold support) | 0.068 | [0.040, 0.138] |
| Category macro-F1 | 0.096 | [0.064, 0.138] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.062] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.636 | [0.569, 0.693] |
| Reversed meaning rate (lower is better) | 0.023 | [0.004, 0.046] |
| Category accuracy on exactly matched spans | 0.809 | [0.690, 0.917] |
| Role accuracy on exactly matched spans | 0.936 | [0.865, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.097 | 0.333 | 0.150 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.039 | 0.200 | 0.066 | 10 |
| UNCERTAIN | 0.031 | 0.250 | 0.056 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.064 | 0.278 | 0.104 | 18 |
| USAGE | 0.068 | 0.333 | 0.113 | 54 |
| ACCESS | 0.084 | 0.259 | 0.127 | 54 |
| PLATFORM | 0.028 | 0.071 | 0.040 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.707 | 0.204 | 0.079 |
| 20% | 0.612 | 0.174 | 0.136 |
| 30% | 0.555 | 0.140 | 0.164 |
| 40% | 0.517 | 0.106 | 0.164 |
| 50% | 0.488 | 0.096 | 0.186 |
| 60% | 0.457 | 0.083 | 0.193 |
| 70% | 0.417 | 0.079 | 0.214 |
| 80% | 0.372 | 0.071 | 0.221 |
| 90% | 0.302 | 0.069 | 0.243 |
| 100% | 0.156 | 0.066 | 0.257 |
