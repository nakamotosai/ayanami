#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
python3 "$WS/skills/enhanced-memory/scripts/dedupe_memory.py" "$WS/MEMORY.md" || true
qmd update || true
echo "OK: maintain (dedupe + qmd update)"
