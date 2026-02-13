#!/usr/bin/env bash
set -euo pipefail
WS="$HOME/.openclaw/workspace"
cd "$WS"
if [[ ! -d .git ]]; then
  echo "NO_GIT: $WS is not a git repo" >&2
  exit 1
fi
# Summarize changes in core files only
files=(AGENTS.md USER.md MEMORY.md IDENTITY.md TOOLS.md)
for f in "${files[@]}"; do
  if git diff --name-only | rg -q "^${f}$"; then
    echo "--- $f"
    git diff -- "$f" | sed -n '1,200p'
  fi
done
