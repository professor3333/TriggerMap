# Hand-labelled dev, seed 2: full -> no-group

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed2.jsonl` (ablation-1-no-group-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-no-group-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.340 | 0.177 | -0.162 | [-0.325, -0.018] | B clearly worse |
| Exact span F1 | 0.377 | 0.203 | -0.175 | [-0.343, -0.030] | B clearly worse |
| Exact span precision | 0.278 | 0.129 | -0.149 | [-0.300, -0.043] | B clearly worse |
| Exact span recall | 0.588 | 0.471 | -0.118 | [-0.353, +0.087] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.191 | 0.115 | -0.077 | [-0.276, +0.002] | no clear difference |
| Category macro-F1 | 0.569 | 0.212 | -0.358 | [-0.536, -0.086] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.484 | 0.622 | +0.138 | [+0.034, +0.220] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 0.875 | -0.025 | [-0.171, +0.032] | no clear difference |
