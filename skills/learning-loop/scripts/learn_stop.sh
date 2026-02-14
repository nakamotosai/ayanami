#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
. "$WS/skills/learning-loop/scripts/learn_lib.sh"

TOPIC=${1:-}
if [[ -z "$TOPIC" ]]; then
  echo "usage: $0 \"topic\"" >&2
  exit 2
fi

DIR=$(ensure_topic "$TOPIC")
touch "$DIR/stop.flag"

bash "$WS/scripts/telegram_send.sh" 8138445887 "[学习模式已停止] $TOPIC\n目录：$DIR" || true

echo "OK: stop $DIR"
