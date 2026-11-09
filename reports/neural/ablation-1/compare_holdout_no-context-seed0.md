# Agreement (held-out half), seed 0: full -> no-context

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/neural/ablation-1/predictions/ablation-1-full-seed0.jsonl` (ablation-1-full-seed0)
- Candidate (B): `reports/neural/ablation-1/predictions/ablation-1-no-context-seed0.jsonl` (ablation-1-no-context-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (ablation-1-full-seed0) | B (ablation-1-no-context-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.208 | 0.227 | +0.019 | [-0.021, +0.062] | no clear difference |
| Exact span F1 | 0.244 | 0.264 | +0.020 | [-0.024, +0.073] | no clear difference |
| Exact span precision | 0.179 | 0.195 | +0.016 | [-0.018, +0.061] | no clear difference |
| Exact span recall | 0.386 | 0.407 | +0.021 | [-0.038, +0.085] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.127 | 0.137 | +0.011 | [-0.026, +0.038] | no clear difference |
| Category macro-F1 | 0.193 | 0.187 | -0.006 | [-0.037, +0.038] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.070 | +0.018 | [+0.000, +0.052] | no clear difference |
| Complete-document exact match, documents without conditions | 0.250 | 0.250 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.428 | 0.466 | +0.038 | [-0.021, +0.091] | no clear difference |
| Reversed meaning rate (lower is better) | 0.046 | 0.065 | +0.018 | [+0.001, +0.043] | B clearly worse |
| Category accuracy on exactly matched spans | 0.926 | 0.912 | -0.014 | [-0.045, +0.009] | no clear difference |
| Role accuracy on exactly matched spans | 0.926 | 0.947 | +0.021 | [-0.035, +0.086] | no clear difference |
