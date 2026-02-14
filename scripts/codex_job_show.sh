#!/usr/bin/env bash
set -euo pipefail

JOB_ID=${1:-}
if [[ -z "$JOB_ID" ]]; then
  echo "usage: $0 <job_id>" >&2
  exit 2
fi

JF="$HOME/.openclaw/workspace/logs/codex/jobs/${JOB_ID}.json"
if [[ ! -f "$JF" ]]; then
  echo "NOT_FOUND: $JF" >&2
  exit 1
fi
cat "$JF"
