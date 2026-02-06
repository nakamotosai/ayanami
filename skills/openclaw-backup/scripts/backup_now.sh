#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/ubuntu/.openclaw/backups"
TS="$(date -u +'%Y%m%dT%H%M%SZ')"
HOST="$(hostname -s 2>/dev/null || echo host)"
OUT="$BACKUP_DIR/openclaw_${HOST}_${TS}.tar.gz"
LOCK="/tmp/openclaw-backup.lock"
KEEP="50"

mkdir -p "$BACKUP_DIR"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[skip] backup already running" >&2
  exit 0
fi

# Archive config + workspace + extensions
# (If an entry doesn't exist, tar prints to stderr; we suppress noisy errors.)
tar -czf "$OUT" \
  -C / \
  home/ubuntu/.openclaw/openclaw.json \
  home/ubuntu/.openclaw/workspace \
  home/ubuntu/.openclaw/extensions \
  2>/dev/null || true

# Retention: keep newest $KEEP
mapfile -t files < <(ls -1t "$BACKUP_DIR"/openclaw_*.tar.gz 2>/dev/null || true)
count="${#files[@]}"
if [ "$count" -gt "$KEEP" ]; then
  for ((i=KEEP; i<count; i++)); do
    rm -f "${files[$i]}" || true
  done
fi

echo "[ok] $OUT"
