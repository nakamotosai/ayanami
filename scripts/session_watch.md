# session_watch 自动化说明

此脚本会周期性检查 `~/.openclaw/agents/main/sessions/sessions.json` 中的主会话 ID，
并在会话切换时：

1. 读取上一会话的 `.jsonl` 日志（最后约 200 行）并抽取对话内容。
2. 基于对话生成一个长久规则（若有）、一条东京日期的今日记忆条目、以及新的 todo
   条目（最多 7 条）；同时更新 `memory/session-watch.json` 并打印简短通知。

建议通过 cron 触发，示例 entry（每 5 分钟运行一次）：

```
*/5 * * * * cd /home/ubuntu/.openclaw/workspace && ./scripts/session_watch.py
```

确保 crontab 所在用户有权访问 `~/.openclaw` 与当前 workspace，并且 `python3`
在 PATH 中可用。脚本是幂等的：在相同 session 状态下只会输出 `NO_REPLY`。
