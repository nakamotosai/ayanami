#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR="/home/ubuntu/.openclaw/backups"
ls -1t "$BACKUP_DIR"/openclaw_*.tar.gz 2>/dev/null || true
