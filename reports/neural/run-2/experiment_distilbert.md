# Experiment: distilbert

- Config: `configs/experiments/distilbert.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`: 172 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0 | 239 | 0.039 [0.028, 0.053] | 0.056 [0.042, 0.073] | 0.037 [0.020, 0.055] | 0.000 [0.000, 0.000] | 0.724 [0.684, 0.756] | 8 | 101.3 |
| distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed1 | 239 | 0.042 [0.031, 0.054] | 0.058 [0.044, 0.071] | 0.040 [0.020, 0.065] | 0.000 [0.000, 0.000] | 0.662 [0.623, 0.694] | 12 | 147.3 |
| distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2 | 239 | 0.033 [0.023, 0.045] | 0.044 [0.031, 0.058] | 0.025 [0.011, 0.041] | 0.000 [0.000, 0.000] | 0.667 [0.630, 0.700] | 14 | 147.2 |
| distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed0 | 239 | 0.074 [0.051, 0.101] | 0.101 [0.077, 0.128] | 0.047 [0.027, 0.067] | 0.000 [0.000, 0.000] | 0.554 [0.491, 0.603] | 13 | 147.2 |
| distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1 | 239 | 0.041 [0.029, 0.055] | 0.052 [0.039, 0.065] | 0.035 [0.017, 0.058] | 0.000 [0.000, 0.000] | 0.770 [0.744, 0.791] | 4 | 68.8 |
| distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2 | 239 | 0.075 [0.052, 0.103] | 0.101 [0.076, 0.130] | 0.060 [0.033, 0.093] | 0.000 [0.000, 0.000] | 0.541 [0.473, 0.600] | 15 | 147.5 |
| distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 38.8 |
| distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed1 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 38.8 |
| distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 38.9 |
| distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 39.0 |
| distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1 | 239 | 0.064 [0.049, 0.081] | 0.086 [0.063, 0.105] | 0.042 [0.020, 0.080] | 0.000 [0.000, 0.000] | 0.510 [0.429, 0.571] | 14 | 145.8 |
| distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 38.9 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| distilbert-2-base-bio_weightingsqrt-learning_rate2e-05 | 3 | 0.038 | 0.004 |
| distilbert-2-base-bio_weightingsqrt-learning_rate5e-05 | 3 | 0.063 | 0.019 |
| distilbert-2-base-bio_weightingnone-learning_rate2e-05 | 3 | 0.000 | 0.000 |
| distilbert-2-base-bio_weightingnone-learning_rate5e-05 | 3 | 0.021 | 0.037 |
