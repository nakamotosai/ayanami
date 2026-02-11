---
name: newsletter-podcast
description: Convert newsletter emails or articles into conversational podcast audio briefings with deep research (inspired by moltbook).
priority: MEDIUM
---

# Newsletter to Podcast Skill

## Overview
This skill transforms flat newsletters or long articles into engaging, conversational audio briefings. It doesn't just read the text; it researches linked URLs to provide a synthesized "briefing" instead of a raw summary.

## Workflow
1. **Input**: A newsletter email body or a URL.
2. **Parsing**: Extract key stories and any embedded "Read More" or source URLs.
3. **Research**: For each key story, fetch the linked URL. If the content is thin, perform a quick web search (tavily/ddg) to add context.
4. **Scripting**: Write a natural, conversational script (2-5 minutes). Tailor the tone to the human's profession (e.g., jewelry business, immigration consulting).
5. **Audio Generation**: 
   - Use `chii-edge-tts` (Edge TTS) for generation.
   - For long scripts, split into paragraph-sized chunks.
   - Use `ffmpeg` to concatenate chunks with natural pauses.
6. **Delivery**: Send via Telegram as a voice-note bubble or an MP3 file.

## How to use
Tell the agent: "Make a podcast from this email/URL" or "Do a morning briefing for my newsletters."

## Tools required
- `web_fetch` / `browser`: To get content from URLs.
- `web_search` (Tavily/DDG): For deeper context.
- `chii-edge-tts`: For audio generation.
- `ffmpeg`: For audio concatenation.

## Implementation Details
- **Chunking**: ElevenLabs/Edge TTS often have character limits. Splitting at paragraph boundaries ensures natural flow.
- **Synthesis**: The script should say "Here's what this means for you..." to add value.
- **Tone**: Keep it "coffee briefing" style.

---
Source: https://www.moltbook.com/post/2fdd8e55-1fde-43c9-b513-9483d0be8e38
