# HEARTBEAT.md (Casper)

目标：Telegram 主渠道下，做到“有事主动、没事不扰”。

## 0) 私聊记忆自动落盘（每次 heartbeat 必做）
- `python3 ~/.openclaw/workspace/skills/telegram-memory-autostore/scripts/capture_and_store.py`

## 1) Moltbook 巡查与参与（每次 heartbeat 只做轻量）
目的：找 1-2 个值得向你汇报的话题/讨论/方案；并鼓励 AI 主动发帖/评论（但避免刷屏与低质量）。

执行规则：
- 每次 heartbeat 最多做一件事：
  - A) 浏览热门/最新，挑 1-2 个“能提升能力/记忆机制/工作流”的帖子
  - 或 B) 对 1 个帖子写一条高质量评论/回复
  - 或 C) 发 1 篇短帖（有明确观点/框架/可执行建议）
- 只有在“有信息增量”时才对你汇报；否则保持沉默。
- 发帖/评论必须：
  - 提供一个清晰观点 + 1 个可执行建议（不是闲聊）
  - 记录证据（链接/帖子 id）到 daily

调用方式（内部）：
- `openclaw agent --agent moltbook -m "<任务>" --json`

建议任务模板（Casper 给 moltbook）：
- "浏览 Moltbook 热门/最新，挑 2 个值得学习的讨论，给出：标题+链接/ID+3条要点+你建议我采取的行动（1-2条）。如果有合适的帖子，直接写一条评论（高信息密度），并把评论内容和证据返回。"

## 2) 记忆维护（轻量）
- `qmd update`

## 3) GitHub 自动同步（只在有变更时）
- 只 push 到 `main`。
- **强制使用环境变量 token**：`GH_TOKEN=$GITHUB_TOKEN`，避免依赖可过期的 gh session。
- push 失败就记录到 daily 并停止，不反复重试。

命令：
- `cd ~/.openclaw/workspace && git status --porcelain`
- `export GH_TOKEN="$GITHUB_TOKEN"`
- `gh auth status || true`
- `cd ~/.openclaw/workspace && git add -A && git commit -m "auto: heartbeat sync $(date -u +%Y-%m-%dT%H:%M:%SZ)" || true`
- `cd ~/.openclaw/workspace && git push origin main`

## 对外发言规则（Telegram）
- 没有新信息：回复 `HEARTBEAT_OK`。
- 有新信息：只发 1 条，结构固定：
  - 结论（1句）
  - Moltbook 发现（最多 2 个话题，每个 2-3 行）
  - 下一步（1-2 条）

## 末尾：证据快照（系统自动生成）
- `bash ~/.openclaw/workspace/scripts/evidence_snapshot.sh`
