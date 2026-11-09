#!/usr/bin/env bash
# Score the transformer ablation run (configs/experiments/ablations.toml) on the development
# machine (no GPU needed).
#
#   bash scripts/gpu/score_ablations.sh ~/Downloads/triggermap-neural-results.tgz
#
# Every run is scored on the held-out half of the model-drafted dev batches 03 and 06
# (splits/selection-v1/holdout.json, never used for early stopping; agreement, not accuracy)
# and on the 10 hand-labelled dev documents. Each variant is then compared, pairwise, with
# the full model trained with the same seed. Unlike score_neural.sh, no run is selected:
# every seed is reported. The test split is not touched.
set -euo pipefail

archive=${1:?usage: score_ablations.sh RESULTS.tgz}
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
OUT=reports/neural/ablation-1
PREFIX=ablation-1

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
tar -xzf "$archive" -C "$tmp" reports/neural/predictions reports/neural/experiment_ablations.md
mkdir -p "$OUT/predictions" "$OUT/metadata"
cp "$tmp/reports/neural/experiment_ablations.md" "$OUT/experiment.md"
cp "$tmp"/reports/neural/predictions/"$PREFIX"-*.jsonl "$OUT/predictions/"
for meta in "$tmp"/reports/neural/predictions/"$PREFIX"-*.metadata.json; do
  cp "$meta" "$OUT/metadata/$(basename "$meta" .metadata.json).json"
done

TM=(uv run --no-sync triggermap)
AGREE=(annotations/batches/batch-03.jsonl)
AGREE_ADD=(--add-gold annotations/batches/batch-06.jsonl --subset splits/selection-v1/holdout.json)
MANUAL=(annotations/pilot/pilot-2.jsonl)

for pred in "$OUT"/predictions/*.jsonl; do
  run=$(basename "$pred" .jsonl)
  "${TM[@]}" evaluate "${AGREE[@]}" "$pred" "${AGREE_ADD[@]}" --split dev \
    --title "Agreement with model drafts (held-out half): $run" \
    --out "$OUT/${run}_dev_holdout.md" >/dev/null
  "${TM[@]}" evaluate "${MANUAL[@]}" "$pred" --split dev --gold-origin manual \
    --title "Hand-labelled dev: $run" --out "$OUT/${run}_dev_manual.md" >/dev/null
done

for variant in no-context no-group docs-60 docs-120; do
  for seed in 0 1 2; do
    a="$OUT/predictions/$PREFIX-full-seed$seed.jsonl"
    b="$OUT/predictions/$PREFIX-$variant-seed$seed.jsonl"
    "${TM[@]}" compare "${AGREE[@]}" "$a" "$b" "${AGREE_ADD[@]}" --split dev \
      --title "Agreement (held-out half), seed $seed: full -> $variant" \
      --out "$OUT/compare_holdout_$variant-seed$seed.md" >/dev/null
    "${TM[@]}" compare "${MANUAL[@]}" "$a" "$b" --split dev --gold-origin manual \
      --title "Hand-labelled dev, seed $seed: full -> $variant" \
      --out "$OUT/compare_manual_$variant-seed$seed.md" >/dev/null
  done
done
echo "scored $(ls "$OUT"/predictions/*.jsonl | wc -l | tr -d ' ') runs into $OUT"
