# Hand-labelled dev: crf-batches-01-02 -> distilbert-1-base-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed2.jsonl` (distilbert-1-base-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (distilbert-1-base-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.026 | -0.344 | [-0.625, +0.023] | no clear difference |
| Exact span F1 | 0.370 | 0.026 | -0.344 | [-0.625, +0.023] | no clear difference |
| Exact span precision | 0.500 | 0.014 | -0.486 | [-0.803, +0.013] | no clear difference |
| Exact span recall | 0.294 | 0.235 | -0.059 | [-0.438, +0.353] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.200 | 0.020 | -0.180 | [-0.578, +0.019] | no clear difference |
| Category macro-F1 | 0.237 | 0.017 | -0.219 | [-0.514, +0.019] | no clear difference |
| Group exact-match F1 | 0.500 | 0.000 | -0.500 | [-1.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.000 | -0.222 | [-0.455, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.880 | +0.546 | [-0.087, +0.875] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
