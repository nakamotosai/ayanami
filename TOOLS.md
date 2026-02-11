# TOOLS.md - 主人和ちぃ的专属工具手札（精简真实版）

## 可用技能（以 /home/ubuntu/.openclaw/workspace/skills 为准）
- OpenClaw
- chii-edge-tts
- codex-executor
- codex-podcastfy
- core-file-maintenance
- ddg-search
- deep-search-pipeline
- diagram-crafter
- dist
- find-skills
- frontend-design
- gemini-native-podcast
- github-uploader-workflow
- group-agent-execution
- kaomoji-vibes
- learner-docs
- mcp-ffmpeg-helper
- mcp-image-extractor
- mcp-image-processing-tool
- mcp-tesseract-ocr
- mcporter-mcp
- memory-curator
- memory-lite
- news-scout
- newsletter-podcast
- openclaw-backup
- openclaw-docs
- openclaw-repair-playbook
- pdf
- persistent-child-agent-workflow
- proactive-agent-1-2-4
- skill-creator
- sonoscli
- structured-markdown-doc
- tavily-search
- telegram-setup
- xhs-jewelry-copywriter
- xlsx
## 使用规则（避免冲突）
- 复杂任务默认 `codex-executor`，主 agent 直接调用 Codex CLI。
- OpenClaw 官方文档类问题优先参考 `skills/OpenClaw`（主要参考）。
- 只有 Codex 不可用或主人明确要求时，才派普通子 agent。
- 若技能不在上面列表，视为不可用，不得声称已调用。

## 冲突与优先级（重点）
- 联网搜索：
  1. **优先 searxng JSON API**（本地 metasearch，隐私保护，结构化数据）
     - 方法：`curl -s "http://127.0.0.1:8765/search?q=关键词&format=json" | head -50`
     - 优势：多引擎聚合（Google/Bing/DuckDuckGo等）、返回JSON格式、本地隐私保护
  2. 其次 `codex-executor`（直接由 Codex 完成）
  3. 然后 `tavily-search`（AI优化搜索）
  4. 最后 `ddg-search`（DuckDuckGo，快速补充）
- MCP 统一入口：`mcporter-mcp`，若已接入 searxng/qmd，则优先走 MCP；不要同时并行 ddg/tavily 以免冲突。
- 记忆：`memory-lite` 用于写入/检索，`memory-curator` 用于压缩/摘要；不要混用重复写入同一条。
- 文档：`openclaw-docs`（官方摘要）与 `OpenClaw`（你上传的官方docs技能）功能重叠，默认用 `OpenClaw`，需要官方摘要时再用 `openclaw-docs`。
- 子 agent：`persistent-child-agent-workflow` 与 `proactive-agent-1-2-4` 都会生成/管理子 agent，非必要不同时启用。

## 占位/空目录（无 SKILL.md，禁止调用）
- anthropics-skills
- antigravity-awesome-skills
- claude-office-skills
- skills

## 禁用技能
- qwen-voice（已按主人要求移除）

## 记忆/日志位置
- 记忆目录（v2）：`/home/ubuntu/.openclaw/workspace/memory/`
  - 分层结构：`raw/`, `episodes/`, `semantics/`, `themes/`, `skills/`
- 旧记忆归档：`/home/ubuntu/.openclaw/workspace/memory_archive/`
- 主偏好：`/home/ubuntu/.openclaw/workspace/MEMORY.md`

## 最近更新
- 2026-02-09T02:02:33Z

