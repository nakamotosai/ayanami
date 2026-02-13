#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
PROMPT=${1:-}
CHAT_ID=${2:-8138445887}

if [[ -z "$PROMPT" ]]; then
  echo "usage: $0 \"prompt\" [chat_id]" >&2
  exit 2
fi

JOBDIR="$WS/logs/codex/jobs"
mkdir -p "$JOBDIR"
TS=$(date -u +%Y%m%d-%H%M%S)
JOB_ID="codex-$TS"
JOB_JSON="$JOBDIR/$JOB_ID.json"
LOG="$JOBDIR/$JOB_ID.log"
RUNNER="$JOBDIR/$JOB_ID.sh"

# Persist a minimal job descriptor.
python3 - <<PY
import json, time
from pathlib import Path
p = Path("$JOB_JSON")
obj = {
  "jobId": "$JOB_ID",
  "createdAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
  "status": "running",
  "chatId": "$CHAT_ID",
}
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf "WS=%q\n" "$WS"
  printf "PROMPT=%q\n" "$PROMPT"
  printf "CHAT_ID=%q\n" "$CHAT_ID"
  printf "JOB_JSON=%q\n" "$JOB_JSON"
  printf "JOB_ID=%q\n" "$JOB_ID"
  cat <<RUN

WRAP_OUT=$(bash "$WS/scripts/codex_run.sh" "$PROMPT" || true)
LAST=$(printf "%s\n" "$WRAP_OUT" | rg -o "last_msg=\S+" | sed "s/^last_msg=//" | tail -n 1)

python3 - <<PY
import json, time
from pathlib import Path
job = Path("$JOB_JSON")
obj = json.loads(job.read_text(encoding="utf-8"))
obj["status"] = "done"
obj["finishedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
obj["lastMsg"] = LAST
job.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

# Preferred: wake gateway so heartbeat can pick it up.
bash "$WS/scripts/gateway_wake.sh" "codex_job_done" || true

# Fallback: push directly to Telegram.
if [[ -n "$CHAT_ID" && -n "$LAST" && -f "$LAST" ]]; then
  SUM=$(head -c 3500 "$LAST")
  bash "$WS/scripts/telegram_send.sh" "$CHAT_ID" "[Codex 完成] $JOB_ID\n\n$SUM\n\n(文件: $LAST)" || true
fi
RUN
} > "$RUNNER"

chmod +x "$RUNNER"
nohup bash "$RUNNER" >"$LOG" 2>&1 &

echo "OK_DISPATCH: job_id=$JOB_ID job=$JOB_JSON log=$LOG"
