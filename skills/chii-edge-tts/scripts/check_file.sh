#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <file>" >&2
  exit 2
fi

if [ ! -f "$FILE" ]; then
  echo "missing file: $FILE" >&2
  exit 1
fi

SIZE=$(wc -c < "$FILE" | tr -d ' ')
if [ "$SIZE" -le 0 ]; then
  echo "empty file: $FILE" >&2
  exit 1
fi

echo "ok $SIZE bytes"
