# Test split, agreement (146): rules-2 minus crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: all; subset `reports/test-evaluation/model_drafted_test_ids.json`; 146 documents)
- Baseline (A): `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/test-evaluation/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 146

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (rules-2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.193 | 0.048 | -0.145 | [-0.190, -0.105] | B clearly worse |
| Exact span F1 | 0.239 | 0.070 | -0.169 | [-0.221, -0.127] | B clearly worse |
| Exact span precision | 0.263 | 0.101 | -0.162 | [-0.225, -0.111] | B clearly worse |
| Exact span recall | 0.219 | 0.053 | -0.166 | [-0.214, -0.125] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.132 | 0.017 | -0.115 | [-0.160, -0.075] | B clearly worse |
| Category macro-F1 | 0.187 | 0.060 | -0.127 | [-0.175, -0.083] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.058 | 0.000 | -0.058 | [-0.101, -0.016] | B clearly worse |
| Complete-document exact match, documents without conditions | 0.857 | 0.857 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.482 | 0.646 | +0.164 | [+0.061, +0.268] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.037 | 0.043 | +0.006 | [-0.046, +0.066] | no clear difference |
| Category accuracy on exactly matched spans | 0.859 | 0.842 | -0.017 | [-0.237, +0.162] | no clear difference |
| Role accuracy on exactly matched spans | 0.923 | 0.789 | -0.134 | [-0.331, +0.038] | no clear difference |
