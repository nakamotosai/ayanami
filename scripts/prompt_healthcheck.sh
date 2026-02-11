#!/usr/bin/env bash
set -euo pipefail

WS="/home/ubuntu/.openclaw/workspace"
FILES=("AGENTS.md" "SOUL.md" "USER.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md")

printf "\n[Prompt Healthcheck] %s\n" "$(date -Iseconds)"
for f in "${FILES[@]}"; do
  if [[ -f "$WS/$f" ]]; then
    size=$(stat -c%s "$WS/$f" 2>/dev/null || echo 0)
    mtime=$(stat -c%y "$WS/$f" 2>/dev/null || echo "-")
    printf "✅ %s | %s bytes | %s\n" "$f" "$size" "$mtime"
  else
    printf "⚠️  missing: %s\n" "$f"
  fi
done

printf "\nTips: If a file is missing, OpenClaw will inject a 'missing file' marker.\n"
