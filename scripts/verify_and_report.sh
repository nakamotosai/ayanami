#!/usr/bin/env bash
set -euo pipefail

task_desc="${1:-}" 
file_path="${2:-}" 

printf "--- TASK EVIDENCE ---\n"
printf "time: %s\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
if [[ -n "$task_desc" ]]; then
  printf "task: %s\n" "$task_desc"
fi

if [[ -n "$file_path" ]]; then
  if [[ -f "$file_path" ]]; then
    printf "status: file exists\n"
    ls -lh "$file_path"
    printf "--- file tail (last 5 lines) ---\n"
    tail -n 5 "$file_path" || true
  else
    printf "status: ERROR file not found\n"
    printf "path: %s\n" "$file_path"
    exit 1
  fi
else
  printf "status: no file path provided\n"
fi