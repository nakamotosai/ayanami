#!/usr/bin/env bash
set -euo pipefail

WS="/home/ubuntu/.openclaw/workspace"
TOPIC=openclaw\ 实用技巧
LOG="/home/ubuntu/.openclaw/workspace/logs/search/jobs/deepsearch-20260213-174539.log"

OUT_LINE=$(bash "$WS/skills/search-suite/scripts/deep_search.sh" "openclaw 实用技巧" | tail -n 1)
echo "$OUT_LINE" >> "$LOG"
OUT_FILE=$(printf "%s" "$OUT_LINE" | sed -n "s/^OK: //p")

if [[ -f "$OUT_FILE" ]]; then
  SUMMARY=$(sed -n /^## Summary/, "$OUT_FILE" | head -c 3500)
  bash "$WS/scripts/telegram_send.sh" 8138445887 "[DeepSearch 完成] openclaw 实用技巧\n\n$SUMMARY\n\n(文件: $OUT_FILE)" || true
else
  bash "$WS/scripts/telegram_send.sh" 8138445887 "[DeepSearch 失败] openclaw 实用技巧\n\n未找到输出文件。请查看日志: $LOG" || true
fi
