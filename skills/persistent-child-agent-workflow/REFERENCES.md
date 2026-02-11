# References for Persistent Child Agent Workflow

1. **AGENTS.md** – source of truth for high-level role behavior and rules for new agents. Reading this ensures the child agent inherits the correct tone and commands.
2. **SOUL.md** – captures persona expectations. Always copy the latest persona file into every agent workspace so the persistent child agent talks in the right voice.
3. **USER.md** – contains owner preferences (language, tone, nickname). Keep a synced copy inside the child workspace for contextual replies.
4. **TOOLS.md** – outlines available skills and utilities. Having this in the child workspace helps onboard future maintainers quickly.
5. **memory/ and memory/HEARTBEAT.md** – reference when establishing heartbeat policies or syncing memory log access.
6. **skills/core-file-maintenance/SKILL.md** – explains how we keep core files auto-synced; useful when you update shared documents inside the child workspace.
7. **config/group-agent-policy.json** – use as a baseline for agent-specific policies and adjust the child agent's policy patch accordingly.
8. **gateway configuration files** (if present under `config/`) – consult these before applying the generated `gateway-config.patch` so you do not accidentally overwrite existing entries.
