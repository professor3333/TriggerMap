# Agreement (held-out half), seed 2: full -> no-group

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed2.jsonl` (ablation-1-no-group-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-no-group-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.185 | 0.134 | -0.051 | [-0.081, -0.017] | B clearly worse |
| Exact span F1 | 0.221 | 0.170 | -0.051 | [-0.086, -0.009] | B clearly worse |
| Exact span precision | 0.162 | 0.108 | -0.054 | [-0.079, -0.024] | B clearly worse |
| Exact span recall | 0.350 | 0.400 | +0.050 | [-0.014, +0.120] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.100 | 0.091 | -0.009 | [-0.040, +0.037] | no clear difference |
| Category macro-F1 | 0.149 | 0.106 | -0.043 | [-0.078, +0.006] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.000 | -0.018 | [-0.052, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.000 | -0.250 | [-0.500, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.667 | +0.183 | [+0.132, +0.238] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.047 | 0.044 | -0.003 | [-0.030, +0.021] | no clear difference |
| Category accuracy on exactly matched spans | 0.857 | 0.804 | -0.054 | [-0.166, +0.047] | no clear difference |
| Role accuracy on exactly matched spans | 0.959 | 0.964 | +0.005 | [-0.068, +0.079] | no clear difference |
