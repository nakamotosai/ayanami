#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/ubuntu/.openclaw/workspace
PROMPT=$(python3 "$ROOT/scripts/codex_auto.py" "$@")
MODEL="${CODEX_MODEL:-gpt-5.1-codex-mini}"
MODEL_SHORT="${MODEL##*/}"
printf "%s" "$PROMPT" | codex exec -m "$MODEL_SHORT" --sandbox danger-full-access --dangerously-bypass-approvals-and-sandbox
