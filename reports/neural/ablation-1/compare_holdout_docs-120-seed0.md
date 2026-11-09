# Agreement (held-out half), seed 0: full -> docs-120

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed0.jsonl` (ablation-1-docs-120-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-docs-120-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.208 | 0.089 | -0.120 | [-0.180, -0.063] | B clearly worse |
| Exact span F1 | 0.244 | 0.109 | -0.136 | [-0.196, -0.076] | B clearly worse |
| Exact span precision | 0.179 | 0.068 | -0.111 | [-0.161, -0.066] | B clearly worse |
| Exact span recall | 0.386 | 0.271 | -0.114 | [-0.220, -0.014] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.127 | 0.049 | -0.078 | [-0.183, -0.017] | B clearly worse |
| Category macro-F1 | 0.193 | 0.070 | -0.123 | [-0.182, -0.072] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.000 | -0.053 | [-0.131, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.000 | -0.250 | [-0.500, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.428 | 0.668 | +0.240 | [+0.160, +0.312] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.046 | 0.033 | -0.014 | [-0.059, +0.027] | no clear difference |
| Category accuracy on exactly matched spans | 0.926 | 0.842 | -0.084 | [-0.173, +0.004] | no clear difference |
| Role accuracy on exactly matched spans | 0.926 | 0.974 | +0.048 | [-0.047, +0.154] | no clear difference |
