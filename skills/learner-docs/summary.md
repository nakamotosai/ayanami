# OpenClaw Official Docs — Learner Summary (2026-02-07)

## 🔹关键事实/结论
- OpenClaw 的**Cron**是 Gateway 内置调度器，作业持久化于 `~/.openclaw/cron/`，支持 main/isolated 两种执行模式，精准触发（cron/at/every）。
- **Heartbeat**是主会话周期检查机制，擅长“批量+上下文感知”的巡检，空闲时返回 `HEARTBEAT_OK`。
- **Webhook**提供 `/hooks` 入口，支持 wake 与 agent 两类动作，并可通过映射/预设（如 Gmail）把外部事件转成自动化任务。
- **Channels**覆盖 WhatsApp/Telegram/Discord/Slack/Signal/LINE/Teams 等；多通道并行运行、路由确定。
- **Browser CLI**支持 profile、tab、snapshot、screenshot 与 Chrome 扩展接管；也支持 node 代理远控。
- **Bedrock**通过 AWS SDK 认证，无需 API key；支持自动发现流式模型并缓存。
- **Broadcast Groups**（实验）可在 WhatsApp 中让多个 agent 同时响应同一消息。

## 🔹核心理解/洞察
- OpenClaw 的“自动化骨架”由 **Cron + Heartbeat + Webhook** 三件套组成：
  - Cron = 精准时间
  - Heartbeat = 智能巡检
  - Webhook = 外部触发
- 频道层与执行层完全分离：消息进来后由 Gateway 统一路由，模型不需要“选择频道”。
- Browser/Profile/Node 的组合让“在本地浏览器 vs 远程浏览器”变成可配置策略。

## 🔹教给主人用的操作步骤/练习
1) **设置定时提醒**：`openclaw cron add --at ... --session main --system-event ... --wake now`
2) **启动 Telegram Bot**：配置 `channels.telegram.botToken`，必要时关闭隐私模式或设为 admin。
3) **开启 Webhook**：配置 `hooks.enabled=true` 与 `hooks.token`，调用 `/hooks/wake` 或 `/hooks/agent`。
4) **浏览器自动化**：`openclaw browser --browser-profile openclaw start` → `open` → `snapshot`。

## 🔹参考来源与 diff 变动链接
- Channels: https://docs.openclaw.ai/channels
- Telegram: https://docs.openclaw.ai/channels/telegram
- Cron: https://docs.openclaw.ai/automation/cron-jobs
- Cron vs Heartbeat: https://docs.openclaw.ai/automation/cron-vs-heartbeat
- Webhooks: https://docs.openclaw.ai/automation/webhook
- Polls: https://docs.openclaw.ai/automation/poll
- Gmail PubSub: https://docs.openclaw.ai/automation/gmail-pubsub
- Browser CLI: https://docs.openclaw.ai/cli/browser
- Agent CLI: https://docs.openclaw.ai/cli/agent
- Agents CLI: https://docs.openclaw.ai/cli/agents
- Bedrock: https://docs.openclaw.ai/bedrock
- Broadcast Groups: https://docs.openclaw.ai/broadcast-groups

Diffs snapshot: /home/ubuntu/.openclaw/workspace/skills/learner-docs/references/last_summary.md
