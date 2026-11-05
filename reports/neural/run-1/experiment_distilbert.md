# Experiment: distilbert

- Config: `configs/experiments/distilbert.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`: 172 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| distilbert-1-base-learning_rate2e-05-seed0 | 239 | 0.007 [0.004, 0.010] | 0.010 [0.007, 0.014] | 0.006 [0.003, 0.008] | 0.000 [0.000, 0.000] | 0.859 [0.841, 0.875] | 5 | 61.4 |
| distilbert-1-base-learning_rate2e-05-seed1 | 239 | 0.007 [0.004, 0.010] | 0.010 [0.007, 0.014] | 0.005 [0.003, 0.008] | 0.000 [0.000, 0.000] | 0.865 [0.847, 0.879] | 5 | 64.1 |
| distilbert-1-base-learning_rate2e-05-seed2 | 239 | 0.006 [0.004, 0.009] | 0.010 [0.006, 0.014] | 0.005 [0.002, 0.009] | 0.000 [0.000, 0.000] | 0.867 [0.849, 0.882] | 6 | 69.0 |
| distilbert-1-base-learning_rate5e-05-seed0 | 239 | 0.019 [0.013, 0.026] | 0.025 [0.018, 0.033] | 0.012 [0.007, 0.017] | 0.000 [0.000, 0.000] | 0.839 [0.815, 0.858] | 6 | 62.5 |
| distilbert-1-base-learning_rate5e-05-seed1 | 239 | 0.018 [0.013, 0.026] | 0.026 [0.020, 0.035] | 0.012 [0.008, 0.018] | 0.000 [0.000, 0.000] | 0.845 [0.826, 0.862] | 6 | 62.8 |
| distilbert-1-base-learning_rate5e-05-seed2 | 239 | 0.019 [0.013, 0.027] | 0.026 [0.019, 0.035] | 0.012 [0.008, 0.019] | 0.000 [0.000, 0.000] | 0.845 [0.827, 0.862] | 6 | 63.8 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| distilbert-1-base-learning_rate2e-05 | 3 | 0.007 | 0.001 |
| distilbert-1-base-learning_rate5e-05 | 3 | 0.019 | 0.000 |
