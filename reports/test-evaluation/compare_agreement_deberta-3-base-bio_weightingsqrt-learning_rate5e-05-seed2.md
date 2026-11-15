# Test split, agreement (146): deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2 minus crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: all; subset `reports/test-evaluation/model_drafted_test_ids.json`; 146 documents)
- Baseline (A): `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/test-evaluation/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 146

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.193 | 0.154 | -0.039 | [-0.080, -0.000] | B clearly worse |
| Exact span F1 | 0.239 | 0.177 | -0.062 | [-0.106, -0.019] | B clearly worse |
| Exact span precision | 0.263 | 0.114 | -0.149 | [-0.208, -0.101] | B clearly worse |
| Exact span recall | 0.219 | 0.393 | +0.174 | [+0.119, +0.228] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.132 | 0.125 | -0.007 | [-0.061, +0.042] | no clear difference |
| Category macro-F1 | 0.187 | 0.158 | -0.029 | [-0.077, +0.015] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.058 | 0.043 | -0.014 | [-0.053, +0.023] | no clear difference |
| Complete-document exact match, documents without conditions | 0.857 | 0.571 | -0.286 | [-0.800, +0.286] | no clear difference |
| False prerequisite rate (lower is better) | 0.482 | 0.650 | +0.168 | [+0.106, +0.239] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.037 | 0.005 | -0.032 | [-0.067, -0.002] | B clearly better |
| Category accuracy on exactly matched spans | 0.859 | 0.893 | +0.034 | [-0.055, +0.126] | no clear difference |
| Role accuracy on exactly matched spans | 0.923 | 0.979 | +0.055 | [-0.002, +0.115] | no clear difference |
