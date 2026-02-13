#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
DATE=${1:-}
if [[ -z "$DATE" ]]; then
  echo "usage: $0 YYYY-MM-DD" >&2
  exit 2
fi
SRC="$WS/memory/$DATE.md"
DST="$WS/MEMORY.md"
if [[ ! -f "$SRC" ]]; then
  echo "missing: $SRC" >&2
  exit 1
fi
# Promote only lines that the human explicitly marked as long-term.
# We keep it deterministic; no LLM inference here.
match=$(rg -n "\[LT\]" "$SRC" || true)
if [[ -z "$match" ]]; then
  echo "NO_LT_MARKS: add [LT] to daily lines you want to promote." >&2
  exit 0
fi
{
  echo
  echo "## Promoted from daily $DATE"
  rg "\[LT\]" "$SRC" | sed 's/\[LT\]//g'
} >> "$DST"
qmd update >/dev/null 2>&1 || true
echo "OK: promoted [LT] lines -> MEMORY.md"
