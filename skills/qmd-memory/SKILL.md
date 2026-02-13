# qmd-memory

用途：用 qmd 对 `workspace/memory` 进行记忆查找（全文/语义/组合查询）。

集合：`memory`（指向 `~/.openclaw/workspace/memory/*.md`）

常用命令：
- 全文检索：`qmd search "关键词" -c memory -n 10 --json`
- 语义检索：`qmd vsearch "描述" -c memory -n 10 --json`
- 组合查询：`qmd query "问题" -c memory -n 10 --json`
- 列文件：`qmd ls memory`
- 取全文：`qmd get "qmd://memory/<file>" --full`

维护：
- 新增/修改记忆后：`qmd update`
