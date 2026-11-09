# Hand-labelled dev, seed 1: full -> docs-120

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed1.jsonl` (ablation-1-docs-120-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-docs-120-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.281 | 0.305 | +0.024 | [-0.067, +0.104] | no clear difference |
| Exact span F1 | 0.351 | 0.339 | -0.012 | [-0.167, +0.091] | no clear difference |
| Exact span precision | 0.250 | 0.238 | -0.012 | [-0.149, +0.070] | no clear difference |
| Exact span recall | 0.588 | 0.588 | +0.000 | [-0.200, +0.154] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.188 | 0.204 | +0.017 | [-0.044, +0.098] | no clear difference |
| Category macro-F1 | 0.294 | 0.199 | -0.095 | [-0.341, +0.063] | no clear difference |
| Group exact-match F1 | 0.000 | 0.167 | +0.167 | [+0.000, +0.421] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.500 | 0.545 | +0.045 | [-0.056, +0.127] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 0.900 | 0.900 | +0.000 | [-0.024, +0.083] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 1.000 | +0.100 | [+0.000, +0.333] | no clear difference |
