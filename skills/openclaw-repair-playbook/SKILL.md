---
name: openclaw-repair-playbook
description: OpenClaw 故障排查与修复清单（基于本机真实修复手段）。适用于：Codex/工具无法调用、tools 为空、gateway 失效、skills 缺失、记忆/工具规则冲突、dist 缺失、文档/技能优先级混乱等。
---

# OpenClaw Repair Playbook

## Use scope
- Fix tool list errors (e.g., tools [] too short), Codex CLI not callable.
- Restore missing skills or broken `skills/` directory.
- Normalize core rules (AGENTS/MEMORY/TOOLS) after drift or hallucination.
- Rebuild `skills/dist` when packaging is incomplete.

## Core workflow (execute in order)
1. Verify tool allowlist for main agent.
2. Confirm Codex CLI path is usable (or fall back).
3. Restore skills directory if missing or truncated.
4. Rebuild dist packages (optional).
5. Normalize AGENTS/MEMORY/TOOLS consistency rules.
6. Restart gateway and re-test.

## Reference files
- See `references/repair-checklist.md` for exact commands and verification.
