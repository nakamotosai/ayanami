#!/usr/bin/env bash
set -euo pipefail
MODE=${1:-}
OUTDIR="$HOME/openclaw-backups"
mkdir -p "$OUTDIR"
TS=$(date +%Y%m%d-%H%M%S)

STATE="$HOME/.openclaw"
if [[ ! -d "$STATE" ]]; then
  echo "NO_STATE_DIR: $STATE" >&2
  exit 1
fi

case "$MODE" in
  --safe)
    TAR="$OUTDIR/openclaw-safe-$TS.tar.gz"
    tar -czf "$TAR" \
      --exclude='.openclaw/credentials' \
      --exclude='.openclaw/keys' \
      --exclude='.openclaw/*.env' \
      -C "$HOME" .openclaw
    ;;
  --full)
    TAR="$OUTDIR/openclaw-full-$TS.tar.gz"
    tar -czf "$TAR" -C "$HOME" .openclaw
    ;;
  *)
    echo "usage: $0 --safe|--full" >&2
    exit 2
    ;;
esac

echo "OK: $TAR"
