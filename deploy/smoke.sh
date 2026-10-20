#!/usr/bin/env bash
# Container smoke test: the image starts, reports ready, and extracts conditions.
#   deploy/smoke.sh <image> [port]
set -euo pipefail
IMAGE="$1"; PORT="${2:-18000}"
NAME="triggermap-smoke-$$"
docker run -d --name "$NAME" --read-only --tmpfs /tmp -e TRIGGERMAP_RELEASE=smoke \
  -e TRIGGERMAP_DATABASE=/tmp/smoke.db -p "127.0.0.1:$PORT:8000" "$IMAGE" >/dev/null
trap 'docker rm -f "$NAME" >/dev/null 2>&1 || true' EXIT
for _ in $(seq 1 60); do
  curl -sf "http://127.0.0.1:$PORT/readyz" >/dev/null && break
  sleep 1
done
curl -sf "http://127.0.0.1:$PORT/readyz" | python3 -c "
import json, sys
ready = json.load(sys.stdin)
assert ready['status'] == 'ready' and ready['release'] == 'smoke', ready
print('ready:', ready['model_id'], 'preprocessing', ready['preprocessing_version'], 'policy', ready['review_policy_version'])"
curl -sf -X POST "http://127.0.0.1:$PORT/v1/extractions" -H 'content-type: application/json' \
  -d '{"text": "When using aiohttp as a web server and enabling static resource resolution with follow_symlinks set to True, files leak."}' \
  | python3 -c "
import json, sys
out = json.load(sys.stdin)
assert len(out['conditions']) == 3 and out['groups'][0]['operator'] == 'ALL', out
print('extraction:', [c['surface'] for c in out['conditions']])"
echo "smoke test passed: $IMAGE"
