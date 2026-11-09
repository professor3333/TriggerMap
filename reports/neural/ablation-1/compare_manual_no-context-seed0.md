# Hand-labelled dev, seed 0: full -> no-context

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed0.jsonl` (ablation-1-no-context-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-no-context-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.364 | 0.291 | -0.073 | [-0.190, +0.021] | no clear difference |
| Exact span F1 | 0.400 | 0.364 | -0.036 | [-0.177, +0.087] | no clear difference |
| Exact span precision | 0.289 | 0.263 | -0.026 | [-0.151, +0.063] | no clear difference |
| Exact span recall | 0.647 | 0.588 | -0.059 | [-0.227, +0.167] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.222 | 0.196 | -0.027 | [-0.177, +0.081] | no clear difference |
| Category macro-F1 | 0.329 | 0.326 | -0.004 | [-0.208, +0.093] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.222 | +0.111 | [+0.000, +0.375] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.500 | +0.017 | [-0.110, +0.091] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.900 | -0.100 | [-0.400, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.909 | 0.900 | -0.009 | [-0.075, +0.067] | no clear difference |
