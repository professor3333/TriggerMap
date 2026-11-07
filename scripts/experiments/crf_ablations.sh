#!/usr/bin/env bash
# CRF ablations (no heading/list context, no part of speech) and learning curve.
#
#   bash scripts/experiments/crf_ablations.sh
#
# Trains every run of configs/experiments/crf-ablations.toml on the train split of pilot-2,
# batch-01 and batch-02 (the training set of the released crf-batches-01-02). It scores each
# run on the 172 model-drafted dev records (batch-03 + batch-06), then compares the full model
# with each ablation, pairwise, on those records and on the 10 hand-labelled dev documents.
# Nothing is fitted or selected on dev, and the test split is not touched. Scores against
# model drafts are agreement with the drafting model, not accuracy.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }

TM=(uv run --no-sync triggermap)
TRAIN=(annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl annotations/batches/batch-02.jsonl)
DEV=(annotations/batches/batch-03.jsonl annotations/batches/batch-06.jsonl)
SAMPLES=(annotations/pilot/pilot_manifest.json annotations/batches/batch-03.json annotations/batches/batch-06.json)
RUNS=artifacts/experiments/crf-ablations
OUT=reports/crf-ablations
mkdir -p "$OUT/predictions"

"${TM[@]}" experiment --config configs/experiments/crf-ablations.toml --gold "${TRAIN[@]}" \
  --dev-gold "${DEV[@]}" --out-root "$RUNS" --report "$OUT/experiment.md"

for run in full no-context no-pos; do
  "${TM[@]}" predict --model crf --model-dir "$RUNS/crf-abl-$run" --sample "${SAMPLES[@]}" \
    --out "$OUT/predictions/crf-abl-$run.jsonl"
done

for run in no-context no-pos; do
  a="$OUT/predictions/crf-abl-full.jsonl"
  b="$OUT/predictions/crf-abl-$run.jsonl"
  "${TM[@]}" compare "${DEV[0]}" "$a" "$b" --add-gold "${DEV[1]}" --split dev \
    --title "Agreement (172 model-drafted dev records): full -> $run" \
    --out "$OUT/compare_agreement_$run.md" >/dev/null
  "${TM[@]}" compare annotations/pilot/pilot-2.jsonl "$a" "$b" --split dev --gold-origin manual \
    --title "Hand-labelled dev (10): full -> $run" \
    --out "$OUT/compare_manual_$run.md" >/dev/null
done
ls "$OUT"
