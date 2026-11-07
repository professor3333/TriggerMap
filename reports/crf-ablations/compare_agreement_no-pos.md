# Agreement (172 model-drafted dev records): full -> no-pos

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/crf-ablations/predictions/crf-abl-full.jsonl` (crf-abl-full)
- Candidate (B): `reports/crf-ablations/predictions/crf-abl-no-pos.jsonl` (crf-abl-no-pos)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-abl-full) | B (crf-abl-no-pos) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.147 | +0.002 | [-0.025, +0.032] | no clear difference |
| Exact span F1 | 0.221 | 0.217 | -0.004 | [-0.035, +0.031] | no clear difference |
| Exact span precision | 0.332 | 0.333 | +0.002 | [-0.046, +0.070] | no clear difference |
| Exact span recall | 0.166 | 0.161 | -0.005 | [-0.030, +0.022] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.115 | 0.121 | +0.006 | [-0.015, +0.035] | no clear difference |
| Category macro-F1 | 0.137 | 0.140 | +0.003 | [-0.021, +0.031] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.045 | -0.019 | [-0.041, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.882 | 1.000 | +0.118 | [+0.000, +0.286] | no clear difference |
| False prerequisite rate (lower is better) | 0.353 | 0.331 | -0.022 | [-0.089, +0.024] | no clear difference |
| Reversed meaning rate (lower is better) | 0.074 | 0.085 | +0.011 | [-0.037, +0.054] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.806 | +0.010 | [-0.058, +0.097] | no clear difference |
| Role accuracy on exactly matched spans | 0.859 | 0.871 | +0.012 | [-0.009, +0.036] | no clear difference |
