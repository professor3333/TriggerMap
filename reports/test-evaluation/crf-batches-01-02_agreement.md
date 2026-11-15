# Test split, agreement with 146 model-drafted records: crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: all; subset `reports/test-evaluation/model_drafted_test_ids.json`; 146 documents)
- Predictions: `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 146 (139 with gold conditions, 7 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.193 | [0.154, 0.238] |
| Exact span F1 | 0.239 | [0.194, 0.288] |
| Exact span precision | 0.263 | [0.207, 0.335] |
| Exact span recall | 0.219 | [0.176, 0.266] |
| Role macro-F1 (roles with gold support) | 0.132 | [0.093, 0.179] |
| Category macro-F1 | 0.187 | [0.143, 0.238] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.058 | [0.016, 0.101] |
| Complete-document exact match, documents without conditions | 0.857 | [0.500, 1.000] |
| False prerequisite rate (lower is better) | 0.482 | [0.400, 0.556] |
| Reversed meaning rate (lower is better) | 0.037 | [0.008, 0.073] |
| Category accuracy on exactly matched spans | 0.859 | [0.784, 0.934] |
| Role accuracy on exactly matched spans | 0.923 | [0.867, 0.974] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.279 | 0.211 | 0.240 | 299 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 11 |
| NOT_REQUIRED | 0.137 | 0.438 | 0.209 | 16 |
| UNCERTAIN | 0.100 | 0.067 | 0.080 | 30 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.183 | 0.193 | 0.188 | 57 |
| USAGE | 0.231 | 0.181 | 0.203 | 166 |
| ACCESS | 0.242 | 0.253 | 0.247 | 91 |
| PLATFORM | 0.250 | 0.071 | 0.111 | 42 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.778 | 0.467 | 0.039 |
| 20% | 0.711 | 0.424 | 0.070 |
| 30% | 0.635 | 0.382 | 0.096 |
| 40% | 0.561 | 0.345 | 0.115 |
| 50% | 0.517 | 0.304 | 0.126 |
| 60% | 0.477 | 0.287 | 0.143 |
| 70% | 0.421 | 0.260 | 0.152 |
| 80% | 0.377 | 0.252 | 0.169 |
| 90% | 0.310 | 0.232 | 0.174 |
| 100% | 0.170 | 0.212 | 0.177 |
