#!/usr/bin/env bash
set -euo pipefail

CHAT_ID=${1:-}
FILE=${2:-}
CAPTION=${3:-}

if [[ -z "$CHAT_ID" || -z "$FILE" ]]; then
  echo "usage: $0 <chat_id> <file_path> [caption]" >&2
  exit 2
fi
[[ -f "$FILE" ]] || { echo "NOT_FOUND: $FILE" >&2; exit 1; }

BOT_TOKEN=$(python3 - <<'PY'
import json
from pathlib import Path
cfg = json.loads(Path.home().joinpath('.openclaw','openclaw.json').read_text(encoding='utf-8'))
print(cfg.get('channels', {}).get('telegram', {}).get('botToken', ''))
PY
)
[[ -n "$BOT_TOKEN" ]] || { echo "ERROR: missing telegram botToken" >&2; exit 1; }

CAPTION=$(python3 -c 'import sys; print((sys.argv[1] if len(sys.argv)>1 else "")[:800])' "${CAPTION:-}")
RESP=$(LC_ALL=C.UTF-8 LANG=C.UTF-8 curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F "chat_id=${CHAT_ID}" \
  -F "document=@${FILE}" \
  -F "disable_content_type_detection=true" \
  -F "caption=${CAPTION}")
python3 - "$RESP" <<'PY'
import json, sys
obj=json.loads(sys.argv[1])
if not obj.get('ok'):
    raise SystemExit('ERROR: telegram sendDocument failed: '+str(obj.get('description','unknown')))
PY
