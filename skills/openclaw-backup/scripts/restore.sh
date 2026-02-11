#!/usr/bin/env bash
set -euo pipefail

MODE="stage"
BACKUP=""
STAGE_DIR="/tmp/openclaw-restore-stage"

while [ $# -gt 0 ]; do
  case "$1" in
    --backup) BACKUP="$2"; shift 2;;
    --mode) MODE="$2"; shift 2;;
    --stage-dir) STAGE_DIR="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [ -z "$BACKUP" ]; then
  echo "--backup is required" >&2
  exit 2
fi

mkdir -p "$STAGE_DIR"
rm -rf "$STAGE_DIR"/*

echo "[info] staging restore from: $BACKUP"
tar -xzf "$BACKUP" -C "$STAGE_DIR"

echo "[ok] staged at: $STAGE_DIR"

echo "[info] staged tree (top):"
find "$STAGE_DIR" -maxdepth 3 -type f | sed -n '1,120p'

if [ "$MODE" = "stage" ]; then
  echo "[done] stage-only; nothing written to ~/.openclaw" 
  exit 0
fi

if [ "$MODE" != "apply" ]; then
  echo "Unknown --mode: $MODE (use stage|apply)" >&2
  exit 2
fi

# APPLY mode (destructive): overwrite current state
# Caller MUST have obtained explicit owner confirmation.

echo "[warn] APPLY mode: overwriting OpenClaw state" >&2

# Backup current state quickly before overwrite
NOW="$(date -u +'%Y%m%dT%H%M%SZ')"
SAFETY="/home/ubuntu/.openclaw/backups/pre_restore_${NOW}.tar.gz"

tar -czf "$SAFETY" \
  -C / \
  home/ubuntu/.openclaw/openclaw.json \
  home/ubuntu/.openclaw/workspace \
  home/ubuntu/.openclaw/extensions \
  2>/dev/null || true

echo "[ok] safety backup created: $SAFETY"

# Restore files
rsync -a --delete "$STAGE_DIR"/home/ubuntu/.openclaw/workspace/ /home/ubuntu/.openclaw/workspace/
cp -f "$STAGE_DIR"/home/ubuntu/.openclaw/openclaw.json /home/ubuntu/.openclaw/openclaw.json

# Extensions may not exist
if [ -d "$STAGE_DIR"/home/ubuntu/.openclaw/extensions ]; then
  mkdir -p /home/ubuntu/.openclaw/extensions
  rsync -a --delete "$STAGE_DIR"/home/ubuntu/.openclaw/extensions/ /home/ubuntu/.openclaw/extensions/
fi

echo "[ok] restore applied. You may want to restart gateway: openclaw gateway restart"
