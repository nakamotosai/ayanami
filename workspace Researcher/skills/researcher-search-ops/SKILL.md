---
name: researcher-search-ops
description: 深度检索执行规范。用于实时新闻、技术调研、复杂问题拆解；优先 SearXNG，失败回退 Codex，输出含完整来源链接。
---

# Researcher Search Ops

## Trigger
当任务涉及：搜索、调研、新闻、最新动态、多来源对比、技术深挖。

## Workflow
1. 先用 `bash scripts/research_dispatch.sh "query"`。
2. 若结果不足或问题复杂，执行 `bash scripts/codex_deep_search.sh "query"`。
3. 输出必须包含：结论摘要、关键发现、证据链接、不确定项、下一步建议。

## Non-negotiables
- 不向用户索要 Telegram 用户 ID。
- 不能省略来源链接。
- 时间敏感结论必须带绝对日期。
