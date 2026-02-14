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
KB="$DIR/kb.md"
Q="$DIR/questions.md"
S="$DIR/state.json"

round=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["round"])' "$S" 2>/dev/null || echo 0)
kb_chars=$(wc -c <"$KB" 2>/dev/null || echo 0)
q_lines=$(rg -n "^- " "$Q" 2>/dev/null | wc -l | tr -d " " || echo 0)

msg=$(printf "[学习进度] %s\n- round=%s\n- kb_chars=%s\n- open_questions=%s\n- dir=%s" "$TOPIC" "$round" "$kb_chars" "$q_lines" "$DIR")

bash "$WS/scripts/telegram_send.sh" 8138445887 "$msg" || true
