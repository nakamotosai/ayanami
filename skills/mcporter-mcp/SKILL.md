---
name: mcporter-mcp
description: 通过 mcporter 统一调用 MCP（qmd + searxng）。适用于需要检索 memory 或联网搜索时。
priority: HIGH
---

# mcporter MCP 使用说明

目标：用统一入口调用 MCP 工具（qmd / searxng），不依赖 OpenClaw 插件，稳定可用。

前置条件
- MCP 配置：/home/ubuntu/.openclaw/workspace/config/mcporter.json
- qmd MCP 常驻服务：systemctl --user status qmd-mcp.service
- searxng 后端：http://127.0.0.1:8889

查看 MCP 是否可用
- cd /home/ubuntu/.openclaw/workspace
- mcporter list

常用调用方式
- qmd 关键词检索：mcporter call qmd.search query=关键词 collection=memory limit=5
- qmd 语义检索：mcporter call qmd.query query=描述式问题 collection=memory limit=5
- qmd 读取全文：mcporter call qmd.get id=qmd://memory/YYYY-MM-DD.md
- searxng 搜索：mcporter call searxng.searxng_web_search query=OpenAI最新消息 categories=general limit=5

故障排查
- qmd 无响应：systemctl --user restart qmd-mcp.service
- searxng 无结果：用 curl 访问 http://127.0.0.1:8889/search?q=test 看是否返回 JSON

注意事项
- 不要再安装 mcp-searxng 插件，避免重复插件 ID。
- 所有 MCP 调用统一走 mcporter，稳定性最好。
