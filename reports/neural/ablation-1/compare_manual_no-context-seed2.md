# Hand-labelled dev, seed 2: full -> no-context

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed2.jsonl` (ablation-1-no-context-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-no-context-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.340 | 0.222 | -0.117 | [-0.232, -0.034] | B clearly worse |
| Exact span F1 | 0.377 | 0.254 | -0.123 | [-0.238, -0.041] | B clearly worse |
| Exact span precision | 0.278 | 0.174 | -0.104 | [-0.197, -0.040] | B clearly worse |
| Exact span recall | 0.588 | 0.471 | -0.118 | [-0.308, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.191 | 0.127 | -0.064 | [-0.221, -0.015] | B clearly worse |
| Category macro-F1 | 0.569 | 0.237 | -0.333 | [-0.498, -0.022] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.484 | 0.462 | -0.022 | [-0.093, +0.051] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 0.875 | -0.025 | [-0.267, +0.000] | no clear difference |
