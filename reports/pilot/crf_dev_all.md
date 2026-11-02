# Pilot dev: crf, gold origin all

- Gold: `annotations/pilot/pilot-1.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 38 documents)
- Predictions: `reports/pilot/predictions/crf-pilot-1.jsonl` (crf-1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 38 (34 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.065 | [0.013, 0.133] |
| Exact span F1 | 0.090 | [0.025, 0.161] |
| Exact span precision | 0.179 | [0.050, 0.308] |
| Exact span recall | 0.060 | [0.016, 0.114] |
| Role macro-F1 (roles with gold support) | 0.031 | [0.009, 0.064] |
| Category macro-F1 | 0.070 | [0.011, 0.139] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.029 | [0.000, 0.091] |
| Complete-document exact match, documents without conditions | 0.750 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.487 | [0.378, 0.606] |
| Reversed meaning rate (lower is better) | 0.050 | [0.000, 0.158] |
| Category accuracy on exactly matched spans | 0.714 | [0.333, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.179 | 0.064 | 0.094 | 110 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 3 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 3 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.500 | 0.077 | 0.133 | 13 |
| USAGE | 0.074 | 0.030 | 0.043 | 67 |
| ACCESS | 0.250 | 0.065 | 0.103 | 31 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 5 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.918 | 0.250 | 0.009 |
| 21% | 0.777 | 0.250 | 0.017 |
| 31% | 0.693 | 0.333 | 0.034 |
| 41% | 0.587 | 0.250 | 0.034 |
| 51% | 0.550 | 0.200 | 0.034 |
| 59% | 0.531 | 0.174 | 0.034 |
| 69% | 0.499 | 0.148 | 0.034 |
| 79% | 0.437 | 0.129 | 0.034 |
| 90% | 0.364 | 0.114 | 0.034 |
| 100% | 0.246 | 0.128 | 0.043 |
