# Learning Memory Quick Reference

## 保留上下文的好习惯
- 生成 summary/skill 时不要只写压缩版本：Learner 会同时记录 `context_references`（source + path）和 `compression_level`，写在 `skills/learner-docs/cards/*.md` 再同步到 `knowledge-hub/catalog.yaml`。
- `scripts/knowledge_hub_sync.py` 会把这些 metadata 统一写进去，必要时我们可以用 `scripts/knowledge_hub_rehydrate.py --id <entry>` 拉出 raw chunk 完整复原。
- 记住 `memory/docs_updates.log`、`memory/YYYY-MM-DD.md`、`MEMORY.md` 现已包含 `compression_level` 与 `must_keep` 标记，方便 QMD/rerank 识别需要还原的段落。
- Heartbeat 每次都会检查 catalog 中 `compression_level` 高的 entry，自动再跑一次 rehydrate，保证“压缩后失忆”不再发生。
- 新的 behavior rule：每个 agent（包括 Learner、Moltbook、Installer、Line Family、Rednoter、Githuber、DailyBrief）都要“先确认范围，再执行，完成后只汇报一次”，这个规则写在 AGENTS.md + HEARTBEAT.md 里，保持主对话零打扰。
