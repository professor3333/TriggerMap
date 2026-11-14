#!/usr/bin/env bash
# Consistency between two model drafting runs of the same batch-07 dev documents.
#
#   bash scripts/experiments/drafter_consistency.sh
#
# Draft 1 is annotations/batches/batch-07.jsonl (Label Studio project 7,
# model-batch-07-guidelines-0.2). Draft 2 is annotations/second-drafts/batch-07.jsonl (project 9,
# model-project9-guidelines-0.2). Both are model_draft_accepted under guidelines v0.2. Draft 2
# is turned into Extraction records and scored with draft 1 as the reference. Typed and span F1
# are symmetric, so the direction only swaps precision and recall. This is consistency between
# two model drafting runs: not accuracy and not inter-annotator agreement. Dev only; nothing is
# fitted, and the test split is not touched.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }

DRAFT1=annotations/batches/batch-07.jsonl
DRAFT2=annotations/second-drafts/batch-07.jsonl
OUT=reports/drafter-consistency
PRED="$OUT/predictions/batch-07-draft-2.jsonl"
mkdir -p "$OUT/predictions"

uv run --no-sync python -I - "$DRAFT2" "$PRED" <<'EOF'
import sys
from pathlib import Path

from triggermap.schema import AdvisoryAnnotation, Extraction

lines = []
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    record = AdvisoryAnnotation.model_validate_json(line)
    assert record.origin_model, f"{record.advisory_id}: no origin_model"
    extraction = Extraction(
        advisory_id=record.advisory_id,
        content_hash=record.content_hash,
        preprocessing_version=record.preprocessing_version,
        model_id=record.origin_model,
        document_status=record.document_status,
        conditions=tuple(c.model_copy(update={"source": "model"}) for c in record.conditions),
        groups=record.groups,
    )
    lines.append(extraction.model_dump_json())
Path(sys.argv[2]).write_text("\n".join(lines) + "\n", encoding="utf-8")
EOF

uv run --no-sync triggermap evaluate "$DRAFT1" "$PRED" --split dev --clusters project \
  --title "batch-07: draft 2 (project 9) scored against draft 1 (project 7)" \
  --out "$OUT/batch-07.md"
