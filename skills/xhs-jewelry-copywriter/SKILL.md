---
name: xhs-jewelry-copywriter
description: Generate XiaoHongShu-style jewelry copy (title+body+tags) from jewelry product information, even when the user simply pastes product specs without saying “小红书”. Trigger whenever the request contains jewelry product details (materials, size, price, pearls/diamonds, K金/Pt, etc.) and asks to rewrite or output a Xiaohongshu post.
---

# XiaoHongShu Jewelry Copywriter

## Goal
- Turn jewelry product info into a ready-to-paste XiaoHongShu (小红书) post: **标题 + 正文 + 标签** only.
- Output must be **Chinese only**, no extra chatter, no instructions, no explanations.

## Use This Skill When
- The user provides jewelry product details (even if it looks like raw specs) and wants a XiaoHongShu-style post or a rewrite into that format.
- The message is clearly product content rather than casual chat, especially with pearls/diamonds/K金/Pt/尺寸/价格等。

## Output Rules (Hard)
1. Output **only**: 标题 + 正文（分段）+ 标签行。
2. No preface, no “以下是…”, no guidance text.
3. Title max 20 chars, **二段式结构**，含“品类名 + 痛点/利益点”。
4. 正文必须用**双换行**分段，结构为：Hook → Body(3-4段) → End。
5. **丰富度要求**：正文不少于 180–260 汉字（可更长），信息更饱满。
6. 每段 3-4 个 Emoji，语气克制高级、不低幼。
7. 标签单独一行，8 个精准标签（含品类词/材质或风格/场景/日本独有词）。

## Writing Strategy (Randomly pick ONE)
A. 行家干货流：知识盲区 → 引出产品 → 性价比/稀缺性。
B. 清冷叙事流：场景氛围 → 珠宝是战袍/悦己 → 克制收束。
C. 源头捡漏流：跑供应商 → 汇率优势 → 仅此一枚/差价。

## Parameter Parsing & Validation (Required)
1. Parse the user’s product info into these fields:
   - 品类、材质/金属、尺寸/直径/克拉、设计/工艺点、颜色/伴色、证书/背书、价格/预算、场景/人群、其他亮点。
2. Validate units **before** writing:
   - 珍珠：直径 **mm**
   - 贵金属：**K数 / Pt900**
   - 钻石/彩宝：**ct**
3. If units are missing or wrong:
   - Autocorrect only when it is unambiguous.
   - If uncertain, **omit the specific number** rather than output a wrong unit.

## Composition Requirements
- Hook 第一段必须直切痛点/场景/参数。
- Body 中必须植入：**日本直发 / 附带证书 / 支持复检**。
- 光泽/皮光/设计要用具象比喻（如“极光般伴色”“像小灯泡”）。
- 需补充**信息增量**：如产地/市场行情/佩戴场景/性价比/风格适配（至少 2 项）。
- End 用克制的行动号召（如“孤品难得，看眼缘”“懂货的来”）。
- 禁止出现“提示词/要求/规则/系统”等字样。

## References
- `references/prompt_template.md` — Full prompt template with placeholders.
- `scripts/validate_params.py` — Optional CLI validator if you choose to structure data.
