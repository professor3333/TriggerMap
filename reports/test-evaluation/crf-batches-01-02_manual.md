# Test split, 4 hand-labelled records: crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: manual; 4 documents)
- Predictions: `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 4 (3 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.125 | [0.000, 0.182] |
| Exact span F1 | 0.125 | [0.000, 0.182] |
| Exact span precision | 0.111 | [0.000, 0.143] |
| Exact span recall | 0.143 | [0.000, 0.250] |
| Role macro-F1 (roles with gold support) | 0.333 | [0.000, 0.333] |
| Category macro-F1 | 0.111 | [0.000, 0.200] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.667 | [0.000, 0.750] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.000 | 0.000 | 0.000 | 6 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.500 | 1.000 | 0.667 | 1 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 0 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 0 |
| USAGE | 0.000 | 0.000 | 0.000 | 3 |
| ACCESS | 0.200 | 1.000 | 0.333 | 1 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 3 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.929 | 1.000 | 0.143 |
| 22% | 0.887 | 0.500 | 0.143 |
| 33% | 0.698 | 0.333 | 0.143 |
| 44% | 0.693 | 0.250 | 0.143 |
| 44% | 0.693 | 0.250 | 0.143 |
| 56% | 0.619 | 0.200 | 0.143 |
| 67% | 0.444 | 0.167 | 0.143 |
| 78% | 0.440 | 0.143 | 0.143 |
| 89% | 0.317 | 0.125 | 0.143 |
| 100% | 0.239 | 0.111 | 0.143 |
