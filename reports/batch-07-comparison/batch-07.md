# batch-07: systems against both model drafts (baseline crf-batches-01-02)

- Reference A: `annotations/batches/batch-07.jsonl`
- Reference B: `annotations/second-drafts/batch-07.jsonl`
- Predictions: `reports/batch-07-comparison/predictions/crf-batches-01-02.jsonl`, `reports/batch-07-comparison/predictions/rules-2.jsonl`, `reports/batch-07-comparison/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl`
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 100
- Conditions in A: 182
- Conditions in B: 319
- Consensus conditions (identical in A and B): 94

Scores against model drafts measure agreement with the drafts, not accuracy. 95% bootstrap intervals.

## Scores

| Metric | `crf-batches-01-02` | `rules-2` | `deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0` |
|---|---:|---:|---:|
| Typed F1 vs reference A | 0.158 [0.101, 0.220] | 0.060 [0.009, 0.125] | 0.138 [0.102, 0.176] |
| Typed F1 vs reference B | 0.136 [0.090, 0.189] | 0.054 [0.017, 0.101] | 0.149 [0.116, 0.184] |
| Span F1 vs reference A | 0.192 [0.128, 0.254] | 0.102 [0.042, 0.174] | 0.164 [0.122, 0.206] |
| Span F1 vs reference B | 0.154 [0.112, 0.202] | 0.091 [0.050, 0.139] | 0.196 [0.159, 0.233] |
| Recall on consensus conditions | 0.181 [0.106, 0.264] | 0.064 [0.010, 0.139] | 0.394 [0.293, 0.489] |
| Predictions in both references | 0.156 [0.086, 0.238] | 0.113 [0.017, 0.256] | 0.056 [0.037, 0.079] |
| Predictions in at least one reference | 0.321 [0.240, 0.412] | 0.208 [0.070, 0.395] | 0.143 [0.108, 0.177] |
| Invented prerequisites vs A (lower is better) | 0.530 [0.430, 0.631] | 0.415 [0.271, 0.566] | 0.674 [0.611, 0.729] |
| Invented prerequisites vs B (lower is better) | 0.390 [0.301, 0.480] | 0.245 [0.120, 0.375] | 0.554 [0.487, 0.614] |
| Invented prerequisites vs both (lower is better) | 0.380 [0.291, 0.471] | 0.208 [0.091, 0.342] | 0.504 [0.437, 0.563] |

## `rules-2` minus `crf-batches-01-02` (paired)

*Better* / *worse* means the whole 95% interval lies on one side of zero.

| Metric | Difference | 95% CI | Verdict |
|---|---:|:---:|---|
| Typed F1 vs reference A | -0.099 | [-0.155, -0.026] | worse |
| Typed F1 vs reference B | -0.082 | [-0.127, -0.029] | worse |
| Span F1 vs reference A | -0.090 | [-0.152, -0.016] | worse |
| Span F1 vs reference B | -0.063 | [-0.115, -0.008] | worse |
| Recall on consensus conditions | -0.117 | [-0.200, -0.020] | worse |
| Predictions in both references | -0.043 | [-0.143, +0.087] | unclear |
| Predictions in at least one reference | -0.114 | [-0.240, +0.053] | unclear |
| Invented prerequisites vs A (lower is better) | -0.115 | [-0.262, +0.035] | unclear |
| Invented prerequisites vs B (lower is better) | -0.145 | [-0.286, +0.004] | unclear |
| Invented prerequisites vs both (lower is better) | -0.172 | [-0.311, -0.014] | better |

Typed F1: clearly worse under both references.

Span F1: clearly worse under both references.

## `deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0` minus `crf-batches-01-02` (paired)

*Better* / *worse* means the whole 95% interval lies on one side of zero.

| Metric | Difference | 95% CI | Verdict |
|---|---:|:---:|---|
| Typed F1 vs reference A | -0.020 | [-0.079, +0.035] | unclear |
| Typed F1 vs reference B | +0.014 | [-0.036, +0.063] | unclear |
| Span F1 vs reference A | -0.028 | [-0.090, +0.033] | unclear |
| Span F1 vs reference B | +0.042 | [-0.018, +0.096] | unclear |
| Recall on consensus conditions | +0.213 | [+0.091, +0.319] | better |
| Predictions in both references | -0.100 | [-0.173, -0.036] | worse |
| Predictions in at least one reference | -0.178 | [-0.251, -0.108] | worse |
| Invented prerequisites vs A (lower is better) | +0.144 | [+0.061, +0.219] | worse |
| Invented prerequisites vs B (lower is better) | +0.164 | [+0.071, +0.253] | worse |
| Invented prerequisites vs both (lower is better) | +0.124 | [+0.027, +0.215] | worse |

Typed F1: the direction differs between the references.

Span F1: the direction differs between the references.
