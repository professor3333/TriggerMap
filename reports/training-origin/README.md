# Training-data origin (dev split only)

Does training on model-made labels help or hurt on hand-made labels? Three CRF bundles share
features and hyperparameters and differ only in their training records. All three are scored
on the **10 hand-labelled pilot documents in the dev split** (`pilot-2`, `--gold-origin manual`,
17 gold conditions). The test split was not touched.

| Bundle | Training records (train split) | Origins |
|---|---|---|
| `crf-pilot-2-manual` | `pilot-2`, `--origin manual` | 7 `manual` |
| `crf-pilot-2` | `pilot-2` | 39: 7 `manual`, 32 model drafts (v0.1) |
| `crf-pilot-2-batch-01` | `pilot-2` + `batch-01` | 139: 7 `manual`, 120 `model_draft_accepted`, 12 `model_draft_revised` |

Each bundle's `metadata.json` records these counts under `training_origins`.

## Results, `manual` dev slice

95% project-group bootstrap intervals, 1,000 resamples, seed 0.

| Metric | `crf-pilot-2-manual` | `crf-pilot-2` | `crf-pilot-2-batch-01` |
|---|---:|---:|---:|
| Typed-condition micro-F1 | 0.300 [0.000, 0.556] | 0.231 [0.062, 0.417] | 0.444 [0.133, 0.667] |
| Exact span precision | 1.000 [0.000, 1.000] | 0.333 [0.111, 1.000] | 0.600 [0.250, 1.000] |
| Exact span recall | 0.176 [0.000, 0.385] | 0.176 [0.043, 0.375] | 0.353 [0.077, 0.611] |
| Group exact-match F1 | 0.000 | 0.000 | 0.500 [0.000, 1.000] |
| False-prerequisite rate (lower is better) | 0.000 | 0.444 [0.000, 0.667] | 0.300 [0.000, 0.750] |

Paired differences (same documents, same resamples):

| Comparison | Typed F1, B − A | 95% CI | Report |
|---|---:|:---:|---|
| `crf-pilot-2` → `crf-pilot-2-batch-01` | +0.214 | [−0.026, +0.457] | [`compare_batch-01.md`](compare_batch-01.md) |
| `crf-pilot-2-manual` → `crf-pilot-2` | −0.069 | [−0.260, +0.121] | [`compare_manual_only.md`](compare_manual_only.md) |

**Reading.** No difference is clear: every paired interval includes zero. Adding `batch-01`
moves every headline metric in the right direction (typed F1 +0.21, false-prerequisite rate
−0.14), but 10 documents cannot separate that from chance. The 7-document manual-only bundle
predicts very little (3 conditions, all correct), so its 0.000 false-prerequisite rate comes
from abstaining, not from accuracy. These results do not show that model-made training labels
help. The question is re-run when the hand-labelled dev batch (`batch-03`) exists.

## Reproduce

```bash
uv run triggermap train --gold annotations/pilot/pilot-2.jsonl --origin manual --out artifacts/crf-pilot-2-manual --model-id crf-pilot-2-manual
uv run triggermap train --gold annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl --out artifacts/crf-pilot-2-batch-01 --model-id crf-pilot-2-batch-01
uv run triggermap predict --model crf --model-dir artifacts/crf-pilot-2-batch-01 --sample annotations/pilot/pilot_manifest.json --out reports/training-origin/predictions/crf-pilot-2-batch-01.jsonl
uv run triggermap compare annotations/pilot/pilot-2.jsonl reports/pilot/predictions/crf-pilot-2.jsonl reports/training-origin/predictions/crf-pilot-2-batch-01.jsonl --split dev --gold-origin manual --out reports/training-origin/compare_batch-01.md
```

The same `predict` and `compare` commands with `crf-pilot-2-manual` give the other files, and
`evaluate … --split dev --gold-origin manual` gives the per-bundle reports.
