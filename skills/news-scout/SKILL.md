---
name: news-scout
description: Fetch trending headlines from SearXNG in any language (Japanese/English/Chinese/etc.), translate the resulting summaries into Chinese, and present them in a clean multi-section format. Trigger this skill when the user asks for real-time news pulled with native-language keywords and expects a Chinese explanation.
---

# News Scout

## Overview
Use this skill whenever you need a repeatable, multilingual news sprint:
1. Issue a search in the target language (e.g., Japanese keywords for Japanese news, English keywords for US/English coverage, etc.).
2. Run `scripts/news_fetch.py` to call the local SearXNG instance, capture the top headlines, and automatically translate the titles/descriptions into Chinese.
3. Format the output into themed sections (politics / economy / society & weather / culture & sports) with spacing so the user gets a polished digest.

## Quick Start
- Ensure `SEARXNG_URL` is set (e.g., `export SEARXNG_URL=http://127.0.0.1:8765`).
- Run: `python3 scripts/news_fetch.py "日本 今日 最新 ニュース" -l ja --count 10`.
- The script returns JSON with Chinese translations. Build a response by organizing those results into sections, translating the query intent back to Chinese where needed, and labeling the source and timestamp.

## Workflow
1. **Select language-specific keywords.** Always search in the native language for the content you want (Japanese for Japan, English for global/US, Chinese for mainland/Taiwan). Mention the language in your reply so the user knows why that keyword set was chosen.
2. **Fetch + translate.** Use `scripts/news_fetch.py` with appropriate `--language` flag, and leave translation enabled (default). Optional: use `--source-lang` if the source language is known and you want to tighten translation accuracy.
3. **Structure output.** Group results into the requested thematic sections, include the headline, a translated summary, the origin (engine/source), and the URL. Leave a blank line between bullet points for readability; keep the entire response in Chinese.
4. **Supplement and finalize.** Mention any translation fallbacks (e.g., “部分标题来自英文，已自动翻译为中文”) and offer to pull additional sections (finance, tech, etc.) if the user wants more.

## Formatting Guidelines
- Always output Chinese, even if the search keywords were Japanese or English.
- Provide context at the top of each section (e.g., “政治类（NHK、读卖）” or “经济类（Asahi、Nikkei）”).
- Include the query and timestamp for transparency.
- Keep results concise (headline + 1–2 sentence summary + source + link) with blank lines between entries.

## Resources
- `scripts/news_fetch.py`: Core automation to query SearXNG, gather top results, translate to Chinese via Google Translate, and emit JSON that includes the query, language, and suggestions.

When interpreting the JSON output, translate whatever additional context is necessary and reassemble it into the desired sections before replying to the user.
