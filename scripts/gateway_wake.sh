#!/usr/bin/env bash
set -euo pipefail

# Wake the local gateway so it can pick up completed job artifacts.
# Uses ~/.openclaw/openclaw.json gateway.auth.token.

REASON=${1:-"codex_job_done"}

PORT=$(python3 - <<"PY"
import json
from pathlib import Path
cfg=json.loads(Path.home().joinpath(".openclaw","openclaw.json").read_text(encoding="utf-8"))
print(cfg.get("gateway", {}).get("port", 18789))
PY
)

TOKEN=$(python3 - <<"PY"
import json
from pathlib import Path
cfg=json.loads(Path.home().joinpath(".openclaw","openclaw.json").read_text(encoding="utf-8"))
print(cfg.get("gateway", {}).get("auth", {}).get("token", ""))
PY
)

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: missing gateway auth token" >&2
  exit 1
fi

curl -sS -X POST "http://127.0.0.1:${PORT}/api/cron/wake" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"reason\":\"${REASON}\"}" \
  >/dev/null
