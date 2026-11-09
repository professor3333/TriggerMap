# Agreement (held-out half), seed 0: full -> no-group

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed0.jsonl` (ablation-1-no-group-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-no-group-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.208 | 0.193 | -0.015 | [-0.060, +0.028] | no clear difference |
| Exact span F1 | 0.244 | 0.224 | -0.020 | [-0.059, +0.018] | no clear difference |
| Exact span precision | 0.179 | 0.162 | -0.017 | [-0.047, +0.015] | no clear difference |
| Exact span recall | 0.386 | 0.364 | -0.021 | [-0.083, +0.031] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.127 | 0.121 | -0.006 | [-0.032, +0.013] | no clear difference |
| Category macro-F1 | 0.193 | 0.166 | -0.027 | [-0.059, +0.008] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.053 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.250 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.428 | 0.459 | +0.031 | [-0.024, +0.089] | no clear difference |
| Reversed meaning rate (lower is better) | 0.046 | 0.047 | +0.001 | [-0.029, +0.029] | no clear difference |
| Category accuracy on exactly matched spans | 0.926 | 0.882 | -0.044 | [-0.122, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.926 | 0.980 | +0.054 | [+0.000, +0.128] | no clear difference |
