#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
LOGDIR="$WS/logs/codex"
mkdir -p "$LOGDIR"

# OpenClaw background runners may not inherit interactive PATH.
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

CODEX_BIN="${CODEX_BIN:-$(command -v codex || true)}"
if [[ -z "$CODEX_BIN" && -x "$HOME/.npm-global/bin/codex" ]]; then
  CODEX_BIN="$HOME/.npm-global/bin/codex"
fi

TS=$(date -u +%Y%m%d-%H%M%S)
LAST_MSG="$LOGDIR/last-$TS.md"
JSONL="$LOGDIR/events-$TS.jsonl"

PROMPT=${1:-}
if [[ -z "$PROMPT" ]]; then
  echo "usage: $0 \"task prompt\"" >&2
  exit 2
fi

if [[ -z "$CODEX_BIN" ]]; then
  echo "ERROR: codex binary not found (PATH=$PATH)" >"$JSONL"
  echo "ERROR: codex_not_found events=$JSONL"
  exit 127
fi

# Non-interactive execution. Write agent's final message to LAST_MSG.
# Hard timeout prevents chat stalls.
( flock -w ${CODEX_LOCK_WAIT:-30} 9 || exit 1
  timeout ${CODEX_TIMEOUT:-600}s "$CODEX_BIN" exec --full-auto -C "$WS" --output-last-message "$LAST_MSG" --json "$PROMPT" ) 9>"$LOGDIR/.codex.lock" >"$JSONL" 2>&1 || true

echo "OK: codex_exec_done last_msg=$LAST_MSG events=$JSONL"

# System-generated evidence snapshot (do not hand-write evidence)
EV=$(bash "$WS/scripts/evidence_snapshot.sh" || true)
echo "EVIDENCE: ${EV:-$WS/memory/evidence/latest.md}"
