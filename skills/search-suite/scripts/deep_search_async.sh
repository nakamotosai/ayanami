#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
TOPIC=${1:-}

if [[ -z "$TOPIC" ]]; then
  echo "usage: $0 \"topic\"" >&2
  exit 2
fi

JOBDIR="$WS/logs/search/jobs"
mkdir -p "$JOBDIR"
TS=$(date -u +%Y%m%d-%H%M%S)
JOB_ID="deepsearch-$TS"
LOG="$JOBDIR/$JOB_ID.log"
RUNNER="$JOBDIR/$JOB_ID.sh"

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  printf "WS=%q\n" "$WS"
  printf "TOPIC=%q\n" "$TOPIC"
  printf "LOG=%q\n" "$LOG"
  cat <<RUN

OUT_LINE=$(bash "$WS/skills/search-suite/scripts/deep_search.sh" "$TOPIC" | tail -n 1)
echo "$OUT_LINE" >> "$LOG"
OUT_FILE=$(printf "%s" "$OUT_LINE" | sed -n "s/^OK: //p")

if [[ -f "$OUT_FILE" ]]; then
  SUMMARY=$(sed -n /^## Summary/, "$OUT_FILE" | head -c 3500)
  bash "$WS/scripts/telegram_send.sh" 8138445887 "[DeepSearch 完成] $TOPIC\n\n$SUMMARY\n\n(文件: $OUT_FILE)" || true
else
  bash "$WS/scripts/telegram_send.sh" 8138445887 "[DeepSearch 失败] $TOPIC\n\n未找到输出文件。请查看日志: $LOG" || true
fi
RUN
} > "$RUNNER"

chmod +x "$RUNNER"
nohup bash "$RUNNER" >"$LOG" 2>&1 &

echo "OK_ASYNC: job_id=$JOB_ID log=$LOG"
