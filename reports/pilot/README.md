# Pilot baseline reports (dev split only)

First scores of the rules and CRF baselines against the `pilot-2` annotations
(`annotations/pilot/pilot-2.jsonl`). Only documents in the **dev** split of
`splits/pool-v1.json` are scored. The 12 pilot documents in the locked test split were not
evaluated.

## Gold slices

| Slice | Dev documents | What a score means |
|---|---:|---|
| `manual` | 10 (9 with conditions, 1 without; 17 gold conditions) | Accuracy against hand-made labels. |
| `all` | 38 (35 with conditions, 3 without) | Mixes the 10 hand-made records with 28 records from model drafts (`model-pilot-draft-2026-11-01-v1`, accepted or revised without recorded annotation time). It mostly measures agreement with the drafting model, **not accuracy**. |

Another 11 pilot documents are assigned to dev but excluded by the split manifest (enriched
stratum), and 39 are in the train split.

## Headline numbers, `manual` slice

95% project-group bootstrap intervals, 1,000 resamples, seed 0.

| Metric | Rules (`rules-2`) | CRF (`crf-pilot-2`) |
|---|---:|---:|
| Typed-condition micro-F1 | 0.095 [0.000, 0.333] | 0.231 [0.062, 0.417] |
| Exact span F1 | 0.095 [0.000, 0.333] | 0.231 [0.062, 0.417] |
| Role macro-F1 | 0.050 [0.000, 0.261] | 0.120 [0.033, 0.378] |
| Group exact-match F1 | 0.000 | 0.000 |
| Complete-document exact match, with conditions (n=9) | 0.111 [0.000, 0.375] | 0.111 [0.000, 0.375] |
| Complete-document exact match, without conditions (n=1) | 1.000 | 1.000 |
| False-prerequisite rate (lower is better) | 0.750 [0.000, 1.000] | 0.444 [0.000, 0.667] |
| Reversed-meaning rate (lower is better) | 0.000 | 0.000 |

These are preliminary: 10 documents give very wide intervals, and the CRF learned from only
39 pilot training documents, 32 of which come from model drafts. The rules baseline does not
learn, so its `manual`-slice numbers are the same as against `pilot-1`. The CRF trained on
`pilot-1` scored 0.154 typed F1 on the same 10 documents.

## Files

| File | Contents |
|---|---|
| `rules_dev_manual.md`, `crf_dev_manual.md` | Full reports, `manual` slice |
| `rules_dev_all.md`, `crf_dev_all.md` | Full reports, `all` slice (agreement with the draft model, see above) |
| `predictions/rules-2.jsonl`, `predictions/crf-pilot-2.jsonl` | The scored predictions (all 100 pilot documents) |

## Reproduce

```bash
uv run triggermap predict --model rules --sample annotations/pilot/pilot_manifest.json --out reports/pilot/predictions/rules-2.jsonl
uv run triggermap train --gold annotations/pilot/pilot-2.jsonl --out artifacts/crf-pilot-2 --model-id crf-pilot-2
uv run triggermap predict --model crf --model-dir artifacts/crf-pilot-2 --sample annotations/pilot/pilot_manifest.json --out reports/pilot/predictions/crf-pilot-2.jsonl
uv run triggermap evaluate annotations/pilot/pilot-2.jsonl reports/pilot/predictions/rules-2.jsonl --split dev --gold-origin manual --title "Pilot-2 dev: rules, gold origin manual" --out reports/pilot/rules_dev_manual.md
```

Use `--gold-origin all` for the `all` slice and the CRF predictions file for the CRF reports.
