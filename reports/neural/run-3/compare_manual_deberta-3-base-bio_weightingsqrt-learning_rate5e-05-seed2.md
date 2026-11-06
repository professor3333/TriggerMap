# Hand-labelled dev: crf-batches-01-02 -> deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.346 | -0.024 | [-0.129, +0.185] | no clear difference |
| Exact span F1 | 0.370 | 0.385 | +0.014 | [-0.116, +0.262] | no clear difference |
| Exact span precision | 0.500 | 0.286 | -0.214 | [-0.433, +0.172] | no clear difference |
| Exact span recall | 0.294 | 0.588 | +0.294 | [+0.130, +0.538] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.200 | 0.196 | -0.004 | [-0.099, +0.148] | no clear difference |
| Category macro-F1 | 0.237 | 0.571 | +0.335 | [-0.061, +0.550] | no clear difference |
| Group exact-match F1 | 0.500 | 0.000 | -0.500 | [-1.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.111 | -0.111 | [-0.375, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.500 | +0.167 | [-0.402, +0.462] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 0.900 | -0.100 | [-0.375, +0.714] | no clear difference |
