#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=按已通过的\ MAGI\ 方案A，执行记忆强化自我升级落地：1\)\ 为三层记忆（session/daily/MEMORY）制定可执行模板与触发条件并更新\ HEARTBEAT.md；2\)\ 新增或更新脚本实现每日轻整理、每周提炼到\ MEMORY.md、去重统计（目标重复率阈值可配置，默认10%）；3\)\ 产出可回滚机制（备份/恢复说明）与\ 7-14\ 天执行计划文档；4\)\ 保持低风险，不做外部发布；5\)\ 输出变更清单、关键文件路径、验证命令与下一步建议。
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260215-045039.json
JOB_ID=codex-20260215-045039
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
