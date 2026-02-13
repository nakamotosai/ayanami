#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
LT="$WS/MEMORY.md"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TEXT=${1:-}
if [[ -z "$TEXT" ]]; then
  echo "usage: $0 \"text\"" >&2
  exit 2
fi
{
  echo
  echo "## ${TS}"
  echo "- ${TEXT}"
} >> "$LT"
qmd update >/dev/null 2>&1 || true
printf "OK: long-term -> %s\n" "$LT"
