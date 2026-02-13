#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
Q=${1:-}
if [[ -z "$Q" ]]; then
  echo "usage: $0 \"query\"" >&2
  exit 2
fi

OUT="$WS/memory/research/fast-$(date -u +%Y%m%d-%H%M%S).md"

{
  echo "# Fast Search"
  echo
  echo "- ts_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- query: $Q"
  echo
  echo "## QMD (memory)"
  cd "$WS" && mcporter call qmd.search query="$Q" collection="memory" limit=10 --output json || true
  echo
  echo "## SearXNG"
  cd "$WS" && mcporter call searxng.searxng_search query="$Q" limit=8 --output json
} > "$OUT"

qmd update >/dev/null 2>&1 || true
bash "$WS/scripts/evidence_snapshot.sh" >/dev/null 2>&1 || true

echo "OK: $OUT"
