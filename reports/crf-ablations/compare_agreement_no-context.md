# Agreement (172 model-drafted dev records): full -> no-context

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/crf-ablations/predictions/crf-abl-full.jsonl` (crf-abl-full)
- Candidate (B): `reports/crf-ablations/predictions/crf-abl-no-context.jsonl` (crf-abl-no-context)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-abl-full) | B (crf-abl-no-context) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.139 | -0.006 | [-0.027, +0.020] | no clear difference |
| Exact span F1 | 0.221 | 0.203 | -0.018 | [-0.044, +0.011] | no clear difference |
| Exact span precision | 0.332 | 0.326 | -0.006 | [-0.048, +0.050] | no clear difference |
| Exact span recall | 0.166 | 0.148 | -0.018 | [-0.040, +0.003] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.115 | 0.114 | -0.000 | [-0.011, +0.017] | no clear difference |
| Category macro-F1 | 0.137 | 0.122 | -0.015 | [-0.038, +0.007] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.045 | -0.019 | [-0.043, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.882 | 1.000 | +0.118 | [+0.000, +0.286] | no clear difference |
| False prerequisite rate (lower is better) | 0.353 | 0.377 | +0.024 | [-0.030, +0.073] | no clear difference |
| Reversed meaning rate (lower is better) | 0.074 | 0.064 | -0.010 | [-0.039, +0.009] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.807 | +0.010 | [-0.055, +0.098] | no clear difference |
| Role accuracy on exactly matched spans | 0.859 | 0.860 | +0.000 | [-0.051, +0.044] | no clear difference |
