# session_watch 自动化说明（跨 agent）

此脚本会周期性扫描 `~/.openclaw/agents/*/sessions/*.jsonl`，并对所有 agent 新增的用户消息做增量处理：

1. 从上次偏移量继续读取（`memory/session-watch.json` 的 `offsets`）。
2. 提取偏好/规则类句子并追加到 `MEMORY.md`。
3. 把本轮跨 agent 摘要写入 `memory/YYYY-MM-DD.md`。

建议通过 cron 触发，示例（每 5 分钟）：

```
*/5 * * * * cd /home/ubuntu/.openclaw/workspace && ./scripts/session_watch.py
```

脚本幂等：无新增消息时输出 `NO_REPLY`，不会重复写入。
首次看到某个历史 session 会把光标初始化到文件末尾，避免把旧历史一次性灌入主记忆。
