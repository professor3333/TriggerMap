# Agreement (held-out half), seed 2: full -> no-context

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed2.jsonl` (ablation-1-no-context-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed2) | B (ablation-1-no-context-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.185 | 0.173 | -0.012 | [-0.044, +0.026] | no clear difference |
| Exact span F1 | 0.221 | 0.208 | -0.013 | [-0.046, +0.025] | no clear difference |
| Exact span precision | 0.162 | 0.149 | -0.013 | [-0.039, +0.018] | no clear difference |
| Exact span recall | 0.350 | 0.343 | -0.007 | [-0.054, +0.044] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.100 | 0.080 | -0.020 | [-0.070, +0.004] | no clear difference |
| Category macro-F1 | 0.149 | 0.138 | -0.011 | [-0.044, +0.029] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.053 | +0.035 | [+0.000, +0.087] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.250 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.483 | 0.506 | +0.023 | [-0.022, +0.064] | no clear difference |
| Reversed meaning rate (lower is better) | 0.047 | 0.053 | +0.005 | [-0.021, +0.036] | no clear difference |
| Category accuracy on exactly matched spans | 0.857 | 0.896 | +0.039 | [-0.040, +0.119] | no clear difference |
| Role accuracy on exactly matched spans | 0.959 | 0.938 | -0.022 | [-0.096, +0.044] | no clear difference |
