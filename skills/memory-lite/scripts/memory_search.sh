#!/usr/bin/env bash
set -euo pipefail
Q=${1:-}
if [[ -z "$Q" ]]; then
  echo "usage: $0 \"query\"" >&2
  exit 2
fi
qmd search "$Q" -c memory -n 10 --json
