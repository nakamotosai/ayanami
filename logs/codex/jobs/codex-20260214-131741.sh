#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=用中文回答：1+1等于几？
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260214-131741.json
JOB_ID=codex-20260214-131741

# Execute Codex CLI in the background. CODEX_TIMEOUT is inherited from the parent env.
WRAP_OUT=$(CODEX_TIMEOUT="${CODEX_TIMEOUT:-300}" bash "$WS/scripts/codex_run.sh" "$PROMPT" || true)
LAST=$(printf "%s\n" "$WRAP_OUT" | rg -o "last_msg=\S+" | sed "s/^last_msg=//" | tail -n 1)

# Mark job done (artifact update). Avoid polling in chat thread.
LAST="$LAST" python3 - <<'PY'
import json, os, time
from pathlib import Path

job = Path(os.environ["JOB_JSON"])
obj = json.loads(job.read_text(encoding="utf-8"))
obj["status"] = "done"
obj["finishedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
obj["lastMsg"] = os.environ.get("LAST", "")
job.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

# Best effort: wake gateway; notifier delivers exactly-once via Telegram.
bash "$WS/scripts/gateway_wake.sh" "codex_job_done" || true
bash "$WS/scripts/codex_job_notifier.sh" || true
