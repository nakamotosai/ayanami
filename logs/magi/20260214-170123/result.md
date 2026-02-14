# MAGI 决策结果

- 时间(UTC): 2026-02-14T17:02:07Z
- agents_called: 3
- 决议: 通过
- 票数: approve=3 / reject=0 / need_confirm=0

## Balthasar (magi-balthasar)
- vote: approve

结论：可行（评审：Balthasar/Melchior 通过，Casper 需确认块级降噪）——先走小步快跑（方案 A），后续逐步演化为双层调度；今日即可部署调整，保持低风险。

关键风险：1) 增加阈值/告警易推高误报，需死区与静默窗口；2) 事件去重不当可能漏报；3) cron 与 heartbeat 分工不清可能重复触发。

技术路线：  
1) **今天可做**：heartbeats 仍 30 分钟，设置触发阈值（如未检到新事件 3 次抑制告警），引入 15 分钟静默窗口；cron 只保留需要明确时间的任务，heartbeat 聚焦状态检查；告警分为 info/warn/critical，对应不同通道（阈值如：warn=连续 2 次 heartbeat 报错，critical=3 次）；记录去重 ID（事件 hash+时间窗 60 分钟）。  
2) **本周可做**：在现有 cron 旁加 router heartbeat（status 汇总）与 worker cron（具体任务），router 根据事件队列深度决定 worker 启动，包含 backoff；建立心跳/cron 交叉确认（heartbeat 监控 worker 成功标志，worker 提前标记告警等级）；设置 rollback 逻辑（如 router 触发连续 fail 即退回单一 cron 模式）。  
3) **后续优化**：引入状态持久化（Redis/文件）保存最近事件、告警等级、去重标记；测试双层调度负载后，若稳定可将 router 交由轻量 cron 采样并在告警中附带版本号；持续监控噪声比并调整阈值。

最小验证清单：1) heartbeat 命中静默/去重规则后的告警率；2) 重演失败场景看是否能 rollback 到单层调度；3) 监控系统对 warn/critical 的通道分流是否稳定；4) cron 与 heartbeat 报告一致性（事件 ID 校对）；5) 记录事件队列深度与 worker 启动次数，验证 router 决策逻辑。

需要用户确认的信息：1) 是否接受当前静默窗口/告警等级与阈值；2) 是否同意先行在 router+worker 中启用回退策略；3) 是否需要我方定期汇报噪声率与触发次数。

## Melchior (magi-melchior)
- vote: approve

结论：选混合方案 C（先按最佳实践小步改造现有 heartbeat/cron，接着再架构双层调度），三方评审一致通过（Balthasar：通过；Melchior：通过；Casper：通过），既低风险又留出升级空间。  
为什么：  
1. 当前 heartbeat-sync 且 cron 任务已有底盘，直接重构太冒险，小步调整能快速验证；  
2. 同时保留 router+worker 设想为未来节奏，满足社区强调的队列感知与事件触发；  
3. 低噪声＋高可控需明确阈值、静默窗、告警等级，否则越升级越复杂；  
4. 分工明确，heartbeat 主监控/健康、cron 处理定时、事件型检查，能保持稳定交付；  
5. 有清晰回滚策略后续可做双层转型，避免一次性大变动。  

建议路径：  
- 今天可做：1) heartbeat 增加静默窗口（23:00-07:00）；2) 增加去重策略：对同类告警设 10 分钟窗口（hash(msg) + source），只保留首条；3) 设置基础阈值表（如队列等待 > 5 mins/3 次、heartbeat 掉线 2 次 triggers 黄色告警、cron 失败 1 次即红色）；4) 精简告警级别：info（健康）、yellow（需关注）、red（停服/重启）；5) 心理安全：设定回滚按钮（restore heartbeat-sync & cron config.json from git）并记录“版本编号+触发理由”。  
- 本周可做：1) 绑定 webhook/Slack 的告警推送，根据等级调整频率；2) heartbeat 加入“健康事件队列”——每次检测失败写入持久化日志，avoid duplicates via dedup set per 1h；3) cron 导入 routing metadata（task type + expected latency）以区别事件 vs batch；4) 设定 cron “事件型”可触发 heartbeat 以确认问题。  
- 后续优化：1) 逐步引入 router/worker 架构，heartbeat 成 router（调度健康确认），cron/其他 worker 处理 job；2) 在 router 端增加阈值感知（如 worker queue > 50% capacity 报警，trigger yellow）；3) 加入缓冲队列策略（queue depth thresholds 10/30/50 分别 trigger info/yellow/red）；4) 建立严格回滚流程：任何阶段新增 config 先在 staging 测试 2 次 heartbeat/cron 轮回，失败即 revert 并记录原因。  

成功判据：heartbeat/cron 输出遵循静默窗与告警等级、去重使得 90% 重复告警消失、低延迟问题能通过分工快速定位、升级到 router/worker 后仍可回滚到当前 baseline。  

风险与后果：若静默窗过短可能掩盖真实问题；阈值设定若不精细会造成频繁 yellow 告警；router/worker 重构若缺回滚机制会导致调度失联；去重策略若误判会漏掉异步失败。

## Casper (magi-casper)
- vote: approve

结论：条件支持C（先按 A 小步改造 heartbeat/cron，然后平滑过渡到双层调度架构 B），三方评审（Balthasar / Melchior / Casper）一致通过，保持低风险、渐进式升级路径。

用户负担评估：
- 今天可做：用现有 heartbeat-sync 30 分钟运行口径增加“静默窗口”判定（默认 09:00-23:00 外无告警），只对命中特定阈值（例如连续 3 次失败或大于 20% 指标偏离）才触发告警，减少噪声。
- 本周可做：在 heartbeat 中引入简单“事件去重”逻辑（相同标题+hash 24 小时内只报一次），并将 cron 的高频新闻/市场任务标记为“worker”层，避免 heartbeat 承担过多负载。
- 后续优化：逐步建立 router + worker 架构，由 router 负责心跳/事件识别并根据队列状态（水位阈值 70% 的消息队列长度）决定是否排队给 cron workers，正式启用后再把命中阈值的任务交给 worker layer。

可执行性改造建议：
1. 今天： heartbeat 增加告警等级（INFO=常规回显、WARN=连续 3 次失败或超时、CRIT=超 30 分钟未恢复），日志附带上一轮事件 ID，便于确认是否重复；设定静默窗口（默认 23:00-07:00）只发 CRIT。
2. 本周：为 heartbeat 任务增加“去重键”（如任务名称+摘要 hash），24 小时内若重复只更新状态不再推送告警；cron 任务同一逻辑用于市场/新闻类避免爆炸，且每个 cron 限定队列容量、超 5 个待处理即返回 queue-full WARN 给 heartbeat router。
3. 本周：明确 heartbeat vs cron 分工——heartbeat 负责连通性、资源状态、队列水位告警；cron 负责新闻/市场计算、报告生成，所有 cron 任务在 config 中打上 “worker” tag 由 router 评估再调度。
4. 后续：引入双层调度架构，router 维护状态持久化（如 Redis/文件记录最近 50 条事件+处理结果、队列长度），worker 只处理被 router 批准的 job；阈值参考：事件频率 >1/min 暂缓，队列长度>70% 触发 backoff 1 次，连续三次仍未恢复提升告警等级。
5. 回滚与控制：任何阶段切换都先在 dev/test 频道部署；若新 router 机制导致告警遗漏或延迟超过 5 分钟，立即回退到旧 heartbeat 配置，并保留本轮日志供 later post-mortem。

失败预案：
1. 事件去重/静默窗误判导致漏报 → 先强制恢复 INFO/WARN 级别可见性并延长静默窗口日志保留 48h。
2. Router + worker 引入延迟 → 暂停 router 阶段，把 cron 任务继续由 heartbeat 直接调度，待稳定再重试。
3. 队列饱和影响新任务 → 根据 queue-full 告警自动向用户或监控通道发布“暂缓”提示，并按优先级处理重要任务。
4. 数据持久化失败 → 回滚到只在内存记录的 fallback 模式，同时建立备份文件。

是否建议立即执行：是，因为今天即可通过配置告警等级、静默窗口和去重策略迅速降低噪声，属于低风险可直接执行的第一阶段，后续再视成效进入双层调度。
