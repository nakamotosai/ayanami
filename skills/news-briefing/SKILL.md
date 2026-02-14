---
name: news-briefing
description: Generate Chinese news briefings from Japanese and global RSS sources with category grouping, Telegram-friendly formatting, and optional ranking logic. Use when user asks for today's hot news, top N news, category-based summaries (society/politics/international/economy/lifestyle/entertainment/sports/AI/crypto), or requests reformatting of news digests for Telegram readability.
---

# News Briefing Skill

Use this skill to produce repeatable, source-backed news digests.

## Workflow

1. Run the fetch script to collect and rank items.
2. Translate titles into Chinese.
3. Add concise interpretations (1-3 sentences each).
4. Output in Telegram-friendly layout.

## Command

```bash
python3 skills/news-briefing/scripts/fetch_news.py --top 20 --region jp
```

Optional:

```bash
python3 skills/news-briefing/scripts/fetch_news.py --top 10 --region jp --format json
```

## Output Rules

- Default language: Chinese.
- Keep category headers with emoji.
- For Telegram readability:
  - category header line
  - separator line `•`
  - each item as: `序号. **标题**` then one-line interpretation
  - use `-` as a standalone line between items
- If user asks “only formatting changes”, do not re-fetch; only re-render existing content.

## Category Set

Use these categories when possible:

- 社会新闻
- 日本政局
- 国际关系
- 经济
- 在日生活
- 娱乐
- 体育
- AI/科技
- 币圈/金融科技

If there are insufficient high-confidence items in a category, note that briefly and continue with available categories.

## Hotness Heuristic

Treat “hot” as a proxy score using:

- cross-source repetition
- channel prominence (top/general > niche)
- recency (earlier ranks in feed)

Do not claim official nationwide click ranking unless the source explicitly provides it.
