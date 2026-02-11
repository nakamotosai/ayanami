---
name: core-file-maintenance
description: Maintain and evolve OpenClaw core files (AGENTS.md, SOUL.md, USER.md, TOOLS.md, MEMORY.md) based on conversation-derived changes to preferences, workflows, tools, MCP, and skills. Use when user asks to auto-sync changes into core files without extra confirmation, or when summarizing daily changes into long-term memory.
---

# Core File Maintenance

## Overview
Use this skill to keep core files continuously updated from ongoing conversations. The goal is zero-lag synchronization: any change in preferences, workflows, tools, MCP servers, skills, or execution policy must be reflected in the core files immediately and reported once completed.

## Trigger Rules
- When the user states a **preference, workflow change, tool/skill/MCP change**, or execution rule → update core files automatically.
- Do not ask for confirmation unless the change is a high-risk operation (deletion, credentials, public outbound messaging).
- After changes, respond with a compact “done” summary and where it was written.

## Workflow (Standard)
1. **Detect change type**
   - Preference / execution style → AGENTS.md + MEMORY.md
   - Persona / tone → SOUL.md + MEMORY.md
   - User profile / personal details → USER.md + MEMORY.md
   - Tools / skills / MCP → TOOLS.md + MEMORY.md
   - Long-term rules → MEMORY.md (and any relevant core file)

2. **Write immediately**
   - Append or update the relevant section in the core files.
   - Avoid duplicating the same rule if it already exists.

3. **Record in daily memory**
   - Add a short line to `memory/YYYY-MM-DD.md` stating what was updated.

4. **Report back once**
   - Confirm updates, list files touched.
   - Do not re-ask for approval.

## Formatting Rules
- Keep entries concise and searchable.
- If adding a new rule, use a bullet or numbered line with date when helpful.
- For execution style: emphasize “少请示、多执行” and “高风险才确认”.

## Checklist (Quick)
- [ ] Update core files (AGENTS/SOUL/USER/TOOLS/MEMORY)
- [ ] Update daily memory (memory/YYYY-MM-DD.md)
- [ ] Report results once

## Notes
- Always prioritize user instructions over generic defaults.
- This skill exists to prevent drift between actual behavior and documented policy.
