# Troubleshooting

## Backups not appearing

- Check directory exists: `/home/ubuntu/.openclaw/backups`
- Run a manual backup:
  - `bash /home/ubuntu/.openclaw/workspace/skills/openclaw-backup/scripts/backup_now.sh`
- If you see `[skip] backup already running`, wait 1 minute and retry.

## Backup file is too small / empty

- Ensure these paths exist on the machine:
  - `/home/ubuntu/.openclaw/openclaw.json`
  - `/home/ubuntu/.openclaw/workspace/`
  - `/home/ubuntu/.openclaw/extensions/` (optional)

## Restore safety

- Prefer `--mode stage` first, inspect the staged tree, then apply only after owner confirmation.
