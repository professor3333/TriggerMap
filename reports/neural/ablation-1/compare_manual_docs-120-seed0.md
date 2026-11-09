# Hand-labelled dev, seed 0: full -> docs-120

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed0.jsonl` (ablation-1-docs-120-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-docs-120-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.364 | 0.148 | -0.215 | [-0.308, -0.110] | B clearly worse |
| Exact span F1 | 0.400 | 0.173 | -0.227 | [-0.382, -0.075] | B clearly worse |
| Exact span precision | 0.289 | 0.109 | -0.180 | [-0.321, -0.068] | B clearly worse |
| Exact span recall | 0.647 | 0.412 | -0.235 | [-0.533, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.222 | 0.096 | -0.126 | [-0.351, -0.037] | B clearly worse |
| Category macro-F1 | 0.329 | 0.105 | -0.224 | [-0.518, -0.128] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.100 | +0.100 | [+0.000, +0.353] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [-0.250, +0.333] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.632 | +0.149 | [-0.028, +0.286] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.857 | -0.143 | [-1.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.909 | 1.000 | +0.091 | [+0.000, +0.375] | no clear difference |
