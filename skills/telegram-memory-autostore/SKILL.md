# Telegram 私聊记忆自动化（telegram-memory-autostore）

目标：每次心跳时自动把 Telegram 私聊的新增对话落盘，并维护短期/长期记忆。

数据层：
- Raw 原文：`workspace/memory/raw/telegram/<peer>/YYYY-MM-DD.jsonl`
- Daily 短期：`workspace/memory/YYYY-MM-DD.md`
- Long-term 长期：`workspace/MEMORY.md`

触发：
- Heartbeat：运行 `scripts/capture_and_store.py`

规则：
- 只处理 **私聊**（sessions.json 里 channel=telegram 且 chatType=direct）。
- 只追加“用户消息”（from=telegram:8138445887）到 raw/daily。
- 遇到消息以 `请记住` / `记住:` / `记住：` 开头：立即写入长期记忆并 `qmd update`。

运行：
```bash
python3 scripts/capture_and_store.py
```
