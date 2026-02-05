---
name: chii-edge-tts
description: Generate cute female-voice TTS audio on the VPS using Microsoft Edge TTS (edge-tts) and send it to the user as a playable Telegram audio/voice attachment. Use when the user asks for “语音说/用语音回/读出来/发语音”, wants a TTS test, or when the agent should reply with audio in a cute girlfriend voice.
---

# Chii Edge TTS（语音回复工作流）

## Goal

Turn a text reply into a **playable** Telegram audio message by:
1) generating an mp3 on the VPS with Edge TTS, then
2) sending that mp3 as Telegram media (not as a local path string).

## Defaults

- Engine: Edge TTS (`edge-tts`)
- Venv: `/home/ubuntu/.openclaw/venv/edge-tts`
- Default voice (female): `zh-CN-XiaoxiaoNeural`
- Output dir: `/tmp/chii-tts`

## Workflow (do this every time)

1) **Compose the exact text** you want to speak (keep it short; 1–3 sentences).
2) **Generate mp3**:
   - `bash scripts/gen_mp3.sh --voice zh-CN-XiaoxiaoNeural --text "..."`
   - It prints the mp3 path.
3) **Validate file is non-empty**:
   - `bash scripts/check_file.sh <mp3>`
4) **Send to Telegram** using the `message` tool:
   - `action=send`, `channel=telegram`, `target=<owner id>`, `media=<mp3>`, `filename=chii-voice.mp3`

### Safety/quality rules

- Never send `MEDIA:/tmp/...` as plain text to the user.
- If mp3 is empty or generation fails: say so, then retry once; if still failing, stop and report error.
- Use cute, warm tone; no emojis unless the owner wants them.

## Voice palette

See `references/voices.md` for recommended female voices.
