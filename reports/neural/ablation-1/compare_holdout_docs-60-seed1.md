# Agreement (held-out half), seed 1: full -> docs-60

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed1.jsonl` (ablation-1-docs-60-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-docs-60-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.198 | 0.072 | -0.125 | [-0.174, -0.083] | B clearly worse |
| Exact span F1 | 0.225 | 0.075 | -0.150 | [-0.195, -0.112] | B clearly worse |
| Exact span precision | 0.156 | 0.047 | -0.109 | [-0.147, -0.080] | B clearly worse |
| Exact span recall | 0.407 | 0.193 | -0.214 | [-0.277, -0.144] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.121 | 0.027 | -0.094 | [-0.173, -0.051] | B clearly worse |
| Category macro-F1 | 0.171 | 0.050 | -0.121 | [-0.165, -0.083] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.070 | 0.000 | -0.070 | [-0.137, -0.018] | B clearly worse |
| Complete-document exact match, documents without conditions | 0.000 | 0.250 | +0.250 | [+0.000, +1.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.567 | 0.677 | +0.110 | [+0.060, +0.166] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.056 | 0.059 | +0.002 | [-0.059, +0.061] | no clear difference |
| Category accuracy on exactly matched spans | 0.912 | 0.963 | +0.051 | [+0.000, +0.109] | no clear difference |
| Role accuracy on exactly matched spans | 0.947 | 1.000 | +0.053 | [+0.000, +0.111] | no clear difference |
