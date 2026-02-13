# telegram-setup

用途：把 Telegram 作为主渠道接通、排障、验证。

核心命令（OpenClaw 内置）：
- 查看渠道状态：`openclaw channels status --probe`
- Telegram 相关查看：`openclaw channels list` / `openclaw channels login`（按提示）
- 发送测试消息：`openclaw message send --channel telegram --target <chat_id|@name> --message "test"`

本技能提供检查脚本：
- `bash scripts/telegram_check.sh`
