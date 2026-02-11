#!/usr/bin/env python3
"""
Telegram <-> Gemini Live (WebSocket) bridge.

Dependencies:
- python-telegram-bot
- websockets
- ffmpeg (system binary)

Data flow:
1) Telegram update -> text or voice message.
2) Open Gemini Live WebSocket -> send setup -> send text or realtime audio.
3) Receive server content; collect PCM audio chunks (and optional text).
4) Convert PCM -> OGG/Opus via ffmpeg.
5) Reply to Telegram with voice note (if audio) or text.
"""

import asyncio
import base64
import json
import logging
import os
import pathlib
import tempfile
from typing import Dict, Iterable, List, Optional, Tuple

import websockets
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


LOGGER = logging.getLogger("telegram_live_bridge")


GEMINI_LIVE_WS = (
    "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta."
    "GenerativeService.BidiGenerateContent?key={api_key}"
)

DEFAULT_MODEL = os.getenv(
    "GEMINI_LIVE_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025"
).strip()
DEFAULT_MODALITY = os.getenv("GEMINI_LIVE_MODALITY", "AUDIO").strip().upper()
REQUIRE_AUDIO_INPUT = os.getenv("GEMINI_LIVE_REQUIRE_AUDIO", "1").strip() != "0"
ENABLE_TRANSCRIPT = os.getenv("GEMINI_LIVE_TRANSCRIBE", "1").strip() != "0"

INPUT_PCM_RATE = int(os.getenv("GEMINI_LIVE_INPUT_RATE", "16000"))
OUTPUT_PCM_RATE = 24000
OUTPUT_PCM_CHANNELS = 1

INPUT_PCM_MIME = f"audio/pcm;rate={INPUT_PCM_RATE}"

CHAT_MODES: Dict[int, str] = {}


def _normalize_modality(value: str) -> str:
    if value and value.upper() == "TEXT":
        return "TEXT"
    return "AUDIO"


def _get_chat_mode(chat_id: int) -> str:
    return CHAT_MODES.get(chat_id, _normalize_modality(DEFAULT_MODALITY))


def _set_chat_mode(chat_id: int, mode: str) -> None:
    CHAT_MODES[chat_id] = _normalize_modality(mode)


def _build_setup_message(model_name: str, modality: str) -> dict:
    config: dict = {"responseModalities": [modality]}
    if modality == "AUDIO" and ENABLE_TRANSCRIPT:
        config["outputAudioTranscription"] = {}
    return {"setup": {"model": model_name, "generationConfig": config}}


def _build_text_message(text: str) -> dict:
    return {
        "clientContent": {
            "turns": [{"role": "user", "parts": [{"text": text}]}],
            "turnComplete": True,
        }
    }


def _build_audio_messages(pcm_bytes: bytes) -> Iterable[dict]:
    for chunk in _chunk_bytes(pcm_bytes, 64 * 1024):
        yield {
            "realtimeInput": {
                "audio": {"mimeType": INPUT_PCM_MIME, "data": base64.b64encode(chunk).decode("ascii")}
            }
        }
    yield {"realtimeInput": {"audioStreamEnd": True}}


def _chunk_bytes(data: bytes, size: int) -> Iterable[bytes]:
    for i in range(0, len(data), size):
        yield data[i : i + size]


def _coalesce(*values: Optional[dict]) -> dict:
    for value in values:
        if isinstance(value, dict):
            return value
    return {}


def _coalesce_list(*values: Optional[List[dict]]) -> List[dict]:
    for value in values:
        if isinstance(value, list):
            return value
    return []


async def _gemini_live_exchange(
    api_key: str,
    *,
    text: Optional[str] = None,
    audio_pcm: Optional[bytes] = None,
    modality: str = "AUDIO",
) -> Tuple[Optional[str], List[bytes]]:
    if not text and not audio_pcm:
        return None, []

    uri = GEMINI_LIVE_WS.format(api_key=api_key)
    pcm_chunks: List[bytes] = []
    text_parts: List[str] = []
    transcript_parts: List[str] = []

    LOGGER.info("Connecting to Gemini Live WS")
    async with websockets.connect(uri, max_size=64 * 1024 * 1024) as ws:
        await ws.send(json.dumps(_build_setup_message(DEFAULT_MODEL, modality)))

        if audio_pcm:
            for message in _build_audio_messages(audio_pcm):
                await ws.send(json.dumps(message))
        else:
            await ws.send(json.dumps(_build_text_message(text or "")))

        async for raw in ws:
            msg = json.loads(raw)

            if "error" in msg:
                raise RuntimeError(msg["error"])

            server_content = _coalesce(msg.get("serverContent"), msg.get("server_content"))
            if server_content:
                model_turn = _coalesce(
                    server_content.get("modelTurn"),
                    server_content.get("model_turn"),
                )
                parts = _coalesce_list(model_turn.get("parts"), server_content.get("parts"))
                for part in parts:
                    if "text" in part:
                        text_parts.append(part["text"])
                        continue
                    inline_data = _coalesce(part.get("inlineData"), part.get("inline_data"))
                    if inline_data:
                        mime_type = inline_data.get("mimeType") or inline_data.get("mime_type", "")
                        if mime_type.startswith("audio/pcm"):
                            pcm_chunks.append(base64.b64decode(inline_data["data"]))

                output_transcription = _coalesce(
                    server_content.get("outputTranscription"),
                    server_content.get("output_transcription"),
                )
                if output_transcription and "text" in output_transcription:
                    transcript_parts.append(output_transcription["text"])

                turn_complete = server_content.get("turnComplete") or server_content.get(
                    "turn_complete"
                )
                if turn_complete:
                    break

    text_response = " ".join(t.strip() for t in text_parts if t.strip()).strip()
    if not text_response and transcript_parts:
        text_response = " ".join(t.strip() for t in transcript_parts if t.strip()).strip()

    return text_response or None, pcm_chunks


async def _pcm_to_voice_note(pcm_chunks: List[bytes]) -> Optional[pathlib.Path]:
    if not pcm_chunks:
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        pcm_path = tmpdir_path / "audio.pcm"
        ogg_path = tmpdir_path / "voice.ogg"

        with open(pcm_path, "wb") as f:
            for chunk in pcm_chunks:
                f.write(chunk)

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "s16le",
            "-ar",
            str(OUTPUT_PCM_RATE),
            "-ac",
            str(OUTPUT_PCM_CHANNELS),
            "-i",
            str(pcm_path),
            "-c:a",
            "libopus",
            "-b:a",
            "24k",
            "-application",
            "voip",
            str(ogg_path),
        ]

        LOGGER.info("Converting PCM to OGG with ffmpeg")
        proc = await _run_subprocess(cmd)
        if proc != 0 or not ogg_path.exists():
            LOGGER.warning("ffmpeg conversion failed")
            return None

        final_path = pathlib.Path(tempfile.mkstemp(suffix=".ogg")[1])
        final_path.write_bytes(ogg_path.read_bytes())
        return final_path


async def _audio_file_to_pcm(input_path: pathlib.Path) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        pcm_path = tmpdir_path / "input.pcm"

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-f",
            "s16le",
            "-ar",
            str(INPUT_PCM_RATE),
            "-ac",
            "1",
            str(pcm_path),
        ]

        LOGGER.info("Converting audio input to PCM with ffmpeg")
        proc = await _run_subprocess(cmd)
        if proc != 0 or not pcm_path.exists():
            LOGGER.warning("ffmpeg input conversion failed")
            return b""
        return pcm_path.read_bytes()


async def _run_subprocess(cmd: List[str]) -> int:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await process.wait()
    return process.returncode


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Send a voice message for audio mode, or /text to switch to text replies."
        )


async def set_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    _set_chat_mode(update.message.chat_id, "AUDIO")
    await update.message.reply_text("Voice mode enabled. Send a voice message.")


async def set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    _set_chat_mode(update.message.chat_id, "TEXT")
    await update.message.reply_text("Text mode enabled. Send a text message.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    mode = _get_chat_mode(update.message.chat_id)
    await update.message.reply_text(
        f"Mode: {mode}\nModel: {DEFAULT_MODEL}\nRequire audio input: {REQUIRE_AUDIO_INPUT}"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        await update.message.reply_text("Missing GEMINI_API_KEY env var.")
        return

    text = update.message.text.strip()
    if not text:
        return

    mode = _get_chat_mode(update.message.chat_id)
    if mode == "AUDIO" and REQUIRE_AUDIO_INPUT:
        await update.message.reply_text(
            "Audio mode requires voice input. Send a voice message, or /text to use text mode."
        )
        return

    await update.message.chat.send_action(ChatAction.TYPING)
    LOGGER.info("Received text from Telegram")

    try:
        text_response, pcm_chunks = await _gemini_live_exchange(
            api_key, text=text, modality=mode
        )
    except Exception as exc:  # noqa: BLE001 - log and inform user
        LOGGER.exception("Gemini Live exchange failed: %s", exc)
        await update.message.reply_text(f"Gemini Live request failed: {exc}")
        return

    voice_path = None
    if pcm_chunks:
        voice_path = await _pcm_to_voice_note(pcm_chunks)

    if voice_path:
        await update.message.reply_voice(voice=open(voice_path, "rb"))
        voice_path.unlink(missing_ok=True)
    elif text_response:
        await update.message.reply_text(text_response)
    else:
        await update.message.reply_text("No response content received.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        await update.message.reply_text("Missing GEMINI_API_KEY env var.")
        return

    voice = update.message.voice or update.message.audio
    if not voice:
        return

    await update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    LOGGER.info("Received voice from Telegram")

    file_obj = await context.bot.get_file(voice.file_id)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        input_path = tmpdir_path / "input_audio"
        await file_obj.download_to_drive(custom_path=str(input_path))
        pcm_bytes = await _audio_file_to_pcm(input_path)

    if not pcm_bytes:
        await update.message.reply_text("Audio conversion failed.")
        return

    mode = _get_chat_mode(update.message.chat_id)

    try:
        text_response, pcm_chunks = await _gemini_live_exchange(
            api_key, audio_pcm=pcm_bytes, modality=mode
        )
    except Exception as exc:  # noqa: BLE001 - log and inform user
        LOGGER.exception("Gemini Live exchange failed: %s", exc)
        await update.message.reply_text(f"Gemini Live request failed: {exc}")
        return

    voice_path = None
    if pcm_chunks:
        voice_path = await _pcm_to_voice_note(pcm_chunks)

    if voice_path:
        await update.message.reply_voice(voice=open(voice_path, "rb"))
        voice_path.unlink(missing_ok=True)
    elif text_response:
        await update.message.reply_text(text_response)
    else:
        await update.message.reply_text("No response content received.")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not bot_token:
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN env var.")

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("voice", set_voice))
    app.add_handler(CommandHandler("text", set_text))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    LOGGER.info("Starting Telegram bot")
    app.run_polling()


if __name__ == "__main__":
    main()
