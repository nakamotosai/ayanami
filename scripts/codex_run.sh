#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
LOGDIR="$WS/logs/codex"
mkdir -p "$LOGDIR"

TS=$(date -u +%Y%m%d-%H%M%S)
LAST_MSG="$LOGDIR/last-$TS.md"
JSONL="$LOGDIR/events-$TS.jsonl"

PROMPT=${1:-}
if [[ -z "$PROMPT" ]]; then
  echo "usage: $0 \"task prompt\"" >&2
  exit 2
fi

# Non-interactive execution. Write agent's final message to LAST_MSG.
# Hard timeout prevents chat stalls.
( timeout ${CODEX_TIMEOUT:-600}s codex exec --full-auto -C "$WS" --output-last-message "$LAST_MSG" --json "$PROMPT" ) >"$JSONL" 2>&1 || true

echo "OK: codex_exec_done last_msg=$LAST_MSG events=$JSONL"

# System-generated evidence snapshot (do not hand-write evidence)
EV=$(bash "$WS/scripts/evidence_snapshot.sh" || true)
echo "EVIDENCE: ${EV:-$WS/memory/evidence/latest.md}"
