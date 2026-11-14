#!/usr/bin/env bash
# Reproduce the rules and CRF results from a fresh clone and the pinned advisory snapshot.
#
#   bash scripts/reproduce/clean_clone.sh WORKDIR [REPO_URL] [REF]
#
# WORKDIR must be empty or absent. The script clones the repository (default: the public
# GitHub repository, branch main), installs the locked environment (uv sync --locked, CRF
# extras), fetches the pinned advisory-database commit and rebuilds the corpus. It then
# regenerates these committed artefacts in place:
#
#   data/manifests/snapshot.json                         (corpus build)
#   reports/agreement/predictions/{rules-2,crf-batches-01-02}.jsonl
#   reports/agreement/{rules-2,crf-batches-01-02}_dev_agreement.md, crf-batches-01-02_dev_manual.md
#   reports/drafter-consistency/                          (draft-2 conversion and report)
#   reports/batch-07-comparison/                          (CRF and rules predictions, report)
#
# The CRF is retrained from the annotations; nothing is downloaded from a release. The tolerance
# is exact: every regenerated file must be byte-identical to the committed one, so the clone's
# `git status` must stay clean. Transformer results need a GPU and are not covered. Needs
# network access (GitHub, PyPI) and about 1.5 GB of disk.
set -euo pipefail

WORK=${1:?usage: clean_clone.sh WORKDIR [REPO_URL] [REF]}
REPO=${2:-https://github.com/professor3333/TriggerMap.git}
REF=${3:-main}
SNAPSHOT=1912cbd6ce9d4cb141636adc4abafb4eb77a93e6
CORPUS_SHA256=734043ff982a337f6cc593745160e997f20ee62609183ff857edce3d47d2b655

if [ -e "$WORK" ] && [ -n "$(ls -A "$WORK")" ]; then
  echo "$WORK is not empty" >&2
  exit 1
fi
mkdir -p "$WORK"
git clone --quiet --branch "$REF" "$REPO" "$WORK/TriggerMap"
cd "$WORK/TriggerMap"
echo "== clone: $(git rev-parse HEAD)"

uv sync --locked --quiet --extra baselines
TM=(uv run --no-sync triggermap)

echo "== corpus from snapshot $SNAPSHOT"
"${TM[@]}" ingest fetch --commit "$SNAPSHOT"
"${TM[@]}" ingest build
uv run --no-sync python -I - "$CORPUS_SHA256" <<'EOF'
import hashlib, sys
digest = hashlib.sha256(open("data/processed/advisories.jsonl", "rb").read()).hexdigest()
assert digest == sys.argv[1], f"corpus sha256 {digest} != {sys.argv[1]}"
print("corpus sha256 matches")
EOF

echo "== rules-2 and crf-batches-01-02 on the pilot and dev batches"
SAMPLES=(annotations/pilot/pilot_manifest.json annotations/batches/batch-03.json annotations/batches/batch-06.json)
AGREE=reports/agreement
"${TM[@]}" predict --sample "${SAMPLES[@]}" --out "$AGREE/predictions/rules-2.jsonl"
"${TM[@]}" train --gold annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl \
  annotations/batches/batch-02.jsonl --out artifacts/crf-batches-01-02 --model-id crf-batches-01-02
"${TM[@]}" predict --model crf --model-dir artifacts/crf-batches-01-02 --sample "${SAMPLES[@]}" \
  --out "$AGREE/predictions/crf-batches-01-02.jsonl"
for model in rules-2 crf-batches-01-02; do
  "${TM[@]}" evaluate annotations/batches/batch-03.jsonl "$AGREE/predictions/$model.jsonl" \
    --add-gold annotations/batches/batch-06.jsonl --split dev \
    --title "Agreement with model drafts: $model" --out "$AGREE/${model}_dev_agreement.md"
done
"${TM[@]}" evaluate annotations/pilot/pilot-2.jsonl "$AGREE/predictions/crf-batches-01-02.jsonl" \
  --split dev --gold-origin manual --title "Hand-labelled dev: crf-batches-01-02" \
  --out "$AGREE/crf-batches-01-02_dev_manual.md"

echo "== drafter consistency and the two-reference batch-07 comparison"
bash scripts/experiments/drafter_consistency.sh
rm reports/batch-07-comparison/predictions/{crf-batches-01-02,rules-2}.jsonl
bash scripts/experiments/batch07_comparison.sh  # the committed DeBERTa predictions are reused

echo "== result"
changed=$(git status --porcelain)
if [ -n "$changed" ]; then
  printf 'NOT REPRODUCED; these files differ from the commit:\n%s\n' "$changed" >&2
  exit 1
fi
echo "REPRODUCED: every regenerated file is byte-identical to commit $(git rev-parse --short HEAD)"
