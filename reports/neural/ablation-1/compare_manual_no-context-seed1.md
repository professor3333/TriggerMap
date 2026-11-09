# Hand-labelled dev, seed 1: full -> no-context

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed1.jsonl` (ablation-1-no-context-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-no-context-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.281 | 0.254 | -0.027 | [-0.079, +0.009] | no clear difference |
| Exact span F1 | 0.351 | 0.286 | -0.065 | [-0.108, -0.014] | B clearly worse |
| Exact span precision | 0.250 | 0.196 | -0.054 | [-0.101, -0.012] | B clearly worse |
| Exact span recall | 0.588 | 0.529 | -0.059 | [-0.182, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.188 | 0.148 | -0.039 | [-0.114, -0.009] | B clearly worse |
| Category macro-F1 | 0.294 | 0.265 | -0.029 | [-0.105, +0.062] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.500 | 0.553 | +0.053 | [-0.050, +0.113] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.375] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 0.889 | -0.011 | [-0.086, +0.000] | no clear difference |
