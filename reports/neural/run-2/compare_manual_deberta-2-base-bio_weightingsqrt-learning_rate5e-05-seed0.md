# Hand-labelled dev: crf-batches-01-02 -> deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.265 | -0.106 | [-0.313, +0.194] | no clear difference |
| Exact span F1 | 0.370 | 0.294 | -0.076 | [-0.294, +0.239] | no clear difference |
| Exact span precision | 0.500 | 0.196 | -0.304 | [-0.525, +0.150] | no clear difference |
| Exact span recall | 0.294 | 0.588 | +0.294 | [+0.111, +0.545] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.200 | 0.158 | -0.042 | [-0.262, +0.143] | no clear difference |
| Category macro-F1 | 0.237 | 0.285 | +0.048 | [-0.202, +0.324] | no clear difference |
| Group exact-match F1 | 0.500 | 0.000 | -0.500 | [-1.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.000 | -0.222 | [-0.455, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.683 | +0.350 | [-0.233, +0.690] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 0.900 | -0.100 | [-0.333, +0.778] | no clear difference |
