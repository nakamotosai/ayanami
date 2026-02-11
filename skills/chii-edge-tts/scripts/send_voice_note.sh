#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VOICE="${CHII_TTS_VOICE:-zh-CN-XiaoxiaoNeural}"
OUT_DIR="${CHII_TTS_OUT_DIR:-/tmp/chii-tts}"
BITRATE="${CHII_TTS_OPUS_BITRATE:-64k}"
TARGET="${CHII_TTS_TELEGRAM_TARGET:-8138445887}"
CONFIG_PATH="${CHII_TTS_CONFIG_PATH:-/home/ubuntu/.openclaw/openclaw.json}"
CAPTION="${CHII_TTS_CAPTION:-}"

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <text...>" >&2
  exit 2
fi

TEXT="$*"
mkdir -p "$OUT_DIR"

MP3_PATH="$("$SKILL_DIR/gen_mp3.sh" --voice "$VOICE" --out-dir "$OUT_DIR" --text "$TEXT")"
OGG_PATH="${MP3_PATH%.mp3}.ogg"
ffmpeg -y -i "$MP3_PATH" -c:a libopus -b:a "$BITRATE" "$OGG_PATH"
rm -f "$MP3_PATH"

BOT_TOKEN="${CHII_TTS_TELEGRAM_TOKEN:-}"
if [ -z "$BOT_TOKEN" ]; then
  BOT_TOKEN=$(python3 - <<PY
import json, pathlib, sys
config = pathlib.Path("$CONFIG_PATH")
if not config.is_file():
    raise SystemExit(f"OpenClaw config not found at {config}")
data = json.loads(config.read_text())
bot = data.get("channels", {}).get("telegram", {}).get("botToken")
if not bot:
    raise SystemExit("Telegram bot token missing in OpenClaw config")
print(bot)
PY
)
fi

CURL_ARGS=(-sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendVoice" -F "chat_id=${TARGET}" -F "voice=@${OGG_PATH}")
if [ -n "$CAPTION" ]; then
  CURL_ARGS+=(-F "caption=${CAPTION}" -F "parse_mode=HTML")
fi

RESPONSE="$(curl "${CURL_ARGS[@]}")"
MESSAGE_ID=$(CHII_TTS_RESPONSE="$RESPONSE" python3 - <<'PY'
import json, os, sys
data = json.loads(os.environ.get("CHII_TTS_RESPONSE", "{}"))
if not data.get("ok"):
    raise SystemExit(f"Telegram sendVoice failed: {data}")
print(data.get("result", {}).get("message_id", "<unknown>"))
PY
)

rm -f "$OGG_PATH"

echo "[ok] voice note sent: ${MESSAGE_ID}"
