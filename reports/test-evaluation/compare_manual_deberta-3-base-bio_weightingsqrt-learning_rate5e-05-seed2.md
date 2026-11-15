# Test split, hand-labelled (4): deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2 minus crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: manual; 4 documents)
- Baseline (A): `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/test-evaluation/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 4

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.125 | 0.133 | +0.008 | [-0.022, +0.068] | no clear difference |
| Exact span F1 | 0.125 | 0.200 | +0.075 | [-0.022, +0.545] | no clear difference |
| Exact span precision | 0.111 | 0.130 | +0.019 | [-0.071, +0.375] | no clear difference |
| Exact span recall | 0.143 | 0.429 | +0.286 | [+0.000, +1.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.333 | 0.413 | +0.080 | [+0.000, +0.545] | no clear difference |
| Category macro-F1 | 0.111 | 0.206 | +0.095 | [+0.000, +0.143] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.667 | 0.684 | +0.018 | [-0.212, +0.889] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.667 | -0.333 | [-0.500, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
