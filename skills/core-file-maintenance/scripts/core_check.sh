#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
need=("USER.md" "MEMORY.md" "IDENTITY.md" "TOOLS.md" "AGENTS.md")
missing=0
for f in "${need[@]}"; do
  if [[ ! -f "$WS/$f" ]]; then
    echo "MISSING: $WS/$f"
    missing=1
  fi
done
if [[ $missing -eq 0 ]]; then
  echo "OK: core files present"
fi
