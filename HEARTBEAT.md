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

## 如主人明确说“安静/别打扰”
- 回复 `HEARTBEAT_OK`
