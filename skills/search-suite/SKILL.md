# search-suite（搜索套件）

提供两种搜索：
- 简易搜索：快、低成本、只拿结果列表
- 强力搜索：多轮搜索 + 抓正文 + 引用式总结

依赖：
- MCP: `searxng`, `fetch`, `qmd`（通过 `mcporter`）
- 本地文件：输出到 `workspace/memory/research/`

入口：
- 简易：`bash scripts/fast_search.sh "query"`
- 强力：`bash scripts/deep_search.sh "topic" "q1" "q2" "q3"`

## 异步强力搜索
- 适用：Telegram 里不想卡住对话，先立即确认开始，后台跑完自动私聊推送摘要。
- 用法：`bash scripts/deep_search_async.sh "topic"`
- 默认规模（可通过环境变量下调/上调）：
  - `DEEP_SEARCH_SEARX_LIMIT`（默认 6）
  - `DEEP_SEARCH_MAX_URLS`（默认 4）
  - `DEEP_SEARCH_MAX_CHARS`（默认 8000）
  - `DEEP_SEARCH_CODEX_TIMEOUT`（默认 420 秒）
