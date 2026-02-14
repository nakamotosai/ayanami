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
OUT="$DIR/report.md"

# Create a long-form report by composing kb + open questions + sources.
{
  echo "# $TOPIC 深度学习完整报告"
  echo
  echo "生成时间(UTC)：$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## 目录"
  echo "- 1. 总览"
  echo "- 2. 核心概念与机制"
  echo "- 3. 交易与市场结构"
  echo "- 4. 套利与策略（含风险与边界）"
  echo "- 5. 风险管理与常见坑"
  echo "- 6. 自测题与错题集"
  echo "- 7. 术语表"
  echo "- 8. 未解问题清单"
  echo "- 9. 来源索引"
  echo
  echo "## 1. 总览"
  echo "本报告来自多轮循环学习过程沉淀的知识库，目标是‘不精简’，尽可能完整覆盖。"
  echo
  echo "## 2-7. 知识库（逐步沉淀）"
  echo
  cat "$DIR/kb.md"
  echo
  echo "## 8. 未解问题清单"
  echo
  cat "$DIR/questions.md"
  echo
  echo "## 9. 来源索引"
  echo
  cat "$DIR/sources.md"
} >"$OUT"

qmd update >/dev/null 2>&1 || true

# Send via Telegram (chunked). If you later want email, add SMTP config.
bash "$WS/scripts/telegram_send_document.sh" 8138445887 "$OUT" "[学习报告定稿] $TOPIC（全文见附件）" || true

echo "OK: $OUT"
