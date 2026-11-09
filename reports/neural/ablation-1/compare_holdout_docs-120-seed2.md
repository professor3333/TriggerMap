# Agreement (held-out half), seed 2: full -> docs-120

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed2.jsonl` (ablation-1-docs-120-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-docs-120-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.185 | 0.061 | -0.124 | [-0.169, -0.083] | B clearly worse |
| Exact span F1 | 0.221 | 0.085 | -0.136 | [-0.180, -0.097] | B clearly worse |
| Exact span precision | 0.162 | 0.050 | -0.112 | [-0.151, -0.081] | B clearly worse |
| Exact span recall | 0.350 | 0.286 | -0.064 | [-0.149, +0.014] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.100 | 0.026 | -0.073 | [-0.143, -0.035] | B clearly worse |
| Category macro-F1 | 0.149 | 0.061 | -0.088 | [-0.131, -0.040] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.000 | -0.018 | [-0.052, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.000 | -0.250 | [-0.500, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.793 | +0.310 | [+0.256, +0.369] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.047 | 0.043 | -0.005 | [-0.042, +0.035] | no clear difference |
| Category accuracy on exactly matched spans | 0.857 | 0.775 | -0.082 | [-0.290, +0.072] | no clear difference |
| Role accuracy on exactly matched spans | 0.959 | 0.900 | -0.059 | [-0.183, +0.057] | no clear difference |
