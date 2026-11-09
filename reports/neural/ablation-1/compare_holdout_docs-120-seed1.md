# Agreement (held-out half), seed 1: full -> docs-120

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed1.jsonl` (ablation-1-docs-120-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-docs-120-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.198 | 0.141 | -0.057 | [-0.092, -0.024] | B clearly worse |
| Exact span F1 | 0.225 | 0.163 | -0.062 | [-0.092, -0.036] | B clearly worse |
| Exact span precision | 0.156 | 0.110 | -0.046 | [-0.070, -0.026] | B clearly worse |
| Exact span recall | 0.407 | 0.314 | -0.093 | [-0.139, -0.048] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.121 | 0.056 | -0.065 | [-0.128, -0.028] | B clearly worse |
| Category macro-F1 | 0.171 | 0.102 | -0.069 | [-0.109, -0.036] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.070 | 0.018 | -0.053 | [-0.118, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.000 | 0.750 | +0.750 | [+0.000, +1.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.567 | 0.629 | +0.062 | [+0.012, +0.108] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.056 | 0.056 | -0.000 | [-0.044, +0.056] | no clear difference |
| Category accuracy on exactly matched spans | 0.912 | 0.886 | -0.026 | [-0.120, +0.047] | no clear difference |
| Role accuracy on exactly matched spans | 0.947 | 0.955 | +0.007 | [-0.083, +0.089] | no clear difference |
