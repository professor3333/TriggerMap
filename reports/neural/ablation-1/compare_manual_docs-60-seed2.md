# Hand-labelled dev, seed 2: full -> docs-60

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed2.jsonl` (ablation-1-docs-60-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-docs-60-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.340 | 0.136 | -0.204 | [-0.431, -0.003] | B clearly worse |
| Exact span F1 | 0.377 | 0.169 | -0.208 | [-0.439, -0.007] | B clearly worse |
| Exact span precision | 0.278 | 0.119 | -0.159 | [-0.356, -0.009] | B clearly worse |
| Exact span recall | 0.588 | 0.294 | -0.294 | [-0.588, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.191 | 0.073 | -0.119 | [-0.411, -0.008] | B clearly worse |
| Category macro-F1 | 0.569 | 0.228 | -0.342 | [-0.551, -0.043] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [-0.273, +0.375] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.484 | 0.538 | +0.055 | [-0.087, +0.185] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 0.800 | -0.100 | [-0.357, +0.000] | no clear difference |
