# Agreement (held-out half), seed 2: full -> docs-60

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed2.jsonl` (ablation-1-docs-60-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-docs-60-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.185 | 0.107 | -0.078 | [-0.123, -0.031] | B clearly worse |
| Exact span F1 | 0.221 | 0.135 | -0.086 | [-0.136, -0.025] | B clearly worse |
| Exact span precision | 0.162 | 0.094 | -0.068 | [-0.109, -0.022] | B clearly worse |
| Exact span recall | 0.350 | 0.243 | -0.107 | [-0.193, -0.013] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.100 | 0.037 | -0.063 | [-0.125, -0.024] | B clearly worse |
| Category macro-F1 | 0.149 | 0.086 | -0.063 | [-0.101, -0.014] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.000 | -0.018 | [-0.052, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 1.000 | +0.750 | [+0.000, +1.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.584 | +0.101 | [+0.038, +0.170] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.047 | 0.053 | +0.006 | [-0.037, +0.046] | no clear difference |
| Category accuracy on exactly matched spans | 0.857 | 0.794 | -0.063 | [-0.207, +0.056] | no clear difference |
| Role accuracy on exactly matched spans | 0.959 | 0.941 | -0.018 | [-0.112, +0.073] | no clear difference |
