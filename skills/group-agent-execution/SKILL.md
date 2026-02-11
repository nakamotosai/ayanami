# group-agent-execution - Telegram group agent deployment skill

## Purpose
Provide a single reference for onboarding, configuring, and operating Telegram group agents under the solo-mode policy (short-lived subagents allowed). Anyone (including future agents) who runs a task matching this description should read this file first.

## When to use
- The user asks for a new Telegram group agent or workspace.
- The user wants to review or modify the way Telegram group agents operate.
- A task requires remembering that Telegram group agents run solo but can spawn short-lived subagents for heavy/tool tasks.

## Policy summary
1. **Solo mode**: Every Telegram group agent runs independently; short-lived subagents are allowed for heavy/tool tasks; persistent subagents are disallowed (see `config/group-agent-policy.json`).
2. **Workspace naming**: Create the workspace directory as `telegram-<group_id>-workspace` under `/home/ubuntu/.openclaw/workspace`.
3. **Memory link**: Record the policy in `MEMORY.md` (core rule #24) so subsequent turns know the rule applies to future group agents.
4. **Group onboarding**: Before spinning a new group agent, confirm the group exists, the bot is present, and you have the group ID (e.g. `-100xxxxxxxx`).
5. **Prompting**: The new agent should inherit the same persona/system instructions as the main agent, including the subagent-first rule for heavy/tool tasks.
6. **Skill use**: Any agent asked to manage group agents should cite `config/group-agent-policy.json` and `MEMORY.md（核心守则：群聊 agent 策略）` to verify compliance before creating or modifying agents.

## Workflow (for future additions)
1. Confirm the Telegram group ID and ensure OpenClaw Bot is added with chat privileges. Mention which workspace file and policy entries will be updated.
2. Create the workspace folder: `mkdir -p telegram-<group_id>-workspace` inside the workspace root.
3. Update any group-specific resources (templates, skill prompts) inside that workspace if needed.
4. Spawn the group agent (e.g., via `sessions_spawn` or equivalent) using the new workspace and route it to `agent:main:telegram:group:<group_id>`. Short-lived subagents are allowed for heavy/tool tasks; do not create persistent subagents.
5. If the user asks, describe what just happened referencing the policy file and the memory entries.

## References
- `config/group-agent-policy.json` (defines `soloMode` and `allowSubagents`).
- `MEMORY.md` core rule #24 (records the group-agent subagent policy).
