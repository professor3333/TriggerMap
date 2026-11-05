# Hand-labelled dev: crf-batches-01-02 -> deberta-1-base-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed1.jsonl` (deberta-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-1-base-learning_rate5e-05-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.047 | -0.324 | [-0.587, +0.032] | no clear difference |
| Exact span F1 | 0.370 | 0.054 | -0.316 | [-0.584, +0.036] | no clear difference |
| Exact span precision | 0.500 | 0.029 | -0.471 | [-0.784, +0.019] | no clear difference |
| Exact span recall | 0.294 | 0.412 | +0.118 | [-0.200, +0.438] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.200 | 0.030 | -0.170 | [-0.538, +0.022] | no clear difference |
| Category macro-F1 | 0.237 | 0.036 | -0.201 | [-0.487, +0.029] | no clear difference |
| Group exact-match F1 | 0.500 | 0.000 | -0.500 | [-1.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.000 | -0.222 | [-0.455, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 0.000 | -1.000 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.847 | +0.514 | [-0.141, +0.849] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 0.857 | -0.143 | [-0.364, +0.667] | no clear difference |
