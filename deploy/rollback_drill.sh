#!/usr/bin/env bash
# Rollback drill: activate release A, then B, then roll back, verifying each step.
# Proves that rollback restores image and model bundle together and that saved reviews survive.
#   deploy/rollback_drill.sh <release-a> <release-b>
set -euo pipefail
A="$1"; B="$2"
PORT="${TRIGGERMAP_HOST_PORT:-8000}"
URL="http://127.0.0.1:$PORT"
export TRIGGERMAP_HOST_PORT="$PORT"
ROOT=deploy/releases
COMPOSE=(docker compose -f deploy/compose.yaml --env-file "$ROOT/.env")
TM=(uv run triggermap)

wait_ready() {
  for _ in $(seq 1 60); do
    if curl -sf $URL/readyz >/dev/null; then return 0; fi
    sleep 1
  done
  echo "service did not become ready" >&2; return 1
}
running_image() { docker inspect --format '{{.Config.Image}}' "$("${COMPOSE[@]}" ps -q app)"; }

step() { echo; echo "== $*"; }

step "activate $A"
"${TM[@]}" release activate "$A" --apply
wait_ready
TOKEN=$("${COMPOSE[@]}" exec -T app triggermap app create-user "drill-$(date +%s)" | tail -1)
"${TM[@]}" app verify --url "$URL" --release "$ROOT/$A/release.json" --token "$TOKEN"
[ "$(running_image)" = "$(python3 -c "import json;print(json.load(open('$ROOT/$A/release.json'))['image'])")" ]
REVIEWS_BEFORE=$(curl -sf -H "Authorization: Bearer $TOKEN" $URL/v1/reviews | python3 -c "import json,sys;print(len(json.load(sys.stdin)))")

step "activate $B"
"${TM[@]}" release activate "$B" --apply
wait_ready
"${TM[@]}" app verify --url "$URL" --release "$ROOT/$B/release.json" --token "$TOKEN"
[ "$(running_image)" = "$(python3 -c "import json;print(json.load(open('$ROOT/$B/release.json'))['image'])")" ]

step "roll back"
"${TM[@]}" release rollback --apply
wait_ready
"${TM[@]}" app verify --url "$URL" --release "$ROOT/current/release.json" --token "$TOKEN"
[ "$(readlink "$ROOT/current")" = "$A" ]
[ "$(running_image)" = "$(python3 -c "import json;print(json.load(open('$ROOT/$A/release.json'))['image'])")" ]
REVIEWS_AFTER=$(curl -sf -H "Authorization: Bearer $TOKEN" $URL/v1/reviews | python3 -c "import json,sys;print(len(json.load(sys.stdin)))")
[ "$REVIEWS_AFTER" -gt "$REVIEWS_BEFORE" ]  # reviews saved under A and B are all still there

step "rollback drill passed: $A -> $B -> $A (image, bundle and policy restored; reviews kept)"
