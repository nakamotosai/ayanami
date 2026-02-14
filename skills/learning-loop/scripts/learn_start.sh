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
rm -f "$DIR/stop.flag" 2>/dev/null || true

LOCK="$DIR/.learn.lock"
( flock -w ${LEARN_LOCK_WAIT:-2} 9 || exit 0

  N=${LEARN_ROUNDS_PER_START:-1}
  for i in $(seq 1 "$N"); do
    bash "$WS/skills/learning-loop/scripts/learn_round.sh" "$TOPIC"
    sleep 2
    [[ -f "$DIR/stop.flag" ]] && break
    sleep ${LEARN_ROUND_SLEEP:-30}
  done

) 9>"$LOCK"

echo "OK: started topic=$TOPIC dir=$DIR rounds=${LEARN_ROUNDS_PER_START:-1}"
