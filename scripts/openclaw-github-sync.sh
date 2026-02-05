#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ubuntu/.openclaw/workspace"
BRANCH="master"

cd "$REPO_DIR"

# Only commit if there are changes
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chii: auto sync $(date -u +'%Y-%m-%dT%H:%M:%SZ')" --no-gpg-sign || true
  git push origin "$BRANCH"
fi
