# TODOs（主人未完成事项清单）

> 规则：这里是“唯一真相源”。ちぃ会在心跳/复盘中持续更新状态，不会写完就丢。

## 🔥 Active（进行中）
- [ ] 🧩 下一步：保持 cron 每两分钟运行脚本，一旦 /new 或 /reset 触发会自动摘录历史会话并更新 MEMORY/记忆日志/todos；我也会在那时再向主人报告新的整理结果（来自 session f89004de）

- [ ] System: [2026-02-07 23:48:28 GMT+9] Cron: 结论：`scripts/session_watch.py` 已经按要求实现“/new 或 /reset 后自动进化记忆”逻辑—它读取 `~/.openclaw/agents/main/sessions/sessions.json` 的 `agent:main:main.sessionId`，对比 `memor…（来自 session f89004de）

- [ ] 证据：脚本本身的流程与写入逻辑直接对应需求（来自 session f89004de）

- [ ] 🧩 下一步建议：保持这个脚本由 cron 以定期（如每 5 分钟）执行，以便在 /new 或 /reset 后自动触发；一旦 sessionId 变更，它会自动把新内容分别写入 `MEMORY.md`、当日记忆与 todos 并通知主人（来自 session f89004de）

- [ ] System: [2026-02-07 23:50:16 GMT+9] Cron: ✅ 结论: `/home/ubuntu/.openclaw/workspace/scripts/session_watch.py` 已经实现了你描述的 session-watch hook —— 通过 `sessions.json` 比对 `memory/session-watch.json`、tail 最后…（来自 session f89004de）

- [ ] 🔎 证据: 脚本直接使用 `agent:main:main` 的 sessionId、会写入 `memory/session-watch.json`、`MEMORY.md`、`memory/YYYY-MM-DD.md`、`memory/todos.md`，且结尾 `print` 通知与步骤一致，可在 `/home/ubuntu/.openclaw/workspace/scripts/sess…（来自 session f89004de）

- [ ] 🧩 下一步: 只要保持这脚本周期性运行（cron 已在 heartbeat 指令里配置），就可以继续让 /new 和 /reset 自动触发记忆进化；如需要调关键词/摘要策略，再告诉我我去微调（来自 session f89004de）

- [ ] System: [2026-02-07 22:17:19 GMT+9] Cron: 脚本 `scripts/session_watch.py` 已经实现了你描述的流程：每次 sessionId 发生变化时读取 `~/.openclaw/agents/main/sessions/<last>.jsonl` 的最后 200 行、提炼长期规则/今日记忆/todo、更新 `memory/sessio…（来自 session 858d11bb）

- [ ] 说明文件 `scripts/session_watch.md` 也已记录如何用 cron 定期触发该脚本（例如 `*/5 * * * * cd /home/ubuntu/.openclaw/workspace && ./scripts/session_watch.py`），确保新会话出现时自动整理记忆而不会重复写入（来自 session 858d11bb）

- [ ] System: [2026-02-07 22:22:19 GMT+9] Cron: 新的 `scripts/session_watch.py` 已经能在主会话换 ID 时拉取前一个 `.jsonl`（最后 200 行）、抽关键词、写入 MEMORY/当日记忆/待办、刷新 `memory/session-watch.json` 并在有更新时报“我已在后台整理并进化记忆 + 更新 todo”（平…（来自 session 858d11bb）

- [ ] 刚才那次 reset 的结果已经写进 `memory/2026-02-07.md`（21:07:31 的 Summary/Decision/Risk/Open todo）、todo 列表新增“继续打磨 session-watch automation”，watch 文件同步到当前 session，剩下只要把 `*/5 * * * * cd /home/ubuntu/.openclaw/wor…（来自 session 858d11bb）

- [ ] Source: memory/2026-02-07.md#63-66; memory/todos.md#6; memory/session-watch.json#1-3; scripts/session_watch.md#10-16（来自 session 858d11bb）

- [ ] System: [2026-02-07 22:42:40 GMT+9] Cron: session_watch.py 已经把“/new 或 /reset 后进化记忆”这套 hook 流程实现好了：它读取 session-watch.json 的 lastSessionId（仍然是 858d11bb-519c-4137-b886-4b6481c46c56）、比对当前主会话 ID、并在相同情况下…（来自 session 858d11bb）

- [ ] System: [2026-02-07 22:45:04 GMT+9] Cron: 脚本 `scripts/session_watch.py` 已经按照你的步骤实现：每次提取 `~/.openclaw/agents/main/sessions/sessions.json` 的当前 sessionId，读取上一个会话的 `.jsonl` 末尾 200 行，提炼包含规则/偏好/决定/风险/tod…（来自 session 858d11bb）

- [x] 2) 读取工作区 `memory/session-watch.json` 的 `lastSessionId` 作为 last（若文件不存在则创建并写入 current，然后输出严格 NO_REPLY）（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] - 以“反幻觉 1/2/4/6”标准，提炼并自动写入：（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] A) `MEMORY.md`：只写长期有效的新规则/偏好/固定事实（不重复旧内容）（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] B) `memory/YYYY-MM-DD.md`（东京时间）：写入这次会话结束的摘要、决定、坑、以及未完成事项（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] C) `memory/todos.md`：更新未完成任务清单（最多新增/更新 7 条；能标记 Done 的就移到 Done）（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] - 最后更新 `memory/session-watch.json`：把 lastSessionId 改成 current（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [x] - 给主人发 1 条极简通知（1–3 行）：“我已在后台整理并进化记忆 + 更新 todo”（完成于 2026-02-07T21:23:00Z，session f3339d35-9a19-4c19-9c51-0c72a8bab0b9）

- [ ] 继续打磨 session-watch automation（scripts/session_watch.py）：让它在每次会话 reset 后都补全 memory/todos/daily log。

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

- [ ] Hooked session f6304c5c-27c0-4b27-8bd6-4ea7da0f3df9 (pending your manual summary).

- [ ] Hooked session 4f7aa8e1-9316-49c5-8467-0767cc825270 (pending your manual summary).

- [ ] Hooked session ec3534f5-9426-4214-9c4d-fe9697728e9c (pending your manual summary).

- [ ] Hooked session d7036f14-cb96-4781-9bfc-4e9bfe9599aa (pending your manual summary).

- [ ] Hooked session 647e4636-5dc7-4638-892d-c4647f41403b (pending your manual summary).

- [ ] Hooked session a7b36c78-edbb-4a9a-87b3-f7adbfd9e8b2 (pending your manual summary).

- [ ] Hooked session 36f40038-2c29-4034-8f87-4944f1380bfa (pending your manual summary).

- [ ] Hooked session 92cda59c-49ed-4f4b-ac6a-acb0fa47eb27 (pending your manual summary).

- [ ] 彻底检查 ~/.openclaw 目录，确认常驻子 agent 清理干净、修复残留并向主人汇报（来源 session-36f40038-2c29-4034-8f87-4944f1380bfa）。

- [ ] Hooked session 7b8ed0c3-98e6-4015-bc7e-f4384b71ce91 (pending your manual summary).

- [ ] Hooked session f3339d35-9a19-4c19-9c51-0c72a8bab0b9 (pending your manual summary).

- [ ] Hooked session ce1d6ffa-753b-48f5-b971-842aac879bf6 (pending your manual summary).

- [ ] Hooked session ca791393-6697-48f5-9a71-c7d84f9ce22b (pending your manual summary).

- [ ] Hooked session 925f4f67-b15e-433b-b6c9-6a6104c808c1 (pending your manual summary).

- [ ] Hooked session 93e59965-b521-47a5-8519-73fff2f8be70 (pending your manual summary).

- [ ] Hooked session bc0abf5c-3b25-4909-b991-c0606545f088 (pending your manual summary).

- [ ] Hooked session c4f81808-2a13-44e8-973d-5ad7e00acbcc (pending your manual summary).

- [ ] Hooked session ca950a26-db15-4d19-aad9-3cb79f4863eb (pending your manual summary).

- [ ] Hooked session bdbcd564-8adc-435a-b51a-119d4b80e8cb (pending your manual summary).

- [ ] Hooked session 8470f665-f6c8-4bda-8193-2633e61fd836 (pending your manual summary).

- [ ] Hooked session c74348d2-9348-4770-a44e-4c5eed55d24e (pending your manual summary).

- [ ] Hooked session a6edf3e3-6aac-463f-a7f4-e10d97006b3b (pending your manual summary).

- [ ] Hooked session 986e5875-207d-4eb0-86cd-b6d8699b4881 (pending your manual summary).

- [ ] Hooked session d16947bb-8546-44ab-8919-d16ee913ea09 (pending your manual summary).

- [ ] Hooked session b88a6442-f15e-4945-a1e7-60a4c2963ee4 (pending your manual summary).

- [ ] Hooked session 7921b46c-758d-4cd5-9fe4-6f4d0464a675 (pending your manual summary).

- [ ] Hooked session c42820da-9ef3-46a8-aff4-5df30f0148fe (pending your manual summary).

- [ ] Hooked session cf5191af-ce01-47c8-bc14-8d69dcc747a6 (pending your manual summary).

- [ ] Hooked session f75b0f5b-a02a-4e6a-84be-85ef816de1ec (pending your manual summary).

- [ ] Hooked session 76f9c2a2-84a0-4183-a644-68f9449b34b3 (pending your manual summary).

- [ ] Hooked session 98773d32-a75a-4b18-96af-1ef3201f4f71 (pending your manual summary).

- [ ] Hooked session 714e78c4-09db-497d-9425-a4d84f6b9e56 (pending your manual summary).

- [ ] Hooked session 29fd7f25-bd95-40df-9f83-39c49e4e62a0 (pending your manual summary).

- [ ] Hooked session 8458a303-216e-4b40-8c5b-7b58a2fcbcd9 (pending your manual summary).

- [ ] Hooked session 8aa32cbf-0335-4722-81cf-0404f3ef8524 (pending your manual summary).

## ⏳ Waiting（等主人/等外部条件）
- [ ] （待捕获）

## ✅ Done（已完成，保留最近 20 条）
- [x] Hooked session f89004de-17e0-467d-95d2-65e20400f570（自动总结于 2026-02-08T00:45:01Z）

- [x] Hooked session 858d11bb-519c-4137-b886-4b6481c46c56（自动总结于 2026-02-07T23:45:01Z）

- [x] Hooked session 30c91063-80a5-4d1e-8951-31996737d61a（自动总结于 2026-02-07T22:28:40Z）

- [x] Hooked session 9bfdca08-2b9a-4e16-ba34-cc2cb0a3f84f（自动总结于 2026-02-07T22:25:01Z）

- [x] 运行 session-watch 自动化流程：提取 session f3339d35-9a19-4c19-9c51-0c72a8bab0b9 转录、更新 MEMORY/2026-02-07.md/todos、刷新 watch 文件并通知主人（2026-02-07T21:23:00Z）
- [x] Hooked session 18b69853-e738-4ad0-87fa-39b817b10763（自动总结于 2026-02-07T21:20:40Z）」}{

- [x] 清理全部常驻子 agent：移除 openclaw.json 配置、删除 agents/workspace 目录、清除 cron 中的子 agent 任务，并重启网关（2026-02-07）。
- [x] 生成今日日本热门事件日报（10条，纯中文，日文检索后翻译）（2026-02-07）。
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
