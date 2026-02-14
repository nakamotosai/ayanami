# polymarket 套利 深度学习完整报告

生成时间(UTC)：2026-02-14T13:59:49Z

## 目录
- 1. 总览
- 2. 核心概念与机制
- 3. 交易与市场结构
- 4. 套利与策略（含风险与边界）
- 5. 风险管理与常见坑
- 6. 自测题与错题集
- 7. 术语表
- 8. 未解问题清单
- 9. 来源索引

## 1. 总览
本报告来自多轮循环学习过程沉淀的知识库，目标是‘不精简’，尽可能完整覆盖。

## 2-7. 知识库（逐步沉淀）

# KB (polymarket 套利)

## 架构与市场机制
- Polymarket 构建在 Polygon 上，采用链下撮合 + 链上结算、配合 Gnosis Conditional Token Framework（CTF）的混合架构，从微观结构角度导出二元市场与“负风险市场”之间的确定性套利不等式；这种架构让专门开发套利逻辑的团队每月能悄悄稳定拿到 1 万、5 万甚至超过 20 万美元的收益。 (Round 1 Source 1)
- 平台在 UMA 与 Polygon 基础设施上搭建，事件的“YES/NO”股份价格区间限定在 0～1 美元，成功的套利者依靠复杂的二元/组合套利与规则化的数据驱动策略来挖掘市场非效率，把握多市场组合带来的阿尔法。 (Round 1 Source 2)
- 虽然结算时 YES + NO 总价必然趋近于 1 美元，但在实际行情中两边价差不等于 1 就形成价差耕作机会；据说相关套利/价差耕作的风险占比低于 5%，年化收益约 10%～20%。 (Round 1 Source 5)

## 套利玩法与工具
- 跨平台套利的经典套路是监控 Polymarket 与 Kalshi 等平台对同一事件的隐含概率，当两者出现分歧时在一端买“YES”、另一端买“NO”，等待概率收敛；该策略实质上是合成套利，执行简单但依赖低延迟监控。 (Round 1 Source 6)
- 当某个市场只有 YES 侧流动性时（NO 较少或已清空），量化策略必须限制仓位以避免单边风险；当两边都有流动性时，持有 YES+NO 等价于“合成现金”，此时可以放宽仓位限制，并叠加 Maker Rebate 计划带来的额外收益。 (Round 1 Source 7)
- 做市商与套利者最常利用“买入 NO”策略，尤其政治类市场贡献了绝大部分已实现利润，而体育类市场目前仍是尚未充分开发的空间。 (Round 1 Source 8)
- 还有一类多事件组合套保，比如一边押 Kamala Harris 赢、一边押共和党在选举人团的所有胜选差距，当这两类头寸总价低于 1 美元时，差值部分就是可以锁定的无风险收益率，实盘案例曾宣称能达到约 40% 年化。 (Round 1 Source 10)
- 现成的开源工具 FKPolyTools 提供 scanMarkets()、实时监控、跟单与聪明钱追踪等功能，帮助开发者自动化发现并监控套利机会。 (Round 1 Source 4)
- Polymarket 做市商入门指南披露了 API 实现、六大核心盈利策略、风险管理流程以及实战操作细节，是搭建自动化套利/做市系统的重要参考。 (Round 1 Source 9)
- 由于平台对 YES+NO 组合的 $1 保证赎回机制，一旦集合价格低于 1 美元，就有 $1 - 当前总价 的套利空间；这种 Dutch Book 式的定价约束也迫使市场在无套利空间时形成强均衡。 (Round 1 Source 11)

## 风控与常见坑
- 虽然套利机会诱人，但它们通常会被快速关闭；大量人同时盯着同一个事件，价格一旦同步向着真实概率收敛，就可能出现两边同时亏损的场景，说明必须提前设定出场条件和头寸限制。 (Round 1 Source 3)

## 8. 未解问题清单

# Questions (polymarket 套利)

1. 如何结合 Polymarket 的 CTF 架构与链下撮合、链上结算的混合模式，具体推导出二元市场与负风险市场之间的套利不等式与其参数范围？ (Round 1 Source 1)
2. Maker Rebate 计划的触发条件、奖励比例和时间窗口具体如何设定，实际做市中如何与已有套利/组合仓位配合？ (Round 1 Source 7)
3. 多市场交易/数据驱动套利通常用哪几类信号（事件类型、成交量、价差或其他）去筛选那些 YES/NO 总价偏离 1 的机会？ (Round 1 Source 2)
4. 进行 Kalshi 与 Polymarket 的跨平台套利时，有哪些跨管辖区的合规要求或限制需要预先明确，尤其涉及美国监管平台 Kalshi 的开户与下单规则？ (Round 1 Source 6)

## 9. 来源索引

# Sources (polymarket 套利)

\n## Round 1
- queries: polymarket 套利 基础 入门 机制 术语 市场 交易
- queries: polymarket 套利 套利 arbitrage spread 对冲 交易策略 风险
- queries: polymarket 套利 site:twitter.com (arbitrage OR 套利 OR strategy OR 风险 OR 对冲)
- queries: polymarket 套利 site:x.com (arbitrage OR 套利 OR strategy OR 风险 OR 对冲)
- queries: Polymarket liquidation fees spread market making risk management
- urls:
-
https://zhuanlan.zhihu.com/p/1989016130568860070
-
https://www.datawallet.com/zh/%E9%9A%90%E8%94%BD%E6%80%A7/top-polymarket-trading-strategies
-
https://cn.investing.com/analysis/article-200488555
-
https://github.com/duzhi5368/FKPolyTools
