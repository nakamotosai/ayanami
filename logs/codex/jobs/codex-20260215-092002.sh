#!/usr/bin/env bash
set -euo pipefail
WS=/home/ubuntu/.openclaw/workspace
PROMPT=$'你在做一个“强力学习模式”的第 118 轮学习。\n话题：polymarket 套利\n\n你只能使用这些本轮抓取到的材料（每个源文件对应一个 URL）：\n- /home/ubuntu/.openclaw/workspace/memory/learn/polymarket_/sources/round-118/src-*.txt 和 /home/ubuntu/.openclaw/workspace/memory/learn/polymarket_/sources/round-118/src-*.url\n\n任务：\n1) 产出“增量沉淀”：把本轮新增/修正的知识点追加写入 /home/ubuntu/.openclaw/workspace/memory/learn/polymarket_/kb.md（用 Markdown，保留足够细节，不要精简）。\n2) 产出“未解问题”：把仍需进一步查证/补洞的问题追加写入 /home/ubuntu/.openclaw/workspace/memory/learn/polymarket_/questions.md（按优先级）。\n3) 每个关键结论末尾必须带来源标注： (Round 118 Source N)\n4) 输出同时包含“套利玩法/交易策略/风控/常见坑/合规与道德边界（提醒风险，不给非法指导）”。\n\n写入规则：\n- 只做追加，不要重写整文件。\n- 尽量去重：如果 kb.md 已经有同义内容，只补充缺失部分。\n- 全部用中文。\n\n最后给我一个本轮摘要（10-20 条要点）用于回传 Telegram。'
JOB_JSON=/home/ubuntu/.openclaw/workspace/logs/codex/jobs/codex-20260215-092002.json
JOB_ID=codex-20260215-092002
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
