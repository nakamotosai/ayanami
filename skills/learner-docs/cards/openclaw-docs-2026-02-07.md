---
title: OpenClaw Docs Deep Study (CLI, Automation, Channels, Bedrock)
source: https://docs.openclaw.ai/
version: 2026-02-07
tags: [openclaw, docs, cli, automation, channels, bedrock]
related_skill: learner-docs
summary: Key operational facts and patterns for OpenClaw CLI, automation (cron/heartbeat/webhooks), channel setup, Bedrock auth, and broadcast groups.
context_references:
  - skills/learner-docs/references/summary.md
  - skills/learner-docs/references/sources.md
  - skills/learner-docs/references/last_summary.md
compression_level: overview
---

## Why it matters
OpenClaw’s operational model revolves around deterministic routing, scheduler separation (heartbeat vs cron), and safe external triggers. This card collects the core configuration behaviors and CLI entrypoints that govern those workflows.

## Key facts
- `openclaw agent` runs a single agent turn; `--agent` targets a configured agent; `--deliver` and reply routing are supported.
- `openclaw agents` manages isolated workspaces and writes identity fields from `IDENTITY.md` or CLI overrides.
- `openclaw approvals` manages exec approvals per host and stores files at `~/.openclaw/exec-approvals.json`.
- `openclaw browser` manages profiles (openclaw/chrome), tabs, snapshot/screenshot, and ref-based UI actions; Chrome relay needs manual attach.
- Cron runs in the gateway; main-session `systemEvent` rides heartbeat, isolated `agentTurn` runs in `cron:` sessions with delivery controls.
- Heartbeat is best for batched, context-aware checks; cron is for exact timing, isolation, or model overrides.
- Webhooks expose `/hooks/wake` and `/hooks/agent` with token auth; mappings/presets enable Gmail and custom transforms.
- Polls work on WhatsApp/Discord/Teams, with platform-specific limits.
- Telegram DMs share main session; groups are isolated and mention-gated by default; draft streaming is DM-only.
- Discord requires intents and has pairing/allowlist DM policies; guild channels are isolated.
- Bedrock uses AWS credential chain; optional discovery via `bedrock:ListFoundationModels`.
- Broadcast groups (WhatsApp) fan out to multiple agents, parallel or sequential, with isolated sessions.

## Patterns / guidance
- Prefer heartbeat for “awareness batching” and cron for “precision + isolation.”
- Treat webhooks and external payloads as untrusted; keep hooks behind tailnet/proxy and use token auth.
- Use agent/workspace separation to encode personas, tool permissions, and model costs.

## Practical starter steps
1) Configure a primary chat channel (Telegram is fastest) and keep DM pairing on.
2) Add heartbeat checklist in `HEARTBEAT.md` for periodic monitoring.
3) Use cron for exact-time reminders or heavy batch jobs with `--session isolated`.
4) Enable hooks for external events and use `/hooks/agent` for isolated runs.
5) Add Bedrock provider only after AWS credentials are detected or set `AWS_PROFILE=default` on EC2.
