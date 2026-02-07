# OpenClaw Official Docs — Summary (2026-02-07)

## Key facts
- Cron jobs run in the Gateway, persist under `~/.openclaw/cron/`, support main vs isolated execution, and accept at/every/cron schedules.
- Heartbeat is the periodic main-session check with context-aware batching; returns `HEARTBEAT_OK` when idle.
- Webhooks (`/hooks`) accept wake or agent actions with required token auth, and support mappings/presets (e.g., Gmail).
- Channels are modular and can run concurrently; Telegram uses grammY and defaults to pairing for DMs.
- Browser CLI controls OpenClaw-managed or extension-attached Chrome profiles and supports snapshots/screenshot/actions.
- Bedrock provider uses AWS SDK credentials; automatic model discovery is available.
- Broadcast Groups (experimental) allow multiple agents to respond to the same WhatsApp message.

## Core workflows
1) Schedule precise reminders with cron; use heartbeat for periodic awareness.
2) Use webhooks to trigger agent runs from external systems.
3) Configure channels (Telegram/WhatsApp/etc.) with allowlists and privacy rules.
4) Automate browser tasks via `openclaw browser` profiles.

## Sources
See `references/sources.md`.
