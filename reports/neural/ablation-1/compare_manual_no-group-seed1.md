# Hand-labelled dev, seed 1: full -> no-group

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed1.jsonl` (ablation-1-no-group-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-no-group-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.281 | 0.310 | +0.030 | [-0.054, +0.134] | no clear difference |
| Exact span F1 | 0.351 | 0.310 | -0.041 | [-0.167, +0.089] | no clear difference |
| Exact span precision | 0.250 | 0.220 | -0.030 | [-0.131, +0.080] | no clear difference |
| Exact span recall | 0.588 | 0.529 | -0.059 | [-0.300, +0.130] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.188 | 0.176 | -0.011 | [-0.079, +0.079] | no clear difference |
| Category macro-F1 | 0.294 | 0.251 | -0.042 | [-0.231, +0.148] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.222 | +0.111 | [+0.000, +0.375] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.500 | 0.571 | +0.071 | [-0.140, +0.173] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.375] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.333] | no clear difference |
