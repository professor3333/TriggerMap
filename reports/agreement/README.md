# Agreement with model drafts (dev split only)

Labels after the pilot are model drafts (owner's decision, 2026-11-05; see
[`docs/targets.md`](../../docs/targets.md)). This report scores three systems in two ways:

- **Agreement:** against the 172 model-drafted dev records of `batch-03` (112) and `batch-06`
  (60), all `model_draft_accepted`, guidelines v0.2. These numbers measure how closely a system
  reproduces the drafting model's labels. **They are not accuracy.**
- **Accuracy:** against the 10 hand-labelled dev documents of `pilot-2` (`--gold-origin manual`,
  17 gold conditions), the only accuracy slice that exists.

The test split was not touched. All intervals are 95% project-group bootstrap intervals, 1,000
resamples, seed 0.

| System | Training records (train split) | Origins |
|---|---|---|
| `rules-2` | none (deterministic rules) | n/a |
| `crf-pilot-2-batch-01` | `pilot-2` + `batch-01`: 139 | 7 `manual`, 132 model drafts |
| `crf-batches-01-02` | `pilot-2` + `batch-01` + `batch-02`: 239 | 7 `manual`, 219 `model_draft_accepted`, 13 `model_draft_revised` |

## Agreement: 172 model-drafted dev documents

155 documents have draft conditions (386 conditions) and 17 have none.

| Metric | `rules-2` | `crf-pilot-2-batch-01` | `crf-batches-01-02` |
|---|---:|---:|---:|
| Typed-condition micro-F1 | 0.107 [0.058, 0.154] | 0.128 [0.095, 0.168] | 0.145 [0.105, 0.185] |
| Exact span F1 | 0.142 [0.085, 0.195] | 0.174 [0.134, 0.215] | 0.221 [0.171, 0.268] |
| Exact span precision | 0.272 [0.182, 0.340] | 0.277 [0.215, 0.372] | 0.332 [0.273, 0.400] |
| Exact span recall | 0.096 [0.055, 0.141] | 0.127 [0.090, 0.162] | 0.166 [0.122, 0.216] |
| Group exact-match F1 | 0.000 | 0.000 | 0.000 |
| Document exact match, no conditions | 0.941 [0.840, 1.000] | 0.941 [0.800, 1.000] | 0.882 [0.714, 1.000] |
| False-prerequisite rate (lower is better) | 0.330 [0.165, 0.467] | 0.416 [0.294, 0.493] | 0.353 [0.260, 0.416] |
| Reversed-meaning rate (lower is better) | 0.060 [0.011, 0.132] | 0.090 [0.035, 0.154] | 0.074 [0.029, 0.131] |

## Accuracy: 10 hand-labelled dev documents

| Metric | `rules-2` | `crf-pilot-2-batch-01` | `crf-batches-01-02` |
|---|---:|---:|---:|
| Typed-condition micro-F1 | 0.095 [0.000, 0.333] | 0.444 [0.133, 0.667] | 0.370 [0.000, 0.640] |
| Exact span precision | 0.250 [0.000, 1.000] | 0.600 [0.250, 1.000] | 0.500 [0.000, 0.818] |
| Exact span recall | 0.059 [0.000, 0.231] | 0.353 [0.077, 0.611] | 0.294 [0.000, 0.571] |
| Group exact-match F1 | 0.000 | 0.500 [0.000, 1.000] | 0.500 [0.000, 1.000] |
| False-prerequisite rate (lower is better) | 0.750 [0.000, 1.000] | 0.300 [0.000, 0.750] | 0.333 [0.000, 1.000] |

## Paired differences (same documents, same resamples)

| Comparison | Slice | Typed F1, B − A | Exact span F1, B − A | Report |
|---|---|---:|---:|---|
| `crf-pilot-2-batch-01` → `crf-batches-01-02` (adding `batch-02`) | agreement | +0.017 [−0.014, +0.047] | **+0.047 [+0.004, +0.086]** | [`compare_agreement_batch-02.md`](compare_agreement_batch-02.md) |
| `rules-2` → `crf-batches-01-02` | agreement | +0.038 [−0.012, +0.097] | **+0.079 [+0.028, +0.138]** | [`compare_agreement_rules.md`](compare_agreement_rules.md) |
| `crf-pilot-2-batch-01` → `crf-batches-01-02` (adding `batch-02`) | accuracy | −0.074 [−0.182, +0.000] | −0.074 [−0.182, +0.000] | [`compare_manual_batch-02.md`](compare_manual_batch-02.md) |

Bold marks a clear difference (the whole interval on one side of zero).

## Reading

- **Agreement is low.** Even the best system reproduces about one in six of the drafting
  model's exact spans (span recall 0.166), and typed F1 stays below 0.15. Exact matching is
  strict: a span that differs by one word counts as a miss.
- **Adding `batch-02` clearly improves span agreement** (+0.047 exact span F1) but not typed
  agreement: the interval for typed F1 includes zero.
- **The CRF clearly beats the rules on span agreement** (+0.079), but not on typed F1 or on the
  false-prerequisite rate.
- **On the 10 hand-labelled documents nothing is clear.** Adding `batch-02` moves typed F1 from
  0.444 to 0.370, with a paired interval of [−0.182, +0.000]. Ten documents cannot separate that
  from chance.
- **No group is matched** in the agreement slice. The drafts contain few groups (9 in
  `batch-03`), and no system reproduces one exactly.

None of these numbers is a release result, and agreement is not accuracy.

## Reproduce

```bash
uv run triggermap train --gold annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl annotations/batches/batch-02.jsonl --out artifacts/crf-batches-01-02 --model-id crf-batches-01-02
uv run triggermap predict --model crf --model-dir artifacts/crf-batches-01-02 --sample annotations/pilot/pilot_manifest.json annotations/batches/batch-03.json annotations/batches/batch-06.json --out reports/agreement/predictions/crf-batches-01-02.jsonl
uv run triggermap evaluate annotations/batches/batch-03.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl --add-gold annotations/batches/batch-06.jsonl --split dev --out reports/agreement/crf-batches-01-02_dev_agreement.md
uv run triggermap evaluate annotations/pilot/pilot-2.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl --split dev --gold-origin manual --out reports/agreement/crf-batches-01-02_dev_manual.md
uv run triggermap compare annotations/batches/batch-03.jsonl reports/agreement/predictions/crf-pilot-2-batch-01.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl --add-gold annotations/batches/batch-06.jsonl --split dev --out reports/agreement/compare_agreement_batch-02.md
```

`rules-2` uses `predict` without `--model`, and `crf-pilot-2-batch-01` uses the bundle trained in
[`reports/training-origin/`](../training-origin/README.md).
