#!/usr/bin/env bash
set -euo pipefail
OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"
TARGET_ID="8138445887"
if [[ $# -lt 1 ]]; then
  echo "usage: notify_progress.sh <message>" >&2
  exit 1
fi
msg="$1"
if [[ -x "$OPENCLAW_CLI" ]]; then
  "$OPENCLAW_CLI" message send --channel telegram --target "$TARGET_ID" --message "$msg" >/dev/null 2>&1 || true
fi