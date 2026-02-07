#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ubuntu/.openclaw/workspace"
BRANCH="master"
LOCK="/tmp/openclaw-github-sync.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  exit 0
fi

cd "$REPO_DIR"

git fetch origin "$BRANCH" >/dev/null 2>&1 || true
# Rebase on remote if possible to avoid divergence
if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git rebase "origin/$BRANCH" >/dev/null 2>&1 || true
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "chii: auto sync $(date -u +'%Y-%m-%dT%H:%M:%SZ')" --no-gpg-sign
  git push origin "$BRANCH"
fi
