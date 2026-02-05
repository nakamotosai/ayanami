#!/usr/bin/env bash
set -euo pipefail

VOICE="zh-CN-XiaoxiaoNeural"
OUT_DIR="/tmp/chii-tts"
TEXT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --voice) VOICE="$2"; shift 2;;
    --out-dir) OUT_DIR="$2"; shift 2;;
    --text) TEXT="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

if [ -z "$TEXT" ]; then
  echo "--text is required" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
TS="$(date -u +'%Y%m%dT%H%M%SZ')"
OUT="$OUT_DIR/chii_${TS}.mp3"

EDGE_BIN="/home/ubuntu/.openclaw/venv/edge-tts/bin/edge-tts"
if [ ! -x "$EDGE_BIN" ]; then
  echo "edge-tts not found at $EDGE_BIN" >&2
  exit 1
fi

"$EDGE_BIN" --voice "$VOICE" --text "$TEXT" --write-media "$OUT"

echo "$OUT"
