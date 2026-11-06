# Held-out agreement at target precision 0.35: CRF -> DeBERTa

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/calibration/predictions/crf-0.35.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/calibration/predictions/deberta-0.35.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.101 | 0.201 | +0.100 | [+0.024, +0.171] | B clearly better |
| Exact span F1 | 0.101 | 0.221 | +0.120 | [+0.047, +0.188] | B clearly better |
| Exact span precision | 0.444 | 0.373 | -0.072 | [-0.348, +0.145] | no clear difference |
| Exact span recall | 0.057 | 0.157 | +0.100 | [+0.043, +0.162] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.068 | 0.062 | -0.006 | [-0.087, +0.053] | no clear difference |
| Category macro-F1 | 0.089 | 0.123 | +0.034 | [-0.016, +0.095] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.035 | +0.018 | [-0.046, +0.099] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.214 | 0.379 | +0.165 | [-0.108, +0.382] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.909 | -0.091 | [-0.222, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
