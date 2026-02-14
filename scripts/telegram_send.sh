#!/usr/bin/env bash
set -euo pipefail

CHAT_ID=${1:-}
TEXT=${2:-}

if [[ -z "$CHAT_ID" || -z "$TEXT" ]]; then
  echo "usage: $0 <chat_id> <text>" >&2
  exit 2
fi

BOT_TOKEN=$(python3 - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path.home().joinpath('.openclaw','openclaw.json').read_text(encoding='utf-8'))
print(cfg.get('channels', {}).get('telegram', {}).get('botToken', ''))
PY
)

if [[ -z "$BOT_TOKEN" ]]; then
  echo "ERROR: missing telegram botToken in openclaw.json" >&2
  exit 1
fi

# Telegram limit is 4096 chars. Truncate by characters (not bytes) to keep UTF-8 valid.
PAYLOAD=$(python3 -c 'import sys; print(sys.argv[1][:3800])' "$TEXT")

RESP=$(LC_ALL=C.UTF-8 LANG=C.UTF-8 curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${PAYLOAD}" \
  -d "disable_web_page_preview=true")

python3 - "$RESP" <<'PY'
import json, sys
try:
    obj = json.loads(sys.argv[1])
except Exception:
    print('ERROR: telegram response not json', file=sys.stderr)
    raise SystemExit(1)
if not obj.get('ok'):
    print('ERROR: telegram send failed: ' + str(obj.get('description','unknown')), file=sys.stderr)
    raise SystemExit(1)
PY
