# TODOs（主人未完成事项清单）

> 规则：这里是“唯一真相源”。ちぃ会在心跳/复盘中持续更新状态，不会写完就丢。

## 🔥 Active（进行中）
- [ ] 创建 core-file-maintenance 技能并完善 SKILL.md（核心文件自动同步流程）。
- [ ] Study Agent（-1003576271520）学习型常驻：初始化规则与记忆强化工作流验证。

- [ ] （待捕获）

- [ ] Replace the temporary TLS artifacts under /etc/letsencrypt/live/searxng with valid certificates, free port 80 from openresty (or move nginx to another port), and reload nginx so HTTPS can proxy to Gunicorn.

- [ ] Hooked session 0c48e21a-c3dc-4040-91e6-27c7c6a239ff (pending your manual summary).

- [ ] Hooked session 5d06fc4c-909f-48ea-949b-91044d798d0b (pending your manual summary).

- [ ] Hooked session 2139b9fa-0e6f-4444-811e-c5a0a11f1258 (pending your manual summary).

- [ ] Hooked session 3f69ba14-5630-423b-b7a2-73b5946c2a2e (pending your manual summary).

- [ ] Hooked session 83144fd8-238e-4373-b802-7bf7d9ce5c5d (pending your manual summary).

- [ ] Hooked session 03fb58fa-7bd4-4557-abb2-c6d4fcc75963 (pending your manual summary).

- [ ] Hooked session eb39e6f8-9b25-4f1f-8f61-2d8ccf0efd4d (pending your manual summary).

## ⏳ Waiting（等主人/等外部条件）
- [ ] （待捕获）

## ✅ Done（已完成，保留最近 20 条）
- [x] 深度研读 docs.openclaw.ai，完成 Learner 摘要/卡片/图表并同步知识库 (2026-02-07).
- [x] 深度学习 docs.openclaw.ai 并输出完整 OpenClaw 技能总结（2026-02-07）。
- [x] Ran `scripts/prompt_healthcheck.sh` and confirmed `docs/prompt-upgrade-decisions.md` exists for the prompt upgrade follow-through (2026-02-07).
- [x] Installed tavily-search、find-skills、proactive-agent-1-2-4 and documented them in TOOLS.md for quick reference (2026-02-07).
- [x] Added `export TAVILY_API_KEY=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` to `~/.bashrc` so tavily-search can talk to the internet out of the box (2026-02-07).
- [x] Ran proactive-agent-1-2-4's security audit script to surface configuration warnings (2026-02-07).
- [x] Started proactive-agent-1-2-4 onboarding in its own workspace and captured Sai's answers to all 12 core questions (2026-02-07).
- [x] 增加 main 代理与 Telegram group 默认绑定（*），确保默认会话归属 main。（2026-02-06）
- [x] 配置工具调用策略（禁用 memory_search）+ 新增 moltbook 代理与 -1003700261569 工作区绑定 + 迁移 line-daughter 工作区。（2026-02-06）
- [x] 检查工具调用/子agent/隔离工作区/后台分配机制并汇报。（2026-02-06）
- [x] 为 LINE 女儿专用 bot 创建独立工作区并绑定指定用户，彻底与主工作区解耦。（2026-02-06）
- [x] 调整心跳逻辑：长时间不互动后仅触发一次 heartbeat，避免连续重复。（2026-02-06）
- [x] 创建并加载 xhs-jewelry-copywriter 技能：珠宝产品信息自动改写为小红书标题+正文+标签，含参数解析与单位校验。（2026-02-06）

- [x] Installed Context7 MCP server, created context7 user/dirs, systemd service, env placeholder `/etc/context7/context7.env`, and exposed port 3000; remaining manual step: set `CONTEXT7_API_KEY` before restarting. (2026-02-06)

- [x] 更新 AGENTS.md + memory 规则：所有指令任务都写入 memory/todos.md（完成后打钩但保留），并同步到今日记忆。

- [x] 将 memory-lite 与 memory-curator 两项记忆管理技能安装到 workspace/skills，以便随时管理记忆文件与摘要。

- [x] 把原有的其他 skill 从 `skills-local/` 迁回 `skills/`，确保所有技能都在主目录下可用。

- [x] 安装 `local-websearch`（自托管 SearXNG）与 `ddg-search`（DuckDuckGo）技能，并在 `~/.bashrc` 里写入 `SEARXNG_URL=http://127.0.0.1:8888` 让搜索脚本直接连本地实例。
