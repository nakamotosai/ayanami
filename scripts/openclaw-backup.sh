#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/home/ubuntu/.openclaw/backups"
TS="$(date -u +'%Y%m%dT%H%M%SZ')"
HOST="$(hostname -s 2>/dev/null || echo host)"
OUT="$BACKUP_DIR/openclaw_${HOST}_${TS}.tar.gz"
LOCK="/tmp/openclaw-backup.lock"
KEEP="7"

mkdir -p "$BACKUP_DIR"

exec 9>"$LOCK"
if ! flock -n 9; then
  exit 0
fi

TAR_ARGS=(
  --exclude=home/ubuntu/.openclaw/workspace/.git
  --exclude=home/ubuntu/.openclaw/workspace/.venv
  --exclude=home/ubuntu/.openclaw/workspace/venv
  --exclude=home/ubuntu/.openclaw/workspace/output/audio
  --exclude=home/ubuntu/.openclaw/workspace/memory_archive
  --exclude=home/ubuntu/.openclaw/workspace/mcp-image-extractor/node_modules
  --exclude=home/ubuntu/.openclaw/workspace/mcp-tesseract-server/node_modules
  --exclude=home/ubuntu/.openclaw/workspace/mcp-ffmpeg-helper/node_modules
)

INCLUDES=(
  home/ubuntu/.openclaw/openclaw.json
  home/ubuntu/.openclaw/workspace
)

if [ -d /home/ubuntu/.openclaw/extensions ]; then
  INCLUDES+=(home/ubuntu/.openclaw/extensions)
fi

if tar -czf "$OUT" "${TAR_ARGS[@]}" -C / "${INCLUDES[@]}"; then
  success=1
else
  success=0
fi

mapfile -t files < <(ls -1t "$BACKUP_DIR"/openclaw_*.tar.gz 2>/dev/null || true)
count="${#files[@]}"
if [ "$count" -gt "$KEEP" ]; then
  for ((i=KEEP; i<count; i++)); do
    rm -f "${files[$i]}" || true
  done
fi

if [ "$success" -eq 1 ]; then
  NOTIFY_TS="$(date '+%Y/%m/%d %H:%M:%S %Z')"
  NOTIFY_TARGET="8138445887"
  OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"
  NOTIFY_MSG="叽~ 主人，我在 ${NOTIFY_TS} 完成备份（${OUT##*/}），当前仅保留最近 ${KEEP} 份，并已排除大体积缓存目录。"
  "$OPENCLAW_CLI" message send --target "$NOTIFY_TARGET" --message "$NOTIFY_MSG" >/dev/null 2>&1 || true
else
  echo "[openclaw-backup] backup failed" >&2
fi