# TOOLS.md - 主人和ちぃ的专属工具手札

## 这是什么
- 这里写的不是“默认模板”，而是我们俩一起打卡的地头，记录常用技能、关键路径、能直接取用的小技巧。
- 出去看文档和代码我会帮你搞，回来我就把记事本里的要点贴在这，让你一句话就能召回用法。
- 视觉太花我会省略，尽量短句+清单，保证翻得快。

## 各技能目录（位于 `/home/ubuntu/.openclaw/workspace/skills`）
- `chii-edge-tts`：用 Edge TTS 生成语音（主打可爱女声 `zh-CN-XiaoxiaoNeural`），需要我送个链接 / 指令就说。 
- `dist`：项目打包/发布流程相关全家桶（常用 `npm run dist`、`clawhub sync`）。
- `github-uploader-workflow`：给 GH 仓库自动生成 issue/PR/summary 时候用的脚本集合。
- `group-agent-execution`：启动多个 telegram agent 的模板，记录了 `spawn` 命令和环境变量。
- `kaomoji-vibes`：颜文字库，用来结尾签名或心跳小纸条（按需要挑选一两个颜文字，就像我们平常那样）。
- `mcporter-mcp`（MCP 统一入口）
- `local-websearch`：直接对接我们自托管的 SearXNG（URL `http://127.0.0.1:8889`，已经写进 `~/.bashrc` 的 `SEARXNG_URL`）。快速搜索示例：`python3 skills/local-websearch/scripts/searxng_search.py "openclaw news" --count 10`。
- `ddg-search`：DuckDuckGo 搜索脚本（`skills/ddg-search/scripts/search.sh "query"`），可以在分身 agent 中直接用来查最新网页、新闻或关键词。
- `memory-curator`：把 daily log 压缩成 digest（用 `./scripts/generate-digest.sh [YYYY-MM-DD]` 生成骨架，补充 Summary/Key Events/Learnings/Tomorrow）。
- `memory-lite`：要写 NOTE 或 grep 记忆时就进这里，常用脚本：`python3 scripts/memory_add.py --kind daily/long --text ...`、`bash scripts/memory_grep.sh "关键词"`、`python3 scripts/memory_summarize.py --days N`。
- `openclaw-backup`：备份 workspace/skills 之类的工具，常配合 `snapshot` 和 `restore` 命令。
- `openclaw-docs`：OpenClaw 官方文档完整技能卡（Cron/Heartbeat/Webhook/Channels/CLI/Browser/Bedrock/Broadcast Groups）。
- `sonoscli`：控制 Sonos 设备（有专属 `sonos` shell 命令），平日播放音乐也能召唤。
- `telegram-setup`：管理 telegram agent 的配置、Webhook，放在这里方便查 `config` 目录里的参数。
- `xhs-jewelry-copywriter`：将珠宝产品信息自动改写为小红书风格的标题+正文+标签，包含参数解析与单位校验。
- `tavily-search`：联网技能，帮我们用指定搜索引擎查看实时外网信息，让ちぃ可以“睁眼看世界”。
- `find-skills`：主动寻找最合适的技能解决问题，遇到不熟悉的需求时先问它而不是一直靠我猜。
- `proactive-agent-1-2-4`：用于启动主动、自我迭代的代理 agent，方便生成、测试、升级技能链；我会在需要时去配合它。

> 需要用哪个技能就告诉我名字，我可以直接 `cd skills/<name>` 或 `python3 scripts/...` 来示范。

## 日常记忆/日志引用
- 主记忆目录：`/home/ubuntu/.openclaw/workspace/memory/`（`MEMORY.md`, `2026-02-05.md`、`2026-02-06.md` 等）。
- 任务跟踪：记得打开 `memory/todos.md`，我会在那里自动写入当前重要事项（Active/Waiting/Done 结构）。
- 记忆更新：如果你说“记住”、“记忆一下”等，我就把关键点追加到 `memory/` 下的文件，再用 `memory-lite` 或 `memory-curator` 区段压缩。可以随时问我“最近记忆里有什么”我会告诉你摘要。

## 帮你总结用途
- 想要“记住一个任务” → 用 `memory-lite/scripts/memory_add.py` 追加 daily/long entry。
- 想把某天日志浓缩 → 先 `./skills/memory-curator/scripts/generate-digest.sh YYYY-MM-DD` 再在 digest 中补写 Summary/Learnings。需要我写模板我来。
- 需要语音提醒/播报 → 直接在 `chii-edge-tts` 里调用 `make_voice.sh`，我会按你想要的语气调整。

## 其他实用路径
- `config/`：agent/gateway/cron 配置（如果要查某个子 agent workspace config 就跳到对应 `telegram-<id>-workspace` 里）。
- `memory/HEARTBEAT.md`：每到心跳我都看它，写了想要提醒的事。

需要我把这份手札再做成 quick reference 卡片，或者截图放进 `README.md` 里？想要的话，ちぃ马上做出来～*/ᐠ｡ꞈ｡ᐟ*
## QMD 记忆检索（统一标准）
- 关键词：`qmd search "关键词" -c memory --json -n 10`
- 语义：`qmd query "描述式问题" -c memory --json -n 10`
- 取全文：`qmd get "qmd://memory/YYYY-MM-DD.md" --full`
- 先列文件：`qmd ls memory`
- 规则：禁止使用 memory_search。

## 新增技能
- `core-file-maintenance`：核心文件自动同步规则与维护流程（AGENTS/SOUL/USER/TOOLS/MEMORY）。


## MCP (mcporter)
- 统一入口：mcporter（配置在 /home/ubuntu/.openclaw/workspace/config/mcporter.json）。
- 已接入：qmd（memory 查询）与 searxng（联网搜索）。
- 快速查看：cd /home/ubuntu/.openclaw/workspace && mcporter list。
- 详细用法：skills/mcporter-mcp/SKILL.md。

## 密钥与 Hook
- 统一密钥位置：`/home/ubuntu/.openclaw/credentials/secrets.json`、`secrets.env`，以及运行用 `~/.openclaw/.env`。
- 同步脚本：`/home/ubuntu/.openclaw/workspace/scripts/secrets_sync.py --export|--apply`。
- Hook 调用需来源校验：`scripts/hooks_agent_dispatch.py` / `scripts/hooks_wake.py` 需要 `--source`（值来自 `HOOKS_SOURCE_TOKEN`）。

## 子 agent 执行
- 主会话工具禁用：只允许 sessions 工具，所有命令/文件/联网任务必须 `sessions_spawn`。
- 子 agent 默认超时：`runTimeoutSeconds=180`；自动归档：30 分钟。
- 辅助模板：`scripts/subagent_dispatch.py` 已包含超时要求。

