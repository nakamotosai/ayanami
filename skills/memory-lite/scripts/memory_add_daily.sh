#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
MEMDIR="$WS/memory"
mkdir -p "$MEMDIR"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TEXT=${1:-}
if [[ -z "$TEXT" ]]; then
  echo "usage: $0 \"text\"" >&2
  exit 2
fi
FILE="$MEMDIR/$(date +%Y-%m-%d).md"
{
  echo
  echo "## ${TS}"
  echo "- ${TEXT}"
} >> "$FILE"
qmd update >/dev/null 2>&1 || true
printf "OK: appended to %s\n" "$FILE"
