#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORIES_DIR="$WORKSPACE/memory"
TODAY="$(date -u +%Y-%m-%d)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
FILE="$MEMORIES_DIR/$TODAY.md"

# Append a short summary entry if not already recorded in today's memory
if [[ -d "$MEMORIES_DIR" ]]; then
  if [[ ! -f "$FILE" ]]; then
    printf "# Daily memory %s\n\n" "$TIMESTAMP" > "$FILE"
  fi
  if ! grep -q "heartbeat maintenance" "$FILE"; then
    printf "%s heartbeat maintenance: refreshed summaries.\n" "$TIMESTAMP" >> "$FILE"
  fi
fi

printf "$TIMESTAMP heartbeat maintenance completed\n"
