# Agreement (held-out half), seed 0: full -> docs-60

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed0.jsonl` (ablation-1-docs-60-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-docs-60-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.208 | 0.046 | -0.162 | [-0.219, -0.110] | B clearly worse |
| Exact span F1 | 0.244 | 0.060 | -0.185 | [-0.238, -0.137] | B clearly worse |
| Exact span precision | 0.179 | 0.039 | -0.140 | [-0.186, -0.102] | B clearly worse |
| Exact span recall | 0.386 | 0.129 | -0.257 | [-0.338, -0.184] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.127 | 0.017 | -0.109 | [-0.198, -0.061] | B clearly worse |
| Category macro-F1 | 0.193 | 0.035 | -0.159 | [-0.211, -0.114] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.018 | -0.035 | [-0.087, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.500 | +0.250 | [+0.000, +1.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.428 | 0.637 | +0.209 | [+0.122, +0.293] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.046 | 0.031 | -0.016 | [-0.055, +0.020] | no clear difference |
| Category accuracy on exactly matched spans | 0.926 | 0.778 | -0.148 | [-0.331, +0.020] | no clear difference |
| Role accuracy on exactly matched spans | 0.926 | 1.000 | +0.074 | [+0.000, +0.178] | no clear difference |
