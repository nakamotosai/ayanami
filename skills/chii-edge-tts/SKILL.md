---
name: chii-edge-tts
description: Generate cute female-voice TTS on the VPS with Edge TTS and send it as a Telegram voice-note (sendVoice) bubble instead of a raw MP3 attachment. Use when the user asks for “语音说/用语音回/读出来/发语音”, wants a quick TTS test, or the reply should sound like a warm girlfriend whisper.
---

# Chii Edge TTS（voice-note 专用工作流）

## Goal
把主人想说的 1–3 句话：
1. 用 Edge TTS 生成音频，
2. 转成 Telegram 喜欢的 Opus/OGG 格式，
3. 直接调用 Telegram Bot 的 `sendVoice` 让消息出现成 “语音气泡”。

## Defaults
- Engine：Edge TTS（`/home/ubuntu/.openclaw/venv/edge-tts/bin/edge-tts`）
- 默认 voice：`zh-CN-XiaoxiaoNeural`
- 临时目录：`/tmp/chii-tts`
- Telegram chat：`8138445887`
- 发送方法：`sendVoice`（voice bubble）

## Workflow（只需要一条命令）
1. 在文本里写好想说的话（甘草般软糯、少用 emoji）。
2. 运行：
   ```bash
   bash scripts/send_voice_note.sh "早安主人，今早的日本热点和备份都好了。想先做哪件事？"
   ```
   这个脚本会：
   - 调用 `scripts/gen_mp3.sh` 生成 MP3。 
   - 用 `ffmpeg` 转成 Opus/OGG（Telegram 语音笔记要求的格式）。
   - 读取 `/home/ubuntu/.openclaw/openclaw.json` 里的 `channels.telegram.botToken`（或 `CHII_TTS_TELEGRAM_TOKEN` 环境变量），
   - 通过 `curl` 调用 `https://api.telegram.org/bot<TOKEN>/sendVoice` 发送语音气泡，执行完成后会删除中间文件并在控制台打印 `voice note sent` 以及 telegram 背后返回的 `message_id`。

3. 如果你想先单独审查 MP3 或手动传 `MEDIA:` 给主会话，也可以：
   - 生成音频：
     ```bash
     bash scripts/gen_mp3.sh --voice zh-CN-XiaoxiaoNeural --text "..."
     ```
   - 验证：
     ```bash
     bash scripts/check_file.sh /tmp/chii-tts/chii_20260206T001903Z.mp3
     ```
   - 再用 `message` tool 附件形式发给主人，若要语音气泡请在输出里加 `[[audio_as_voice]]` 或直接用 `scripts/send_voice_note.sh`。

## 可选变量
| 环境变量 | 说明 |
| --- | --- |
| `CHII_TTS_VOICE` | 覆盖 Edge TTS voice id（默认 `zh-CN-XiaoxiaoNeural`） |
| `CHII_TTS_OUT_DIR` | 输出目录，默认 `/tmp/chii-tts` |
| `CHII_TTS_OPUS_BITRATE` | `ffmpeg` 转码比特率（默认为 `64k`，Telegram 推荐 32–64kbps） |
| `CHII_TTS_TELEGRAM_TARGET` | Telegram chat id（默认 8138445887） |
| `CHII_TTS_TELEGRAM_TOKEN` | 直接提供 Bot token（覆盖 `openclaw.json`） |
| `CHII_TTS_CAPTION` | sendVoice 的 `caption` 字段（脚本会自动加 `parse_mode=HTML`），默认无 |
| `CHII_TTS_CONFIG_PATH` | 指定 OpenClaw config 路径（默认 `/home/ubuntu/.openclaw/openclaw.json`） |

## Safety & quality
- 语音必须用 [voice note bubble](https://core.telegram.org/bots/api#sendvoice) 发送；脚本自动转成 OGG+Opus，并调用 `sendVoice`。
- 如果生成或发送失败，它会立刻退出并打印错误（`set -euo pipefail` + `python3` 校验 JSON 结果）。
- 语音尽量保持 1–3 句（<10 秒），避免长段落或所有句子都加 emoji。

## Voice palette
需要更多 voice 可选项请看 `references/voices.md`。
