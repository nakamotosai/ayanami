---
name: openclaw-docs
description: Core OpenClaw official-docs skill. Summarizes Gateway scheduling, webhooks, channels, CLI, browser control, and model/provider setup with actionable steps.
---

# OpenClaw Official Docs — Core Skill

This skill distills the official OpenClaw documentation into a compact, actionable playbook. Use it to configure channels, automation, webhooks, CLI workflows, browser control, and model providers.

## 1) Key concepts (official docs distillate)

### Scheduling: Cron vs Heartbeat
- **Cron (Gateway scheduler)**: precise timing, persists jobs under `~/.openclaw/cron/`, supports `main` (system event on next heartbeat) and `isolated` (dedicated agent turn). One-shots auto-delete unless `deleteAfterRun=false`.
- **Heartbeat**: periodic awareness in the main session (default ~30 min). Best for batching checks and context-aware decisions; emits `HEARTBEAT_OK` when nothing is needed.

### Webhooks (External triggers)
- Gateway exposes `/hooks` with a required token (prefer `Authorization: Bearer`).
- `POST /hooks/wake` enqueues a system event and can trigger an immediate heartbeat.
- `POST /hooks/agent` runs an isolated agent turn, can deliver to a specific channel/recipient, and posts a summary back to main.
- Mappings/presets (e.g., Gmail) transform payloads into wake/agent actions.

### Channels (Messaging surfaces)
- Officially supported: WhatsApp, Telegram, Discord, Slack, Feishu/Lark, Google Chat, Mattermost, Signal, iMessage (legacy), BlueBubbles (recommended), MS Teams, LINE, Matrix, Zalo, WebChat, etc.
- Multiple channels can run simultaneously; routing is deterministic per chat.

### Telegram (Bot API)
- Bot API via grammY; long-polling by default, webhook optional.
- DM access is pairing by default; groups are isolated (`agent::telegram:group:`).
- Token via env `TELEGRAM_BOT_TOKEN` or config; config takes precedence.
- Privacy Mode may block group visibility; disable privacy mode or make bot admin.

### CLI essentials
- `openclaw agent`: run a direct agent turn via Gateway; supports target/agent/session-id, thinking level, and deliver-to-channel.
- `openclaw agents`: manage isolated agent workspaces; set identity via `IDENTITY.md` or explicit flags.
- `openclaw browser`: manage browser control, profiles, tabs, snapshots, screenshots, and Chrome extension relay.

### Browser control
- `openclaw` profile: dedicated OpenClaw-managed Chrome.
- `chrome` profile: attach existing Chrome tab via extension (manual attach).
- Browser actions include snapshot/screenshot/navigate/click/type; supports node host proxy for remote browsers.

### Polls
- Polls supported in WhatsApp (web), Discord, and MS Teams; options differ by channel.
- Use `openclaw message poll` or the message tool with `pollQuestion/pollOption`.

### Bedrock provider (AWS)
- Uses Bedrock Converse streaming; auth via AWS SDK credential chain.
- Supports discovery of streaming/text models; configurable cache, defaults, and provider filters.

### Broadcast Groups (Experimental)
- WhatsApp-only broadcast to multiple agents for the same incoming message.
- Strategies: parallel or sequential; use-case includes multi-language or QA workflows.

## 2) Quick operational recipes

### A) Schedule a reminder (cron)
1. Add a job with `openclaw cron add --at ... --session main --system-event ... --wake now`.
2. List jobs with `openclaw cron list`, inspect runs with `openclaw cron runs --id <jobId>`.

### B) Set up Telegram quickly
1. Create bot in @BotFather; get token.
2. Configure `channels.telegram.botToken` or set `TELEGRAM_BOT_TOKEN`.
3. Start gateway; approve DM pairing code on first message.
4. If bot misses group messages, disable privacy mode or grant admin rights.

### C) Webhook external trigger
1. Enable hooks and set token in config.
2. POST to `/hooks/wake` for a system event or `/hooks/agent` for an isolated agent run.
3. Use mappings or presets (e.g., Gmail) for structured payloads.

### D) Browser control quick start
1. `openclaw browser --browser-profile openclaw start`
2. `openclaw browser --browser-profile openclaw open https://docs.openclaw.ai`
3. `openclaw browser snapshot` or `openclaw browser screenshot`

## 3) When to use what (cheat sheet)
- **Heartbeat**: periodic checks, context-aware actions, reduce API calls.
- **Cron**: exact-time tasks, background analysis, reminders, isolated runs.
- **Webhook**: external event triggers (email, SaaS, CI, etc.).

## 4) Official source highlights (key URLs)
- Channels: https://docs.openclaw.ai/channels
- Telegram: https://docs.openclaw.ai/channels/telegram
- Cron jobs: https://docs.openclaw.ai/automation/cron-jobs
- Cron vs Heartbeat: https://docs.openclaw.ai/automation/cron-vs-heartbeat
- Webhooks: https://docs.openclaw.ai/automation/webhook
- Polls: https://docs.openclaw.ai/automation/poll
- Gmail PubSub: https://docs.openclaw.ai/automation/gmail-pubsub
- Browser CLI: https://docs.openclaw.ai/cli/browser
- Agent CLI: https://docs.openclaw.ai/cli/agent
- Agents CLI: https://docs.openclaw.ai/cli/agents
- Bedrock: https://docs.openclaw.ai/bedrock
- Broadcast Groups: https://docs.openclaw.ai/broadcast-groups
