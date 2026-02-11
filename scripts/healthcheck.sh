#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_CLI="/home/ubuntu/.npm-global/bin/openclaw"
CFG="/home/ubuntu/.openclaw/openclaw.json"
NOTIFY_TARGET="8138445887"
GATEWAY_PORT="18789"
SYSTEMD_UNIT="openclaw-gateway.service"

failures=()

if [[ ! -r "$CFG" ]]; then
  failures+=("openclaw.json 不可读")
fi

if [[ ! -x "$OPENCLAW_CLI" ]]; then
  failures+=("openclaw CLI 不可用")
fi

if command -v systemctl >/dev/null 2>&1; then
  if systemctl --user list-units --type=service | grep -q "$SYSTEMD_UNIT"; then
    if ! systemctl --user is-active --quiet "$SYSTEMD_UNIT"; then
      failures+=("systemd 用户服务未运行: $SYSTEMD_UNIT")
    fi
  fi
fi

if ! ss -lnt 2>/dev/null | grep -q ":${GATEWAY_PORT} "; then
  failures+=("gateway 端口 ${GATEWAY_PORT} 未监听")
fi

if ! pgrep -f openclaw-gateway >/dev/null 2>&1; then
  failures+=("openclaw-gateway 进程不存在")
fi

scripts=(
  "/home/ubuntu/.openclaw/workspace/scripts/heartbeat_dynamic.sh"
  "/home/ubuntu/.openclaw/workspace/scripts/openclaw-backup.sh"
  "/home/ubuntu/.openclaw/workspace/scripts/openclaw-github-sync.sh"
  "/home/ubuntu/.openclaw/workspace/scripts/session_watch.py"
  "/home/ubuntu/.openclaw/workspace/scripts/live_user_capture.py"
  "/home/ubuntu/.openclaw/workspace/scripts/backup_verify.sh"
  "/home/ubuntu/.openclaw/workspace/scripts/cron_failure_notify.py"
)

for s in "${scripts[@]}"; do
  if [[ ! -x "$s" ]]; then
    failures+=("脚本不可执行: ${s}")
  fi
done

if [[ ${#failures[@]} -gt 0 ]]; then
  msg="健康检查失败：\n- ${failures[*]}"
  if [[ -x "$OPENCLAW_CLI" ]]; then
    "$OPENCLAW_CLI" message send --channel telegram --target "$NOTIFY_TARGET" --message "$msg" >/dev/null 2>&1 || true
  fi
  exit 1
fi

exit 0
