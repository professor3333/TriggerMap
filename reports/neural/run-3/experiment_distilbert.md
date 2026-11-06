# Experiment: distilbert

- Config: `configs/experiments/distilbert.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`, subset `splits/selection-v1/selection.json`: 111 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0 | 239 | 0.042 [0.028, 0.063] | 0.056 [0.040, 0.079] | 0.049 [0.014, 0.071] | 0.000 [0.000, 0.000] | 0.700 [0.642, 0.738] | 8 | 86.2 |
| distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1 | 239 | 0.052 [0.039, 0.070] | 0.072 [0.053, 0.090] | 0.052 [0.020, 0.084] | 0.000 [0.000, 0.000] | 0.627 [0.572, 0.668] | 10 | 106.4 |
| distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2 | 239 | 0.034 [0.019, 0.052] | 0.042 [0.026, 0.062] | 0.025 [0.008, 0.049] | 0.000 [0.000, 0.000] | 0.671 [0.609, 0.720] | 8 | 90.2 |
| distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0 | 239 | 0.096 [0.061, 0.139] | 0.129 [0.094, 0.177] | 0.080 [0.028, 0.149] | 0.000 [0.000, 0.000] | 0.496 [0.398, 0.555] | 18 | 164.4 |
| distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1 | 239 | 0.078 [0.054, 0.113] | 0.110 [0.084, 0.149] | 0.060 [0.029, 0.113] | 0.000 [0.000, 0.000] | 0.558 [0.471, 0.609] | 10 | 107.3 |
| distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2 | 239 | 0.083 [0.057, 0.120] | 0.112 [0.083, 0.150] | 0.028 [0.020, 0.040] | 0.000 [0.000, 0.000] | 0.505 [0.409, 0.582] | 15 | 147.5 |
| distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.000 [0.000, 1.000] | 1 | 49.0 |
| distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed1 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 48.9 |
| distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 49.2 |
| distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0 | 239 | 0.052 [0.029, 0.086] | 0.067 [0.041, 0.100] | 0.038 [0.012, 0.078] | 0.000 [0.000, 0.000] | 0.543 [0.458, 0.609] | 8 | 89.6 |
| distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed1 | 239 | 0.076 [0.053, 0.100] | 0.094 [0.063, 0.123] | 0.093 [0.020, 0.175] | 0.000 [0.000, 0.000] | 0.566 [0.416, 0.645] | 12 | 122.5 |
| distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2 | 239 | 0.053 [0.033, 0.078] | 0.071 [0.044, 0.095] | 0.019 [0.012, 0.026] | 0.000 [0.000, 0.000] | 0.493 [0.379, 0.581] | 12 | 122.5 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| distilbert-3-base-bio_weightingsqrt-learning_rate2e-05 | 3 | 0.042 | 0.009 |
| distilbert-3-base-bio_weightingsqrt-learning_rate5e-05 | 3 | 0.085 | 0.009 |
| distilbert-3-base-bio_weightingnone-learning_rate2e-05 | 3 | 0.000 | 0.000 |
| distilbert-3-base-bio_weightingnone-learning_rate5e-05 | 3 | 0.060 | 0.013 |
