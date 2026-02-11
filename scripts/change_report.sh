#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
OUT_FILE="$WORKSPACE/memory/last_change_report.txt"
SNAP_FILE="$WORKSPACE/memory/last_change_report.snapshot"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$WORKSPACE/memory"

if [ -d "$WORKSPACE/.git" ]; then
  current=$(git -C "$WORKSPACE" status --porcelain=v1 | awk '{print $2}' | sed '/^$/d' | sort -u)
  if [ -z "$current" ]; then
    printf "%s\n" "$TIMESTAMP no file changes detected" | tee "$OUT_FILE"
    printf "" > "$SNAP_FILE"
    exit 0
  fi

  {
    printf "%s\n" "$TIMESTAMP changed files:"
    printf "%s\n" "$current" | sed 's#^#- #' 
  } | tee "$OUT_FILE"

  printf "%s\n" "$current" > "$SNAP_FILE"
  exit 0
fi

printf "%s\n" "$TIMESTAMP no git repo; change report unavailable" | tee "$OUT_FILE"
