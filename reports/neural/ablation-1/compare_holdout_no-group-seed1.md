# Agreement (held-out half), seed 1: full -> no-group

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-group-seed1.jsonl` (ablation-1-no-group-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed1) | B (ablation-1-no-group-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.198 | 0.228 | +0.030 | [-0.003, +0.064] | no clear difference |
| Exact span F1 | 0.225 | 0.287 | +0.062 | [+0.030, +0.098] | B clearly better |
| Exact span precision | 0.156 | 0.220 | +0.064 | [+0.037, +0.095] | B clearly better |
| Exact span recall | 0.407 | 0.414 | +0.007 | [-0.034, +0.051] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.121 | 0.127 | +0.007 | [-0.038, +0.034] | no clear difference |
| Category macro-F1 | 0.171 | 0.217 | +0.047 | [+0.019, +0.080] | B clearly better |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.070 | 0.070 | +0.000 | [-0.046, +0.054] | no clear difference |
| Complete-document exact match, documents without conditions | 0.000 | 0.250 | +0.250 | [+0.000, +0.500] | no clear difference |
| False prerequisite rate (lower is better) | 0.567 | 0.498 | -0.070 | [-0.117, -0.024] | B clearly better |
| Reversed meaning rate (lower is better) | 0.056 | 0.065 | +0.009 | [-0.038, +0.055] | no clear difference |
| Category accuracy on exactly matched spans | 0.912 | 0.879 | -0.033 | [-0.111, +0.027] | no clear difference |
| Role accuracy on exactly matched spans | 0.947 | 0.914 | -0.034 | [-0.099, +0.027] | no clear difference |
