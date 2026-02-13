#!/usr/bin/env bash
set -euo pipefail

MODE="search"  # default: fast + stable (no LLM expansion)
if [[ "${1:-}" == "--mode" ]]; then
  MODE="${2:-search}"
  shift 2
fi

Q=${1:-}
if [[ -z "$Q" ]]; then
  echo "usage: $0 [--mode search|query|vsearch] \"query\"" >&2
  exit 2
fi

case "$MODE" in
  search)
    qmd search "$Q" -c memory -n 10 --json
    ;;
  query)
    # Higher quality but may download models / be slower.
    qmd query "$Q" -c memory -n 10 --json
    ;;
  vsearch)
    qmd vsearch "$Q" -c memory -n 10 --json
    ;;
  *)
    echo "unknown mode: $MODE" >&2
    exit 2
    ;;
esac
