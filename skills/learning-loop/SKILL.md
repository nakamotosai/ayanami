# learning-loop（强力学习模式）

目标：对一个话题做多轮循环学习（检索->抓取->沉淀->自测->补洞），直到输出一份完整中文长报告，并自动回传到 Telegram。

依赖：
- MCP: `searxng`, `fetch`, `qmd`（通过 `mcporter`）
- 后台执行：`scripts/codex_dispatch.sh` + `scripts/codex_job_notifier.sh`
- Telegram：`scripts/telegram_send.sh`（必要时会分段发送）

入口：
- 开始/继续：`bash scripts/learn_start.sh "topic"`
- 停止：`bash scripts/learn_stop.sh "topic"`
- 单轮（通常不手动用）：`bash scripts/learn_round.sh "topic"`
- 定稿：`bash scripts/learn_publish.sh "topic"`

输出目录：`~/.openclaw/workspace/memory/learn/<topic_slug>/`
- `state.json`：轮次、状态
- `questions.md`：未解问题清单
- `kb.md`：知识库（持续增长）
- `sources.md`：来源索引
- `report.md`：最终完整报告（很长，不精简）
- `stop.flag`：停止信号

说明：
- 默认每轮抓取规模很克制，防止慢与成本爆炸。你可以用环境变量调大：
  - `LEARN_ROUNDS_PER_START`（默认 1）
  - `LEARN_SEARX_LIMIT`（默认 6）
  - `LEARN_MAX_URLS`（默认 4）
  - `LEARN_MAX_CHARS`（默认 12000）
