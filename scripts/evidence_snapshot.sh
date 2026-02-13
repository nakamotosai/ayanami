#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
OUTDIR="$WS/memory/evidence"
mkdir -p "$OUTDIR"
OUT="$OUTDIR/latest.md"
TS_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cd "$WS"

{
  echo "# Evidence Snapshot"
  echo
  echo "- ts_utc: $TS_UTC"
  echo "- workspace: $WS"
  echo

  echo "## Git"
  if command -v git >/dev/null 2>&1 && [[ -d .git ]]; then
    echo "- branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
    echo "- head: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
    echo "- dirty: $(git status --porcelain | wc -l | tr -d ' ') files"
    echo
    echo "### Changed Files (tracked diff)"
    git diff --name-only || true
    echo
    echo "### Untracked (top 50)"
    git ls-files --others --exclude-standard | sed -n '1,50p' || true
  else
    echo "- git: not available"
  fi
  echo

  echo "## QMD"
  if command -v qmd >/dev/null 2>&1; then
    qmd status 2>/dev/null | sed -n '1,120p' || true
  else
    echo "- qmd: not installed"
  fi
  echo

  echo "## MCP (mcporter)"
  if command -v mcporter >/dev/null 2>&1; then
    (cd "$WS" && mcporter list 2>/dev/null) || true
  else
    echo "- mcporter: not installed"
  fi
  echo

  echo "## Recent Logs (top 20)"
  find "$WS/logs" -type f -maxdepth 3 -printf '%TY-%Tm-%TdT%TH:%TM:%TSZ %p\n' 2>/dev/null | sort -r | sed -n '1,20p' || true
} > "$OUT"

echo "$OUT"
