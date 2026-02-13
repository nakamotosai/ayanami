# TOOLS.md - Researcher 专员工具手册

## 核心工具

### 1) SearXNG 主搜索（默认）
- 地址：`http://127.0.0.1:8889`
- 命令：
- `python3 scripts/searxng_search.py "关键词" --count 15`
- `bash scripts/research_dispatch.sh "问题描述"`

### 2) Codex 兜底深搜
- 命令：
- `bash scripts/codex_deep_search.sh "复杂问题"`

## 使用规则
- 任何“最新/今天/最近”问题，优先检索后再回答。
- 输出必须保留链接，不要只给摘要。
- 不要要求用户提供 Telegram ID；当前会话即目标。
