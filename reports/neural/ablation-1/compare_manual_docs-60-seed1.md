# Hand-labelled dev, seed 1: full -> docs-60

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed1.jsonl` (ablation-1-docs-60-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-docs-60-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.281 | 0.148 | -0.133 | [-0.307, -0.036] | B clearly worse |
| Exact span F1 | 0.351 | 0.148 | -0.203 | [-0.401, -0.092] | B clearly worse |
| Exact span precision | 0.250 | 0.094 | -0.156 | [-0.344, -0.067] | B clearly worse |
| Exact span recall | 0.588 | 0.353 | -0.235 | [-0.500, -0.062] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.188 | 0.078 | -0.110 | [-0.294, -0.067] | B clearly worse |
| Category macro-F1 | 0.294 | 0.115 | -0.178 | [-0.509, +0.008] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.000 | -0.111 | [-0.300, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.500 | 0.689 | +0.189 | [+0.079, +0.296] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.375] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.333] | no clear difference |
