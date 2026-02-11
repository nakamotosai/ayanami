---
name: codex-podcastfy
description: "Generate podcast-style summaries (MP3 + transcript) from URLs using local Codex CLI instead of Gemini. Use when the user wants to turn an article/video/PDF link into a listening-friendly audio recap."
---

# Codex Podcastfy

## What it does
1. Fetches the HTML/text of the provided URL(s) and strips boilerplate with BeautifulSoup.
2. Calls `codex exec` (model configurable via `CODEX_MODEL`) to rewrite the material into a host/guest dialogue plus three highlight bullets.
3. Uses Edge TTS to render the transcript into an MP3 saved under `output/audio/`, while transcripts land in `output/transcripts/`.

## When to use
- You want a podcast-style digest of one or more links without provisioning a Gemini API key.
- You need both the raw transcript (for editing or publishing) and a polished MP3 ready to share or forward via Telegram.
- The content is conversational; the skill even supports a `--longform` switch for deeper dives.

## Setup (one-time)
```bash
python3 -m pip install --user requests beautifulsoup4 edge-tts
sudo apt-get install -y ffmpeg  # Edge TTS already writes MP3, but ffmpeg keeps options open
```
Ensure `codex` is logged in and `CODEX_MODEL` (e.g., `openai-codex/gpt-5.1-codex-mini`) points to an accessible model. The skill ships with its own `.venv`—activate it (`source .venv/bin/activate`) or call the bundled interpreter to keep dependencies isolated.

## Usage
```bash
cd ~/.openclaw/workspace/skills/codex-podcastfy
source .venv/bin/activate          # optional, or use .venv/bin/python directly
CODEX_MODEL=openai-codex/gpt-5.1-codex-mini .venv/bin/python scripts/codex_podcastfy.py --url "https://example.com/article"
```
Optional flags:
- `--url` (repeatable)
- `--voice` (Edge TTS voice, default `en-US-JennyNeural`)
- `--longform` (asks Codex for a lengthier script)
- `--output-dir` (override default `output/` root)

After running it prints where the MP3 and transcript live; you can then send the MP3 via Telegram or upload elsewhere.
