#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=请设计一套完整的\ IQOS/电子烟戒烟方案，适用于一天2包到1包的重度使用者。方案包括：1\)\ 目标设定、心理准备；2\)\ 减量/冷断的决策依据与具体执行步骤；3\)\ 替代支持（尼古丁替代、行为、健康）；4\)\ 复发防范、压力管理、回顾机制；5\)\ 记录、监督与指标（比如每日习惯、触发事件、体验记录、回撤检查）。要求中文，分阶段可复制，带具体时间表和可检查的成功标准，不涉及医疗诊断或处方。
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260215-045557.json
JOB_ID=codex-20260215-045557
LATEST=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/latest.json

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
