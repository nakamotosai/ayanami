#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LAST_CHAT_FILE="$MEMORY_DIR/last_chat.ts"
FORCE_FILE="$MEMORY_DIR/force_heartbeat"
LAST_HB_FILE="$MEMORY_DIR/last_heartbeat.ts"
OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"

refresh_last_chat() {
  if [[ ! -x "$OPENCLAW_CLI" ]]; then
    return 0
  fi
  LAST_CHAT_PATH="$LAST_CHAT_FILE" OPENCLAW_CLI="$OPENCLAW_CLI" python3 <<'PY'
import json
import os
import pathlib
import subprocess
import sys
path = pathlib.Path(os.environ["LAST_CHAT_PATH"])
cli = os.environ["OPENCLAW_CLI"]
cmd = [cli, "sessions", "--json", "--active", "120"]
try:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = proc.stdout
except subprocess.CalledProcessError as exc:
    output = exc.stdout or exc.stderr or ""
if not output:
    sys.exit(0)
start = output.find("{")
if start == -1:
    sys.exit(0)
payload = json.loads(output[start:])
sessions = payload.get("sessions") or []
if not sessions:
    sys.exit(0)
latest = max(sessions, key=lambda s: s.get("updatedAt", 0))
updated_at = int(latest.get("updatedAt", 0) or 0)
if updated_at <= 0:
    sys.exit(0)
# updatedAt is in ms
path.write_text(str(updated_at // 1000))
PY
}

refresh_last_chat

now_ts=$(date +%s)
active=false

if [[ -f "$LAST_CHAT_FILE" ]]; then
  last_ts=$(cat "$LAST_CHAT_FILE" 2>/dev/null || echo 0)
  if [[ $((now_ts - last_ts)) -le 600 ]]; then
    active=true
  fi
fi

if [[ -f "$FORCE_FILE" ]]; then
  active=true
  rm -f "$FORCE_FILE"
fi

# Cooldown: avoid repeated heartbeats within a short window
if [[ -f "$LAST_HB_FILE" ]]; then
  last_hb=$(cat "$LAST_HB_FILE" 2>/dev/null || echo 0)
  if [[ $((now_ts - last_hb)) -le 600 ]]; then
    exit 0
  fi
fi

if [[ "$active" != true ]]; then
  exit 0
fi

# Compact memory on heartbeat
"$WORKSPACE/scripts/memory_compact.sh" >/dev/null 2>&1 || true

"$WORKSPACE/scripts/heartbeat_maintenance.sh" >/dev/null 2>&1 || true
echo "$now_ts" > "$LAST_HB_FILE"