# telegram-setup - Configure Telegram channel features

## Purpose
Capture the authoritative setup steps, gating switches, and capability checklist for OpenClaw's Telegram channel so future agents can implement or debug configuration changes in a single scroll. Include the concepts of tokens, dm policy, group privacy, draft streaming, command menus, and troubleshooting hints drawn straight from the official Telegram channel docs (https://docs.openclaw.ai/channels/telegram).

## When to use
- The user wants to modify anything under `channels.telegram` (bot token, DM/grouppolicy, allowlists, mention patterns, draft streaming, custom commands, streamMode).
- A troubleshooting task touches Telegram-specific behaviors (privacy mode, sendMessage failures, https/dns blocking, command menu updates, draft streaming requirements).
- You need to explain what Telegram features OpenClaw can provide and choose which to enable/implement.

## Summary of capabilities you can toggle by following the doc
1. **Token & access** – set `channels.telegram.botToken` (config overrides env), optionally define accounts (multi-token via `channels.telegram.accounts`), keep the token private, regenerate via BotFather if leaked.
2. **DM pairing vs open** – DM access defaults to pairing; confirm the token is set and approve the pairing code; adjust `channels.telegram.dmPolicy` to `pairing`/`open` as needed.
3. **Group behavior** – groups are `agent:main:telegram:group:<id>` sessions; use `channels.telegram.groups` to gate mentions/allowlists and match allow/ban regex patterns. Adjust privacy via BotFather `/setprivacy` or add bot as admin to see all messages; mention gating commands (per-agent `groupChat.mentionPatterns`).
4. **Draft streaming** – enable when you have threaded DM mode in BotFather and `channels.telegram.streamMode` is `partial` (or `block`). Works only for private chats with thread IDs; groups not supported.
5. **Formatting** – Outbound uses HTML parse_mode; OpenClaw sanitizes Markdown-like input. Retries plain text on Telegram parse failure.
6. **Custom commands** – use `channels.telegram.customCommands` to add bot menu entries (e.g., `/backup`, `/generate`). This registers with Telegram on startup.
7. **Troubleshooting signals** – `setMyCommands` failed indicates outbound connectivity; sendMessage errors point to IPv6/DNS issues.

## Workflow guidance
1. Confirm the user has a BotFather token and knows which DM policy/group settings are desired.
2. Update `channels.telegram` config in `openclaw.json` (or env keys) to match the requested features (botToken, dmPolicy, groups, streamMode, customCommands). Use `channels.telegram.groups`/`agents.list[].groupChat` to apply custom mention patterns.
3. Restart/reload the gateway to apply the new config and watch for logs (e.g., `setMyCommands` success, mention pattern warnings).
4. For troubleshooting, inspect `openclaw logs`, run `openclaw doctor`, and verify that Telegram HTTP calls succeed (watch for IPv6/DNS errors).
5. When enabling draft streaming, ensure BotFather's Threaded Mode is on and streamMode is not `off`.

## References
- `https://docs.openclaw.ai/channels/telegram`
- `~/.openclaw/openclaw.json` (`channels.telegram` block and `apps.telegram` entries)
- BotFather commands: `/newbot`, `/setprivacy`, `/setjoingroups`, thread mode toggle, and token regeneration.
