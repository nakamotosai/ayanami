#!/usr/bin/env bash
set -euo pipefail

# Alias for the voice-note workflow so you can run it from the workspace
# without remembering the skill path.
SCRIPT="/home/ubuntu/.openclaw/workspace/skills/chii-edge-tts/scripts/send_voice_note.sh"
if [ ! -x "$SCRIPT" ]; then
  echo "Voice-note script missing: $SCRIPT" >&2
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Usage: $0 <text...>" >&2
  exit 2
fi

bash "$SCRIPT" "$@"
