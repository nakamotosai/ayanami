#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=用中文回答：1+1等于几？（不要运行任何命令，不要读取文件）
CHAT_ID=8138445887
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260214-131035.json

WRAP_OUT=$(bash "$WS/scripts/codex_run.sh" "$PROMPT" || true)
LAST=$(printf "%s\n" "$WRAP_OUT" | rg -o "last_msg=\S+" | sed "s/^last_msg=//" | tail -n 1)

# Persist completion state (no polling / no chat blocking)
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

# Wake gateway (best effort) + run notifier to deliver once.
bash "$WS/scripts/gateway_wake.sh" "codex_job_done" || true
bash "$WS/scripts/codex_job_notifier.sh" || true
