# self-evolve（自我进化）

目标：让 OpenClaw 在 VPS 上稳定“越用越强”。

包含两条自动化：
1. 每小时提炼（自动写入长期记忆 + 去重）
2. 每日 08:00（东京）提案（只发 1 条，最多 3 个升级项）

安全护栏：
- 默认不跑重型命令（例如 `qmd query/embed`），避免卡死。
- 所有长输出写入 `workspace/logs/`。
- 自动写长期记忆时必须去重，并保留可追溯证据（时间戳/来源文件）。

入口：
- 每小时提炼：`python3 scripts/evolve_hourly.py`
- 每日提案：`python3 scripts/evolve_daily_proposal.py`
