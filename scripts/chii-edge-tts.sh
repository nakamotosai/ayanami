#!/usr/bin/env bash
set -euo pipefail

VOICE="${CHII_TTS_VOICE:-zh-CN-XiaoxiaoNeural}"
OUT_DIR="${CHII_TTS_OUT_DIR:-/tmp/chii-tts}"
TEXT="${*:-}"

if [ -z "$TEXT" ]; then
  echo "Usage: $0 <text...>" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
TS="$(date -u +'%Y%m%dT%H%M%SZ')"
OUT="$OUT_DIR/chii_${TS}.mp3"

/home/ubuntu/.openclaw/venv/edge-tts/bin/edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$OUT"

echo "$OUT"
