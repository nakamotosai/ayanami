#!/usr/bin/env bash
set -euo pipefail
STATE="$HOME/.openclaw"
echo "== openclaw channels status =="
openclaw channels status --probe || true

echo
for f in "$STATE/credentials/telegram-pairing.json" "$STATE/credentials/telegram-allowFrom.json"; do
  if [[ -f "$f" ]]; then
    echo "FOUND: $f"
  else
    echo "MISSING: $f"
  fi
done
