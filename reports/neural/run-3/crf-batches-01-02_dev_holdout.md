# Agreement with model drafts (held-out half): crf-batches-01-02

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.127 | [0.054, 0.201] |
| Exact span F1 | 0.176 | [0.100, 0.261] |
| Exact span precision | 0.281 | [0.159, 0.434] |
| Exact span recall | 0.129 | [0.070, 0.191] |
| Role macro-F1 (roles with gold support) | 0.103 | [0.034, 0.186] |
| Category macro-F1 | 0.131 | [0.060, 0.200] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.053 | [0.000, 0.123] |
| Complete-document exact match, documents without conditions | 0.750 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.412 | [0.288, 0.538] |
| Reversed meaning rate (lower is better) | 0.108 | [0.000, 0.250] |
| Category accuracy on exactly matched spans | 0.833 | [0.600, 1.000] |
| Role accuracy on exactly matched spans | 0.889 | [0.700, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.275 | 0.117 | 0.164 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.333 | 0.200 | 0.250 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.111 | 0.056 | 0.074 | 18 |
| USAGE | 0.074 | 0.037 | 0.049 | 54 |
| ACCESS | 0.423 | 0.204 | 0.275 | 54 |
| PLATFORM | 0.500 | 0.071 | 0.125 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.781 | 0.667 | 0.029 |
| 20% | 0.696 | 0.462 | 0.043 |
| 30% | 0.605 | 0.421 | 0.057 |
| 41% | 0.533 | 0.308 | 0.057 |
| 50% | 0.473 | 0.281 | 0.064 |
| 59% | 0.430 | 0.289 | 0.079 |
| 70% | 0.388 | 0.267 | 0.086 |
| 80% | 0.350 | 0.255 | 0.093 |
| 91% | 0.307 | 0.224 | 0.093 |
| 100% | 0.186 | 0.203 | 0.093 |
