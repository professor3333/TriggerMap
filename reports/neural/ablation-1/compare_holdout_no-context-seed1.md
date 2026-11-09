# Agreement (held-out half), seed 1: full -> no-context

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed1.jsonl` (ablation-1-no-context-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-no-context-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.198 | 0.198 | +0.000 | [-0.028, +0.027] | no clear difference |
| Exact span F1 | 0.225 | 0.233 | +0.007 | [-0.021, +0.033] | no clear difference |
| Exact span precision | 0.156 | 0.160 | +0.004 | [-0.019, +0.025] | no clear difference |
| Exact span recall | 0.407 | 0.429 | +0.021 | [-0.018, +0.060] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.121 | 0.107 | -0.013 | [-0.060, +0.010] | no clear difference |
| Category macro-F1 | 0.171 | 0.179 | +0.008 | [-0.007, +0.031] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.070 | 0.070 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.567 | 0.610 | +0.042 | [+0.005, +0.078] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.056 | 0.030 | -0.027 | [-0.060, +0.004] | no clear difference |
| Category accuracy on exactly matched spans | 0.912 | 0.917 | +0.004 | [-0.040, +0.050] | no clear difference |
| Role accuracy on exactly matched spans | 0.947 | 0.933 | -0.014 | [-0.082, +0.056] | no clear difference |
