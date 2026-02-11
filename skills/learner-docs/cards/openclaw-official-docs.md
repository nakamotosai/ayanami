---
title: "OpenClaw Official Docs — Core Skill"
source: "https://docs.openclaw.ai/"
version: "2026-02-07"
tags: [openclaw, docs, automation, channels, cli, browser, webhooks]
related_skill: "openclaw-docs"
summary: "Distills OpenClaw’s official docs into a compact skill covering cron/heartbeat/webhooks, channel setup (Telegram/WhatsApp/etc.), CLI usage, browser control, Bedrock provider setup, and broadcast groups."
---

## Key Facts
- Cron runs in Gateway; jobs persist under `~/.openclaw/cron/` with main vs isolated execution.
- Heartbeat is periodic main-session awareness; returns `HEARTBEAT_OK` when idle.
- Webhooks (`/hooks`) accept wake/agent actions with token auth; mappings/presets enable Gmail flows.
- Channels are modular; Telegram uses grammY with pairing default for DMs.
- Browser CLI controls OpenClaw-managed and extension-attached Chrome profiles.
- Bedrock uses AWS SDK credentials; supports automatic model discovery.
- Broadcast Groups (experimental) allow multi-agent responses in WhatsApp.

## How to Use (Quick Steps)
1) Cron reminder: `openclaw cron add --at ... --session main --system-event ... --wake now`.
2) Telegram: set `channels.telegram.botToken` or `TELEGRAM_BOT_TOKEN`; disable privacy mode for full group visibility.
3) Webhook trigger: enable hooks + token; POST `/hooks/wake` or `/hooks/agent`.
4) Browser automation: `openclaw browser --browser-profile openclaw start` → `open` → `snapshot`.

## Sources
- https://docs.openclaw.ai/channels
- https://docs.openclaw.ai/channels/telegram
- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/automation/cron-vs-heartbeat
- https://docs.openclaw.ai/automation/webhook
- https://docs.openclaw.ai/automation/poll
- https://docs.openclaw.ai/automation/gmail-pubsub
- https://docs.openclaw.ai/cli/browser
- https://docs.openclaw.ai/cli/agent
- https://docs.openclaw.ai/cli/agents
- https://docs.openclaw.ai/bedrock
- https://docs.openclaw.ai/broadcast-groups

## Metadata
- context_references: ["/home/ubuntu/.openclaw/workspace/skills/learner-docs/references/summary.md", "/home/ubuntu/.openclaw/workspace/skills/learner-docs/references/last_summary.md"]
- compression_level: medium
