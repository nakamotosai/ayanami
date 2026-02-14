#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
PROMPT=${1:-}
CHAT_ID=${2-__unset__}
if [[ "$CHAT_ID" == "__unset__" ]]; then CHAT_ID=8138445887; fi

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
LATEST="$JOBDIR/latest.json"

# Artifact channel: job descriptor.
JOB_JSON="$JOB_JSON" JOB_ID="$JOB_ID" CHAT_ID="$CHAT_ID" LATEST="$LATEST" python3 - <<'PY'
import json, os, time
from pathlib import Path

p = Path(os.environ["JOB_JSON"])
obj = {
  "jobId": os.environ["JOB_ID"],
  "createdAtUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
  "status": "running",
  "chatId": os.environ.get("CHAT_ID", ""),
  "notified": False,
}
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
Path(os.environ["LATEST"]).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

# Runner (signal channel): wake + notifier. No substitutions during generation.
{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf "WS=%q\n" "$WS"
  printf "PROMPT=%q\n" "$PROMPT"
  printf "JOB_JSON=%q\n" "$JOB_JSON"
  printf "JOB_ID=%q\n" "$JOB_ID"
  printf "LATEST=%q\n" "$LATEST"
  cat <<'RUN'

WRAP_OUT=$(CODEX_TIMEOUT="${CODEX_TIMEOUT:-300}" bash "$WS/scripts/codex_run.sh" "$PROMPT" || true)
LAST=$( (printf "%s\n" "$WRAP_OUT" | rg -o "last_msg=\S+" | sed "s/^last_msg=//" | tail -n 1) || true )

LAST="$LAST" python3 - <<'PY'
import json, os, time
from pathlib import Path

job = Path(os.environ["JOB_JSON"])
obj = json.loads(job.read_text(encoding="utf-8"))
obj["lastMsg"] = os.environ.get("LAST", "")
last = Path(obj["lastMsg"]) if obj["lastMsg"] else None
if last and last.exists() and last.stat().st_size > 0:
    obj["status"] = "done"
    obj["finishedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
else:
    obj["status"] = "failed"
    obj["failedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    obj["failReason"] = "missing_last_msg_artifact"
job.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
Path(os.environ["LATEST"]).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

if [[ -n "$LAST" && -f "$LAST" ]]; then
  bash "$WS/scripts/gateway_wake.sh" "codex_job_done" || true
  bash "$WS/scripts/codex_job_notifier.sh" || true
fi
RUN
} > "$RUNNER"

chmod +x "$RUNNER"

nohup env JOB_JSON="$JOB_JSON" JOB_ID="$JOB_ID" LATEST="$LATEST" CODEX_TIMEOUT="${CODEX_TIMEOUT:-300}" bash "$RUNNER" >"$LOG" 2>&1 &
PID=$!
JOB_JSON="$JOB_JSON" PID="$PID" python3 - <<'PY'
import json, os
from pathlib import Path
p=Path(os.environ["JOB_JSON"])
obj=json.loads(p.read_text(encoding="utf-8"))
obj["runnerPid"]=int(os.environ.get("PID","0") or 0)
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

echo "OK_DISPATCH: job_id=$JOB_ID job=$JOB_JSON log=$LOG"
