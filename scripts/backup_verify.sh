#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/ubuntu/.openclaw/backups"
OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"
NOTIFY_TARGET="8138445887"

latest=$(ls -1t "$BACKUP_DIR"/openclaw_*.tar.gz 2>/dev/null | head -n 1 || true)

if [[ -z "$latest" ]]; then
  msg="备份验证失败：未找到任何 openclaw 备份文件。"
  if [[ -x "$OPENCLAW_CLI" ]]; then
    "$OPENCLAW_CLI" message send --channel telegram --target "$NOTIFY_TARGET" --message "$msg" >/dev/null 2>&1 || true
  fi
  exit 1
fi

if ! tar -tzf "$latest" >/dev/null 2>&1; then
  msg="备份验证失败：tar -t 失败（${latest##*/}）。"
  if [[ -x "$OPENCLAW_CLI" ]]; then
    "$OPENCLAW_CLI" message send --channel telegram --target "$NOTIFY_TARGET" --message "$msg" >/dev/null 2>&1 || true
  fi
  exit 1
fi

exit 0
