# TOOLS.md

## 三个最基本能力（Casper 必须会用）

### 1) 调用 VPS 上的 Codex CLI（本机执行）
- 后台（推荐，避免卡住 Telegram）：`CODEX_TIMEOUT=300 bash scripts/codex_dispatch.sh "任务" 8138445887`
  - 结果会自动回传；也可手动跑：`bash scripts/codex_job_notifier.sh`
- 检查：`codex --version`
- 用途：需要在 VPS 上直接跑命令、脚本、代码改动时。
- 原则：先只读检查（例如 `ls`/`rg`/`cat`），再做写入；不可逆操作先确认。

### 2) 调用 Skills（技能=可复用工作流）
- 位置：`~/.openclaw/workspace/skills/<skill-name>/SKILL.md`
- 用法：先读 `SKILL.md`；优先运行技能自带脚本；不要手打一长串命令。

### 3) 调用 MCP（通过 mcporter）
- 检查：`mcporter --version`
- 配置：在 workspace 根目录执行 `mcporter list` 会读取 `./config/mcporter.json`
- 常用：
  - `cd ~/.openclaw/workspace && mcporter list`
  - `cd ~/.openclaw/workspace && mcporter list <server> --schema`
  - `cd ~/.openclaw/workspace && mcporter call <server.tool> key=value ...`
- 原则：需要外部工具/检索/集成时优先走 MCP；结果要可复核（保留关键命令与输出要点）。

## 工具使用原则（通用）
1. 先用最快路径拿结果：优先读取本地配置/记忆，再调用外部工具。
2. 查询类任务先检索已有索引/知识库，再做联网搜索。
3. 命令输出过大时改用精确查询，避免重跑重命令。
4. 汇报只保留关键证据：文件路径、关键命令、结论。

## 输出模板（建议）
- 结论：一句话说明结果。
- 已执行：列出做了什么。
- 证据：文件路径/命令关键结果。
- 风险或待确认：只列必要项。

## 搜索与记忆查找（已接通）

### 本地搜索：SearXNG
- 地址：`http://127.0.0.1:8081`
- 示例：`curl -fsS "http://127.0.0.1:8081/search?q=openclaw&format=json"`

### 记忆查找：QMD（collection: memory）
- QMD 完全在本地运行，不需要外部 API key，直接操作 qmd search/query 即可；如果遇到认证错误，多半是由于初始配置未同步。
- 示例：`qmd search "关键词" -c memory -n 10 --json`
- 示例：`qmd query "我之前对X的偏好是什么" -c memory -n 10 --json`

## MCP（mcporter）已接通：SearXNG + QMD

- 列工具：`cd ~/.openclaw/workspace && mcporter list --schema`

### MCP 搜索（SearXNG）
- 调用：`cd ~/.openclaw/workspace && mcporter call searxng.searxng_search query="关键词" limit=5 --output json`

### MCP 记忆查找（QMD）
- 调用：`cd ~/.openclaw/workspace && mcporter call qmd.search query="关键词" collection="memory" limit=10 --output json`
- 高质量查询：`cd ~/.openclaw/workspace && mcporter call qmd.query query="问题" collection="memory" limit=10 --output json`

## 常用 Skills（已安装）
- memory-lite：`skills/memory-lite`（写 daily、搜索、update）
- core-file-maintenance：`skills/core-file-maintenance`（核心文件检查/差异摘要）
- openclaw-backup：`skills/openclaw-backup`（safe/full 备份包）
- telegram-setup：`skills/telegram-setup`（渠道检查/排障）

## 常用 MCP（已接入 mcporter）
- searxng：`searxng.searxng_search`（本地搜索）
- qmd：`qmd.search` / `qmd.query` / `qmd.get`（记忆查找）
- fetch：`fetch.fetch_url`（抓网页原始文本）
- tasks：`tasks.add_todo` / `tasks.list_todos`（本地 todos）
- github：`github.list_issues`（需要 `GITHUB_TOKEN`）

### 快速例子
- 搜索：`cd ~/.openclaw/workspace && mcporter call searxng.searxng_search query="openclaw" limit=5 --output json`
- 记忆：`cd ~/.openclaw/workspace && mcporter call qmd.query query="我的偏好" collection="memory" limit=10 --output json`
- 抓取：`cd ~/.openclaw/workspace && mcporter call fetch.fetch_url url=https://example.com maxChars=2000 --output text`
- TODO：`cd ~/.openclaw/workspace && mcporter call tasks.add_todo text="xxx" --output text`

## ClawHub（官方 skill registry）
- CLI：`clawhub -V`
- 搜索：`cd ~/.openclaw/workspace && clawhub search "关键词" --limit 10`
- 浏览：`cd ~/.openclaw/workspace && clawhub explore --limit 20`
- 安装：`cd ~/.openclaw/workspace && clawhub install <slug>`
- 更新：`cd ~/.openclaw/workspace && clawhub update`
- 已装列表：`cd ~/.openclaw/workspace && clawhub list`

注意：部分 skills 会被 VirusTotal Code Insight 标记为 suspicious，非交互安装会被拦截。
处理方式：先 `clawhub inspect <slug>` 审核代码，再决定是否 `clawhub install <slug> --force`。

## RSS（已安装 skill）
- rssaurus：`skills/rssaurus`（RSS 读取与摘要）

## ClawHub 安装的常用 skills（已安装）
- telegram：`skills/telegram`
- tg-history：`skills/tg-history`
- telegram-pairing-approver：`skills/telegram-pairing-approver`（包含脚本，使用前先读 SKILL.md）
- openclaw-github-assistant：`skills/openclaw-github-assistant`（需要 `GITHUB_TOKEN`）
- rssaurus：`skills/rssaurus`
- rss-digest：`skills/rss-digest`
- rss-ai-reader：`skills/rss-ai-reader`（需要额外 API key 与 Telegram bot token 等配置）

## VPS 运维必备 skills（已安装）
- docker-compose：`skills/docker-compose`
- container-debug：`skills/container-debug`
- docker-diag：`skills/docker-diag`
- cron-dashboard：`skills/cron-dashboard`
- system-monitor：`skills/system-monitor`
- security-sentinel：`skills/security-sentinel`
- security-sentinel（ClawHub）：`skills/security-sentinel`（扫描暴露 secrets）
- security-sentinel（ClawHub 已装的是 security-sentinel 目录名：`skills/security-sentinel`）
- security-sentinel 运行：`node skills/security-sentinel/scan.js`
- security-sentinel：使用前先确认扫描范围
- security-sentinel：只在本机，不外传
- security-sentinel：发现敏感就先停止扩散
- security-sentinel：不自动上传
- git-summary：`skills/git-summary`
- git-sync：`skills/git-sync`
- gh：`skills/gh`
- webhook：`skills/webhook`

## 记忆统一入口（推荐）
- 强化记忆：`skills/enhanced-memory`
  - daily 写入：`bash skills/enhanced-memory/scripts/add_daily.sh "..."`
  - 长期写入：`bash skills/enhanced-memory/scripts/add_long.sh "..."`
  - 检索：`bash skills/enhanced-memory/scripts/search.sh "..."`
  - 提炼：在 daily 标记 `[LT]` 后 `bash skills/enhanced-memory/scripts/promote_lt.sh YYYY-MM-DD`
  - 维护：`bash skills/enhanced-memory/scripts/maintain.sh`

## Telegram 私聊记忆自动化（推荐）
- `skills/telegram-memory-autostore`
- 每次 heartbeat 会自动运行：
  - `python3 ~/.openclaw/workspace/skills/telegram-memory-autostore/scripts/capture_and_store.py`
- 手动触发也可直接跑同一条命令。

## 搜索套件（推荐）
- `skills/search-suite`
  - 简易搜索：`bash skills/search-suite/scripts/fast_search.sh "query"`
  - 强力搜索：`bash skills/search-suite/scripts/deep_search.sh "topic" "q1" "q2" "q3"`
  - 输出：`memory/research/`

## learning-loop（强力学习模式）
- 开始/继续：`bash skills/learning-loop/scripts/learn_start.sh "topic"`
- 定稿：`bash skills/learning-loop/scripts/learn_publish.sh "topic"`
- 停止：`bash skills/learning-loop/scripts/learn_stop.sh "topic"`

## MAGI 三分身（决策）
- 强制统一入口：`bash scripts/magi_vote.sh "<决策包>"`
- 成功标志：输出包含 `MAGI_VOTE_OK` 和 `agents_called=3`
- 结果文件：`logs/magi/latest.md`、`logs/magi/latest.json`
- 若 `agents_called != 3`：视为调度失败，不允许输出“已完成投票”结论。
