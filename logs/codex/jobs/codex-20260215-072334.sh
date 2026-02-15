#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=同步修复\ \`skills/news-briefing/scripts/fetch_news.py\`\ 的速度问题：当前\ cron\ 每天拉12个\ feed\ 顺序抓取，常会挂在\ 10\ 分钟\ timeout。请改成用\ ThreadPoolExecutor\ 并发抓取（默认\ concurrency=6，也允许通过命令行\ --concurrency\ 调整），每个抓取仍然用\ urllib.request.urlopen\(...\,\ timeout=20\)\ 但要支持并发。其他逻辑（标题规整、打分、分类、Telegram\ 渲染）保持不变。改完后运行\ python3\ skills/news-briefing/scripts/fetch_news.py\ --top\ 10\ --format\ json\ 以确认至少能顺利返回\ JSON。
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260215-072334.json
JOB_ID=codex-20260215-072334
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
