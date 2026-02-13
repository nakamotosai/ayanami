# HEARTBEAT.md

目标：提高主动性，但不打扰。

## 每次 heartbeat（只做 1-3 项，没新东西就回 HEARTBEAT_OK）
1. 记忆索引：如有新增 `workspace/memory/*.md`，运行 `qmd update`。
2. TODO：用 MCP tasks 查看 `todos.md`，必要时补 1 条真正重要的下一步。
   - `cd ~/.openclaw/workspace && mcporter call tasks.list_todos --output text`
3. Telegram 主渠道：只在有明确事件/待办时才发消息；否则保持安静。

## 什么时候可以主动联系用户
- 发现高风险操作需要确认
- 有新的“可立即执行”的方案/修复
- 用户明确要求的定时/监控出现异常

## 什么时候保持沉默
- 没有新信息/没新增待办/没有需要确认的风险
