# Agreement: adding batch-02 (crf-pilot-2-batch-01 -> crf-batches-01-02)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/crf-pilot-2-batch-01.jsonl` (crf-pilot-2-batch-01)
- Candidate (B): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-pilot-2-batch-01) | B (crf-batches-01-02) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.128 | 0.145 | +0.017 | [-0.014, +0.047] | no clear difference |
| Exact span F1 | 0.174 | 0.221 | +0.047 | [+0.004, +0.086] | B clearly better |
| Exact span precision | 0.277 | 0.332 | +0.055 | [-0.026, +0.108] | no clear difference |
| Exact span recall | 0.127 | 0.166 | +0.039 | [+0.006, +0.069] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.089 | 0.115 | +0.026 | [-0.001, +0.059] | no clear difference |
| Category macro-F1 | 0.122 | 0.137 | +0.015 | [-0.007, +0.035] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.058 | 0.065 | +0.006 | [-0.015, +0.027] | no clear difference |
| Complete-document exact match, documents without conditions | 0.941 | 0.882 | -0.059 | [-0.160, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.416 | 0.353 | -0.062 | [-0.124, +0.036] | no clear difference |
| Reversed meaning rate (lower is better) | 0.090 | 0.074 | -0.016 | [-0.054, +0.014] | no clear difference |
| Category accuracy on exactly matched spans | 0.857 | 0.797 | -0.060 | [-0.138, -0.003] | B clearly worse |
| Role accuracy on exactly matched spans | 0.878 | 0.859 | -0.018 | [-0.071, +0.064] | no clear difference |
