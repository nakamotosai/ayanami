# Daily Upgrade Proposal (2026-02-13T17:03:48Z)

最多 3 条。每条包含：改动点 / 风险 / 验收。

## 1) 默认检索走 qmd search（避免模型下载导致卡死）

- 改动：保持 `skills/enhanced-memory/scripts/search.sh` 默认 search 模式

- 风险：低

- 验收：运行 `bash skills/enhanced-memory/scripts/search.sh "关键词"`

## 2) Heartbeat 自检改为轻量 health（减少 gateway timeout）

- 改动：把 `openclaw cron status` 换成 `openclaw status` 或直接跳过

- 风险：低

- 验收：手动触发 heartbeat cron，确认耗时 < 30s

## 3) GitHub sync 强制 GH_TOKEN=GITHUB_TOKEN（避免 session 过期）

- 改动：HEARTBEAT.md 已加固（保持）

- 风险：低

- 验收：制造一次变更，触发 heartbeat，确认 push 成功

