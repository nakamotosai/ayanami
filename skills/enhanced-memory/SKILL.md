# 强化记忆（enhanced-memory）

目标：把所有“记忆写入/查找/提炼/清理”收敛到一个统一入口，避免多个 memory skills 混乱。

依赖：
- `qmd`（用于索引与检索）
- （可选）`mcporter`（通过 MCP 调用 qmd/search）

## 你应该用它的时机
- 用户说“记住/记录/以后别忘/写进记忆/偏好是…”
- 用户问“我之前说过什么/我的偏好是什么/历史怎么配置的”
- daily 太乱，需要提炼到长期 `MEMORY.md`
- 长期记忆出现重复/噪音，需要去重

## 核心约定
- **长期记忆**：`~/.openclaw/workspace/MEMORY.md`
- **日记（daily）**：`~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- 写完任何记忆后都跑 `qmd update`，保证下一轮可检索。

## 常用命令

### 1) 追加一条 daily 记忆
```bash
bash scripts/add_daily.sh "文本"
```

### 2) 追加一条长期记忆（直接写入 MEMORY.md）
```bash
bash scripts/add_long.sh "文本"
```

### 3) 从 daily 提炼到长期记忆（基于标记）
规则：在 daily 里把你想升级为长期的条目标记为 `[LT]`，然后运行：
```bash
bash scripts/promote_lt.sh YYYY-MM-DD
```

### 4) 查记忆（默认查 collection: memory）
```bash
bash scripts/search.sh "关键词"
```

### 5) 维护（索引更新 + 长期记忆去重）
```bash
bash scripts/maintain.sh
```
