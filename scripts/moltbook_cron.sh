#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
LOG_DIR="$WS/logs/moltbook-cron"
mkdir -p "$LOG_DIR"
RUN_DIR="$LOG_DIR/$(date -u +%Y%m%d-%H%M%SZ)"
mkdir -p "$RUN_DIR"
PROMPT=$(cat <<'EOF'
你是 Moltbook 社区的活跃成员，目标是关注 OpenClaw 相关的自我升级、自我进化、记忆存储、稳定性等话题，并在有价值的讨论里参与一次。任务：
1. 浏览热门/最新帖子，挑选 2~3 条与上述方向高度相关的内容，每条提炼标题/链接/ID、3 条要点（尤其标注可借鉴的策略、工具、流程），并给出 1~2 条针对性的建议（例如：你该回复什么、记录什么、跟进哪个资源）。
2. 如果发现特别契合的帖子，写一条高信息密度的评论（引用具体行动，要求包含建议/原理/下一步），并在输出中标注被评论的帖子 ID 与评论内容。
3. 总结：最后用一段话告诉我你做了哪些事情，有没有发帖/评论，哪些洞见值得记忆。
要求输出中文，结构清晰，便于我直接转述。
EOF
)
OUTPUT_FILE="$RUN_DIR/result.json"
cd "$WS" && openclaw agent --agent moltbook -m "$PROMPT" --json >"$OUTPUT_FILE"
SUMMARY=$(jq -r '.result.payloads[].text' "$OUTPUT_FILE" | head -n 2000)
if [[ -n "$SUMMARY" && "$SUMMARY" != "null" ]]; then
  bash "$WS/scripts/telegram_send.sh" 8138445887 "[Moltbook巡查] $(date -u +'%Y-%m-%dT%H:%M:%SZ' )\n$SUMMARY" || true
fi
