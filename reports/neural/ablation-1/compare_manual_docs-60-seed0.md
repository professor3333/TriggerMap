# Hand-labelled dev, seed 0: full -> docs-60

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed0.jsonl` (ablation-1-docs-60-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-docs-60-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.364 | 0.029 | -0.335 | [-0.565, -0.122] | B clearly worse |
| Exact span F1 | 0.400 | 0.058 | -0.342 | [-0.600, -0.093] | B clearly worse |
| Exact span precision | 0.289 | 0.038 | -0.251 | [-0.472, -0.070] | B clearly worse |
| Exact span recall | 0.647 | 0.118 | -0.529 | [-0.913, -0.095] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.222 | 0.035 | -0.187 | [-0.584, -0.045] | B clearly worse |
| Category macro-F1 | 0.329 | 0.029 | -0.300 | [-0.630, -0.181] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.000 | -0.111 | [-0.300, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.537 | +0.054 | [-0.191, +0.203] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.050 | +0.050 | [+0.000, +0.125] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.500 | -0.500 | [-1.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.909 | 1.000 | +0.091 | [-1.000, +0.375] | no clear difference |
