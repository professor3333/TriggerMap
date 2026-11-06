# Hand-labelled dev: crf-batches-01-02 -> distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.227 | -0.143 | [-0.346, +0.077] | no clear difference |
| Exact span F1 | 0.370 | 0.227 | -0.143 | [-0.346, +0.077] | no clear difference |
| Exact span precision | 0.500 | 0.185 | -0.315 | [-0.607, +0.062] | no clear difference |
| Exact span recall | 0.294 | 0.294 | +0.000 | [-0.143, +0.182] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.200 | 0.135 | -0.065 | [-0.287, +0.071] | no clear difference |
| Category macro-F1 | 0.237 | 0.184 | -0.052 | [-0.224, +0.124] | no clear difference |
| Group exact-match F1 | 0.500 | 0.000 | -0.500 | [-1.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.000 | -0.222 | [-0.455, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.429 | +0.095 | [-0.333, +0.375] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +1.000] | no clear difference |
