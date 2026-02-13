#!/usr/bin/env bash
set -euo pipefail

CHAT_ID=${1:-}
TEXT=${2:-}

if [[ -z "$CHAT_ID" || -z "$TEXT" ]]; then
  echo "usage: $0 <chat_id> <text>" >&2
  exit 2
fi

BOT_TOKEN=$(python3 - <<PY
import json
from pathlib import Path
cfg = json.loads(Path.home().joinpath(".openclaw","openclaw.json").read_text(encoding="utf-8"))
print(cfg.get("channels", {}).get("telegram", {}).get("botToken", ""))
PY
)

if [[ -z "$BOT_TOKEN" ]]; then
  echo "ERROR: missing telegram botToken in openclaw.json" >&2
  exit 1
fi

# Telegram hard limit is 4096 chars; keep headroom.
PAYLOAD=$(python3 - <<PY
import sys
print(sys.argv[1][:3800])
PY
"$TEXT")

curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${PAYLOAD}" \
  -d "disable_web_page_preview=true" \
  >/dev/null
