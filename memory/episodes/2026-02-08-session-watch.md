# session_watch 自动记忆整理流程

## Goal
- 从存档提炼该主题的关键信息

## Context
- 来源：
- /home/ubuntu/.openclaw/workspace/memory_archive/20260209T020218Z/2026-02-08.md

## Progress
- 目前只做首次归档摘要

## Decision
- 由新记忆体系接管后续更新

## Evidence (from archive)
- - [2026-02-08T00:45:01Z] Decision: Evidence: 1) `scripts/session_watch.md` 说明建议每 5 分钟由 cron 启动 `./scripts/session_watch.py`，脚本本身说明了 `NO_REPLY` 的幂等性； 2) `scripts/session_watch.py` 实现了你描述的所有步骤，包括 `last`/`current` 比对、tail 旧会话、提炼规则/决定/风险/任务并写入三份记忆、更新 todo 与 watch 文件、回报"我已在后台整理并进化记忆 + 更新 todo"； 3)…
- - [2026-02-08T00:45:01Z] Risk/Pitfall: Evidence: 1) `scripts/session_watch.md` 说明建议每 5 分钟由 cron 启动 `./scripts/session_watch.py`，脚本本身说明了 `NO_REPLY` 的幂等性； 2) `scripts/session_watch.py` 实现了你描述的所有步骤，包括 `last`/`current` 比对、tail 旧会话、提炼规则/决定/风险/任务并写入三份记忆、更新 todo 与 watch 文件、回报"我已在后台整理并进化记忆 + 更新 todo"； 3)…
- - [2026-02-08T00:45:01Z] Open todo: 🧩 下一步：保持 cron 每两分钟运行脚本，一旦 /new 或 /reset 触发会自动摘录历史会话并更新 MEMORY/记忆日志/todos；我也会在那时再向主人报告新的整理结果；System: [2026-02-07 23:48:28 GMT+9] Cron: 结论：`scripts/session_watch.py` 已经按要求实现"/new 或 /reset 后自动进化记忆"逻辑-它读取 `~/.openclaw/agents/main/sessions/sessions.json` 的 `agent:main:main.sessionId`，对比 `memor…；证据：脚本本身的流程与写入逻辑直接对应需求（已同步到 TODOs）
- - 1. System: [2026-02-08 00:15:10 GMT+9] Cron: ⚠️ 📖 Read: `~/.openclaw/workspace/config/cron/jobs.json` failed: ENOENT: no such file or directory, access '/home/ubuntu/.openclaw/workspace/config/cron/jobs.json'
- System: [2026-02-08 00:16:41 GMT+9] Cron: 🔹 结论：`scripts/session_watch.py` 已按照你描述的流程实现了"/new 或 /reset → sessionId 变化 → 自动整理记忆/待办"的 hook：它会检测 `~/.openclaw/agents/main/sessions/sessions.json` 的主会话 ID、比对 `memory/session-watch.json` 的 `lastSessionId`、在需要时抓取旧 `.jsonl` 的尾 200 行、按反幻觉 1/2/4/6 规则写入 `MEMORY.md`、对应日期的 `memory/YYYY-MM-DD.md` 以及 `memory/todos.md`，并把 `session-watch.json` 更新为当前 ID，最后输出"我已在后台整理并进化记忆 + 更新 todo"。
- 🔹 细节：`memory/session-watch.json` 目前记录 `f89004de-17e0-467d-95d2-65e20400f570`，因此还没触发写入；只要按 crontab（例如 `*/5 * * * * cd /home/ubuntu/.openclaw/workspace && ./scripts/session_watch.py`）定期跑，新的 /new 或 /reset 触发后脚本会自动回写三份记忆并更新 TODOs，保持一致性。
