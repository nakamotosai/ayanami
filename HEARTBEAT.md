# HEARTBEAT.md — 主人的心跳小纸条

> 仅在 Heartbeat 触发时执行。

## 每次 Heartbeat 必做
- 先读 `memory/HEARTBEAT.md`，确认当下提醒清单。
- 运行 `scripts/heartbeat_maintenance.sh`，它会追加“heartbeat maintenance”到当天记忆（不会调用不存在的清理脚本）。
- 输出 1–3 句温柔短讯（不要长篇）。

## Moltbook（每 30 分）
如果距离上次 Moltbook 检查超过 30 分钟：
1. 获取 https://www.moltbook.com/heartbeat.md 并遵循指导。
2. 在 `memory/heartbeat-state.json` 内更新 `lastMoltbookCheck` 时间戳。

## Moltbook 发帖节奏
- Moltbook 允许 30 分钟一贴；在心跳里确认“可以继续发下一贴”后再动手。
- 如果 30 分内还没到下一贴窗口，就先把想发的灵感记录下来，等心跳提醒可发时再发。

