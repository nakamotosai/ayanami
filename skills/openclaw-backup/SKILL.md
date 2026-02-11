---
name: openclaw-backup
description: Create hourly local backups of an OpenClaw instance on a VPS (config + workspace + extensions), manage retention, list backups, and guide safe restore. Use when the user asks to set up automatic backups, verify backups, list available backups, restore/rollback OpenClaw state, or check backup retention.
---

# OpenClaw Backup（本机自动备份/恢复）

## What this skill does

- Create a timestamped **local** backup tarball containing:
  - `~/.openclaw/openclaw.json`
  - `~/.openclaw/workspace/`
  - `~/.openclaw/extensions/`
- Enforce retention (default 72 files ≈ 3 days @ hourly)
- List and inspect backups
- Provide a **safe restore workflow** (restore is potentially destructive)

## Quick commands (host shell)

- Run one backup now:
  - `bash scripts/backup_now.sh`
- List backups:
  - `bash scripts/list_backups.sh`
- Restore (SAFE mode: stage only):
  - `bash scripts/restore.sh --backup <path-to-tar.gz> --mode stage`
- Restore (APPLY mode: writes files; requires explicit confirmation from owner):
  - `bash scripts/restore.sh --backup <path-to-tar.gz> --mode apply`

## Default settings

- Backup dir: `/home/ubuntu/.openclaw/backups`
- Retention: keep newest `72`

## Safety rule (non-negotiable)

- **backup/list/inspect**: can run directly.
- **restore/apply**: must ask owner to confirm before applying changes (it can overwrite config/workspace).

## Notes

- If backups are missing or empty, read `references/troubleshooting.md`.
