# OpenClaw 2026.2.9 发布说明（中文翻译）

## 新增
- iOS：实验性节点应用与 onboarding setup-code，方便在 Apple 设备上启动节点。（#11756）感谢 @mbelinky。
- Channels：全面整理 BlueBubbles 渠道并清理旧项，改善渠道面板体验。（#11093）感谢 @tyler6204。
- Plugins：新增设备配对与手机控制插件（Telegram /pair、iOS/Android 节点控制），可在插件市场直接管理。（#11755）感谢 @mbelinky。
- 工具：将 Grok（xAI）接入 web_search 供应商列表，支持新型搜索来源。（#12419）感谢 @tmchow。
- Gateway：为 Web UI 添加 agent 管理 RPC（agents.create/update/delete），便于界面动态控制代理。（#11045）感谢 @advaitpaliwal。
- Web UI：聊天记录中显示压缩（Compaction）分隔线，更直观地看到不同段落。（#11341）感谢 @Takhoffman。
- Agents：在 agent 封包中包含运行时 shell 访问，提升工具执行能力。（#1835）感谢 @Takhoffman。
- 路径：引入 `OPENCLAW_HOME` 变量，可覆盖内部路径解析时的 home 目录。（#12091）感谢 @sebslight。

## 修复
- Telegram：增强引用解析、保留引用上下文、规避 `QUOTE_TEXT_INVALID`、避免嵌套回复错判。（#12156）感谢 @rybnikov。
- Telegram：在主题 ID 过期时尝试不带 `message_thread_id` 重试，恢复主动推送。 (#11620)
- Telegram：用 `<tg-spoiler>` 渲染 Markdown “剧透”结构。（#11543）感谢 @ezhikkk。
- Telegram：命令注册截断至 100 条，避免 `BOT_COMMANDS_TOO_MUCH` 启动失败。（#12356）感谢 @arosstale。
- Telegram：匹配 DM allowFrom 时先用 sender user id 备用 chat id，配对日志更清晰。（#12779）感谢 @liuxiaopai-ai。
- Onboarding：QuickStart 下自动安装 shell 补全（Manual 模式仍提示）。
- Auth：去除 API key/token 中的换行再保存以避免解析错误。
- Web UI：刷新聊天时平滑滚动到底部，手动刷新时不再闪烁“新消息”徽章。
- Tools/web_search：在搜索缓存 key 中加入 provider 设置，并为 Grok 传递 inlineCitations。（#12419）感谢 @tmchow。
- Tools/web_search：归一化 Perplexity 的模型 ID，OpenRouter 保持不变。（#12795）感谢 @cdorsey。
- Model failover：HTTP 400 也参与故障切换，自动降级模型更聪明。（#1879）感谢 @orenyomtov。
- Errors：避免在对话提到“context overflow”时触发误判。（#2078）感谢 @sbking。
- Gateway：压缩后不再“失忆”，注入的 transcript 保留 Pi 会话 parentId 链。（#12283）感谢 @Takhoffman。
- Gateway：修复多代理会话的使用统计发现。（#11523）感谢 @Takhoffman。
- Agents：处理过大工具结果导致的上下文溢出（预先限幅 + 备用截断）。（#11579）感谢 @tyler6204。
- Subagents/compaction：稳定广播时机并跨重试保留压缩指标。（#11664）感谢 @tyler6204。
- Cron：分享隔离广播流程，强化调度/投递可靠性。（#11641）感谢 @tyler6204。
- Cron 工具：当 LLM 省略 add payload 封装时恢复扁平参数。（#12124）感谢 @tyler6204。
- Gateway/CLI：`gateway.bind=lan` 时使用 LAN IP 作为探测 URL 和控制 UI 链接。（#11448）感谢 @AnonO6。
- Hooks：修复自 2026.2.2 起因 tsdown 迁移损坏的内置 hook。（#9295）感谢 @patrickshao。
- Routing：按消息刷新绑定时重新加载配置，绑定变更无需重启即可生效。（#11372）感谢 @juanpablodlc。
- Exec approvals：将转发命令以等宽字呈现，方便安全审核。（#11937）感谢 @sebslight。
- Config：把 `maxTokens` 限制在 `contextWindow` 内，防止非法模型配置。（#5516）感谢 @lailoo。
- Thinking：为 github-copilot/gpt-5.2-codex、github-copilot/gpt-5.2 允许 `xhigh` 强度。（#11646）感谢 @LatencyTDH。
- Discord：支持 forum/media 线程创建消息、关联 message_thread_create 参数、强化路由。 (#10062) 感谢 @jarvis89757。
- Paths：让 `OPENCLAW_HOME` 推导的路径结构更稳健，并修复 Windows 驱动器字母在 tool meta 缩短时的处理。（#12125）感谢 @mcaxtr。
- Memory：设置 Voyage embeddings 的 `input_type` 以提升检索质量。（#10818）感谢 @mcinteerj。
- Memory/QMD：跨 agent 重用默认模型缓存，避免重复下载。（#12114）感谢 @tyler6204。
- 媒体理解：识别 `.caf` 音频附件用于转录。（#10982）感谢 @succ985。
- 状态目录：尊重 `OPENCLAW_STATE_DIR`，用于默认设备标识与画布存储路径。（#4824）感谢 @kossoy。
