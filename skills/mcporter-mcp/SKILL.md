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
- **searxng JSON API 推荐**：
  ```bash
  curl -s "http://127.0.0.1:8765/search?q=关键词&format=json" | head -50
  ```
  优势：多引擎聚合、返回JSON结构化数据、本地隐私保护、速度快

备用 searxng MCP 调用
- mcporter call searxng.searxng_web_search query=OpenAI最新消息 categories=general limit=5

故障排查
- qmd 无响应：systemctl --user restart qmd-mcp.service
- searxng 无结果：用 curl 访问 http://127.0.0.1:8889/search?q=test 看是否返回 JSON

注意事项
- 不要再安装 mcp-searxng 插件，避免重复插件 ID。
- 所有 MCP 调用统一走 mcporter，稳定性最好。

## 📝 新闻输出标准格式
使用 searxng JSON API 搜索新闻时，必须严格遵循以下格式规范：

### 格式要求：
1. **标题格式**：`### N. **新闻标题**`
2. **内容格式**：使用 `- **类型**：内容` 格式，不带空行
3. **条目间空行**：只在每条新闻之间保留一个空行
4. **整体结构**：标题 + 无空行内容 + 一个空行 + 下一条

### 标准模板：
```
### 1. **新闻标题**
- **详情**：具体内容描述
- **影响**：相关影响分析
- **来源**：新闻来源平台
- **时间**：发布时间

### 2. **下一条新闻标题**
- **详情**：具体内容描述
- **影响**：相关影响分析
- **来源**：新闻来源平台
- **时间**：发布时间
```

### 禁止：
- 标题和内容之间的空行
- 同一条新闻内的多余空行
- 条目间的多余空行（只能保留一个）

这样确保输出格式紧凑、阅读友好！
