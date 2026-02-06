#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
SESSION_WATCH="$MEMORY_DIR/session-watch.json"
HOOK_STATE_FILE="$MEMORY_DIR/.hook-last-session"
SLEEP_SECONDS=4
OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"

mkdir -p "$MEMORY_DIR"

read_session_id() {
  SESSION_WATCH_PATH="$SESSION_WATCH" OPENCLAW_CLI="$OPENCLAW_CLI" python3 <<'PY'
import json
import os
import pathlib
import subprocess
import sys
import time
path = pathlib.Path(os.environ["SESSION_WATCH_PATH"])
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
session_id = str(latest.get("sessionId", ""))
if not session_id:
    sys.exit(0)
data = {"lastSessionId": session_id, "updatedAt": int(time.time())}
path.write_text(json.dumps(data))
print(session_id)
PY
}

send_voice_greeting() {
  local script_path="/home/ubuntu/.openclaw/workspace/scripts/chii-edge-voice-note.sh"
  local text="叽～主人，新会话来了，ちぃ用轻柔的声音问候您：今天想先做哪件事呢？"
  if [[ -x "$script_path" ]]; then
    if ! bash "$script_path" "$text"; then
      >&2 echo "[session-memory-hook] warning: voice greeting failed"
    fi
  else
    >&2 echo "[session-memory-hook] warning: voice note script missing: $script_path"
  fi
}

ensure_daily_log() {
  local session_id="$1"
  local today
  today=$(date -u +'%Y-%m-%d')
  local daily_file="$MEMORY_DIR/$today.md"
  local timestamp
  timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
  local entry="- [${timestamp}] Hook captured new session ${session_id} (preserving memory)."

  DATE_FILE="$daily_file" ENTRY="$entry" TIMESTAMP="$timestamp" python3 <<'PY'
from pathlib import Path
import os
import sys
file_path = Path(os.environ["DATE_FILE"])
entry = os.environ["ENTRY"]
if file_path.exists():
    text = file_path.read_text().rstrip()
    if entry in text:
        sys.exit(0)
    text = text + "\n" + entry + "\n"
else:
    text = f"# 今日记忆 {os.environ['TIMESTAMP']}\n{entry}\n"
file_path.write_text(text if text.endswith("\n") else text + "\n")
PY
}

ensure_todo_entry() {
  local session_id="$1"
  local todo_file="$MEMORY_DIR/todos.md"
  local entry="- [ ] Hooked session ${session_id} (pending your manual summary)."

  TODO_FILE="$todo_file" ENTRY="$entry" python3 <<'PY'
from pathlib import Path
import os
path = Path(os.environ["TODO_FILE"])
entry = os.environ["ENTRY"]
text = path.read_text()
if entry in text:
    sys.exit(0)
marker = "## 🔥 Active"
if marker not in text:
    new_text = text.rstrip() + "\n\n" + marker + "\n" + entry + "\n"
else:
    start = text.index(marker) + len(marker)
    tail = text[start:]
    next_section_offset = tail.find("\n## ")
    insert_at = len(text) if next_section_offset == -1 else start + next_section_offset
    before = text[:insert_at].rstrip()
    after = text[insert_at:].lstrip()
    separator = "\n" if before and not before.endswith("\n") else ""
    new_text = before + separator + "\n" + entry + "\n\n" + after
path.write_text(new_text if new_text.endswith("\n") else new_text + "\n")
PY
}

last_seen_session=""
if [[ -f "$HOOK_STATE_FILE" ]]; then
  last_seen_session=$(<"$HOOK_STATE_FILE")
fi

while true; do
  session_id=$(read_session_id)
  if [[ -n "$session_id" && "$session_id" != "$last_seen_session" ]]; then
    ensure_daily_log "$session_id"
    ensure_todo_entry "$session_id"
    send_voice_greeting
    printf "%s" "$session_id" > "$HOOK_STATE_FILE"
    last_seen_session="$session_id"
  fi
  sleep "$SLEEP_SECONDS"
done
