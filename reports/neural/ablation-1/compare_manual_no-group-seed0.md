# Hand-labelled dev, seed 0: full -> no-group

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed0.jsonl` (ablation-1-no-group-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-no-group-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.364 | 0.355 | -0.009 | [-0.113, +0.101] | no clear difference |
| Exact span F1 | 0.400 | 0.387 | -0.013 | [-0.124, +0.100] | no clear difference |
| Exact span precision | 0.289 | 0.267 | -0.023 | [-0.143, +0.071] | no clear difference |
| Exact span recall | 0.647 | 0.706 | +0.059 | [+0.000, +0.182] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.222 | 0.216 | -0.007 | [-0.101, +0.088] | no clear difference |
| Category macro-F1 | 0.329 | 0.442 | +0.113 | [-0.022, +0.219] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.514 | +0.032 | [-0.038, +0.104] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.909 | 0.917 | +0.008 | [+0.000, +0.083] | no clear difference |
