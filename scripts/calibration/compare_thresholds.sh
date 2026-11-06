#!/usr/bin/env bash
# Compare the CRF and DeBERTa after review thresholds, as a reviewer would see them unflagged.
#
#   bash scripts/calibration/compare_thresholds.sh
#
# For each model and target precision, `calibrate --method identity` picks the lowest
# confidence threshold whose kept predictions reach the target on the SELECTION half of the
# model-drafted dev records (splits/selection-v1). `threshold` keeps the predictions at or
# above it, and `evaluate` / `compare` score them on the HELD-OUT half only. Every number is
# agreement with model drafts, not accuracy. The test split is not touched.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }

TM=(uv run --no-sync triggermap)
GOLD=(annotations/batches/batch-03.jsonl annotations/batches/batch-06.jsonl)
HOLDOUT=(--add-gold annotations/batches/batch-06.jsonl --subset splits/selection-v1/holdout.json)
OUT=reports/calibration
TARGETS=(0.30 0.35 0.40)
predictions() {  # bash 3.2 (macOS) has no associative arrays
  case "$1" in
    crf) echo reports/agreement/predictions/crf-batches-01-02.jsonl ;;
    deberta) echo reports/neural/run-3/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl ;;
  esac
}
mkdir -p "$OUT/predictions"

for model in crf deberta; do
  for target in "${TARGETS[@]}"; do
    policy="$OUT/$model-identity-$target.yaml"
    "${TM[@]}" calibrate --gold "${GOLD[@]}" --pred "$(predictions "$model")" --gold-origin all \
      --method identity --target-precision "$target" --version "agreement-$model-$target" \
      --out "$policy" >/dev/null
    t=$(sed -n 's/^accept_threshold: //p' "$policy")
    if [ -z "$t" ] || [ "$t" = "null" ]; then
      echo "$model: target $target not reachable on the selection half"
      continue
    fi
    kept="$OUT/predictions/$model-$target.jsonl"
    "${TM[@]}" threshold "$(predictions "$model")" --min-confidence "$t" --out "$kept"
    "${TM[@]}" evaluate "${GOLD[0]}" "$kept" "${HOLDOUT[@]}" --split dev \
      --title "Held-out agreement, $model at target precision $target (threshold $t)" \
      --out "$OUT/${model}-${target}_holdout.md" >/dev/null
  done
done

for target in "${TARGETS[@]}"; do
  a="$OUT/predictions/crf-$target.jsonl"
  b="$OUT/predictions/deberta-$target.jsonl"
  [ -f "$a" ] && [ -f "$b" ] || continue
  "${TM[@]}" compare "${GOLD[0]}" "$a" "$b" "${HOLDOUT[@]}" --split dev \
    --title "Held-out agreement at target precision $target: CRF -> DeBERTa" \
    --out "$OUT/compare_${target}.md" >/dev/null
done
ls "$OUT"
