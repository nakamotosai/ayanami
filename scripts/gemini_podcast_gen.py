#!/usr/bin/env python3
"""Gemini native podcast helper that stitches multi-voice clips with lofi beds."""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

BACKGROUND_URL = "https://www.bensound.com/bensound-music/bensound-littleidea.mp3"
CACHE_DIR = Path(__file__).parent / ".cache"
DEFAULT_SPEAKER_VOICES = {"Aoede": "Aoede", "Charon": "Charon"}
SAMPLE_SCRIPT = textwrap.dedent("""
Aoede: Welcome back to the Gemini native podcast studio, Charon. [sigh]
Charon: Always a pleasure, Aoede. Let us cue our lofi spark. [laugh]
Aoede: We'll lean into the storyteller energy while listeners chill with soft synths.
Charon: We'll tag emotions explicitly so the TTS knows when to breathe.
""")


class UsageError(Exception):
    pass


def create_parser():
    description = (
        """Generate a Gemini-native audio conversation that mixes speakers with a lofi bed.
Lines should be "Speaker: dialogue"; emotional fillers like [laugh], [sigh], and [breath] travel through unchanged.
You can reroute voices via repeated --speaker-voice arguments and drop in your own background track afterward."""
    )

    epilog = textwrap.dedent(
        """
Background mixing: downloads bensound-littleidea.mp3 once, loops it, and keeps the music ~10% volume while speech goes on top.
Multi-speaker flow: specify each speaker line, map names with --speaker-voice Speaker=GeminiVoice, and text is sent to Gemini-2.5-flash-preview-tts for WAVs.
Output formats: mp3 (libmp3lame) and/or opus (libopus) controlled with --output-format; files are saved under the specified directory.
Use --demo to run a built-in sample conversation that exercises Aoede, Charon, and laugh/sigh cues without needing a script file.
"""
    )

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--script-text",
        help="Inline script text (multiple lines separated by '\n'); speaker lines must be non-empty.",
    )
    source_group.add_argument("--script-file", help="Path to a script file with Speaker: line-by-line cues.")

    parser.add_argument(
        "--speaker-voice",
        action="append",
        metavar="NAME=VOICE",
        default=[],
        help="Map a speaker name to a Gemini voice (default Aoede and Charon)."
            " Repeat to override or add characters.",
    )
    parser.add_argument(
        "--api-key",
        help="Gemini API key; falls back to GENAI_API_KEY environment variable if omitted.",
    )
    parser.add_argument(
        "--output-format",
        choices=("mp3", "opus", "both"),
        default="mp3",
        help="Final encoding; mp3 uses libmp3lame, opus uses libopus, both generates two files.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to place final file(s); created automatically if missing.",
    )
    parser.add_argument(
        "--output-prefix",
        default="podcast",
        help="Base name for the final files (e.g., podcast.mp3).",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the built-in Aoede/Charon sample script with laugh/sigh cues for testing.",
    )
    return parser


def parse_script(raw_text):
    segments = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" not in line:
            # Default to first speaker if missing colon
            speaker, content = "Aoede", line
        else:
            speaker, content = line.split(":", 1)
        speaker = speaker.strip()
        content = content.strip()
        if not speaker or not content:
            continue
        segments.append({"speaker": speaker, "text": content})
    if not segments:
        raise UsageError("脚本中未找到任何有效的对话行。")
    return segments


def merge_speaker_map(custom_mappings):
    speaker_map = dict(DEFAULT_SPEAKER_VOICES)
    for mapping in custom_mappings or []:
        if "=" not in mapping:
            raise UsageError("--speaker-voice 必须采用 NAME=VOICE 格式。")
        name, voice = mapping.split("=", 1)
        name = name.strip()
        voice = voice.strip()
        if not name or not voice:
            raise UsageError("--speaker-voice 中的名称和语音都不能为空。")
        speaker_map[name] = voice
    return speaker_map


def ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise UsageError("找不到 ffmpeg，无法拼接或混合音频。请先安装 ffmpeg。")


def download_background():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    dst = CACHE_DIR / "bensound-littleidea.mp3"
    if dst.exists():
        return dst
    print("正在下载背景音乐，请稍候……")
    urllib.request.urlretrieve(BACKGROUND_URL, dst)
    return dst


def save_wav(filename, pcm_data, rate=24000):
    """Saves raw L16 PCM data to a WAV file."""
    with wave.open(str(filename), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(rate)
        wf.writeframes(pcm_data)


def call_gemini(api_key, text, voice):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-preview-tts:generateContent?key="
        f"{api_key}"
    )
    # The model expects an instruction like "Say: ..." for better TTS performance
    prompt = f"Say: {text}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice
                    }
                }
            }
        }
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_data = response.read()
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="ignore")
        raise UsageError(f"API 请求失败：{exc.code} {exc.reason}。响应：{message}")
    except urllib.error.URLError as exc:
        raise UsageError(f"无法连接到 Gemini API：{exc.reason}")

    decoded = json.loads(response_data)
    try:
        parts = decoded["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    except (KeyError, IndexError):
        pass
    raise UsageError(f"API 未返回可解码的音频。响应内容：{json.dumps(decoded, indent=2)}")


def concatenate_segments(segment_paths, output_path):
    # Use a simple list of files if it's small, otherwise concat demuxer
    if len(segment_paths) == 1:
        shutil.copy(segment_paths[0], output_path)
        return

    list_txt = output_path.parent / "segments.txt"
    with open(list_txt, "w", encoding="utf-8") as handle:
        for path in segment_paths:
            # Use relative path to avoid path issues
            handle.write(f"file '{path.name}'\n")
    
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_txt),
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]
    # Run in the directory of the segments
    subprocess.run(cmd, check=True, cwd=str(output_path.parent))
    list_txt.unlink()


def mix_with_background(speech_path, background_path, mixed_path):
    # Background volume set to 0.1 (10%) as requested
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(speech_path),
        "-stream_loop",
        "-1",
        "-i",
        str(background_path),
        "-filter_complex",
        "[1:a]volume=0.08[a1];[0:a][a1]amix=inputs=2:duration=shortest[aout]",
        "-map",
        "[aout]",
        "-c:a",
        "pcm_s16le",
        str(mixed_path),
    ]
    subprocess.run(cmd, check=True)


def encode_output(mixed_path, output_path, codec_args):
    cmd = ["ffmpeg", "-y", "-i", str(mixed_path)] + codec_args + [str(output_path)]
    subprocess.run(cmd, check=True)


def load_script_text(args):
    if args.demo:
        return SAMPLE_SCRIPT
    if args.script_text:
        return args.script_text
    if args.script_file:
        return Path(args.script_file).read_text(encoding="utf-8")
    raise UsageError("必须通过 --script-text、--script-file 或 --demo 提供脚本输入。")


def main():
    parser = create_parser()
    args = parser.parse_args()

    raw_text = load_script_text(args)
    segments = parse_script(raw_text)
    speaker_map = merge_speaker_map(args.speaker_voice)
    api_key = args.api_key or os.environ.get("GENAI_API_KEY")
    if not api_key:
        parser.error("需要通过 --api-key 或 GENAI_API_KEY 环境变量提供 Gemini API 密钥。")

    ensure_ffmpeg()
    background_path = download_background()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    segment_paths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for index, segment in enumerate(segments, start=1):
            speaker = segment["speaker"]
            if speaker not in speaker_map:
                # Fallback to default speaker if mapping missing
                speaker = "Aoede"
            voice_name = speaker_map[speaker]
            print(f"生成第 {index}/{len(segments)} 段：{segment['speaker']} ({voice_name})")
            
            # Use exponential backoff for 429
            for attempt in range(3):
                try:
                    segment_audio = call_gemini(api_key, segment["text"], voice_name)
                    break
                except UsageError as e:
                    if "429" in str(e) and attempt < 2:
                        wait_time = 30 * (attempt + 1)
                        print(f"  触发频率限制，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        raise e
            
            print(f"  音频大小：{len(segment_audio)} 字节")
            segment_path = tmpdir_path / f"segment_{index:02d}.wav"
            save_wav(segment_path, segment_audio)
            segment_paths.append(segment_path)
            
            # Avoid 429 on free tier (3 RPM)
            if index < len(segments):
                time.sleep(2)

        speech_wav = tmpdir_path / "speech.wav"
        concatenate_segments(segment_paths, speech_wav)
        mixed_wav = tmpdir_path / "speech_with_bg.wav"
        mix_with_background(speech_wav, background_path, mixed_wav)

        final_outputs = []
        if args.output_format in ("mp3", "both"):
            mp3_path = output_dir / f"{args.output_prefix}.mp3"
            encode_output(mixed_wav, mp3_path, ["-c:a", "libmp3lame", "-q:a", "2"])
            final_outputs.append(mp3_path)
        if args.output_format in ("opus", "both"):
            opus_path = output_dir / f"{args.output_prefix}.opus"
            encode_output(mixed_wav, opus_path, ["-c:a", "libopus", "-b:a", "128k"])
            final_outputs.append(opus_path)

    print("生成完成，输出文件：")
    for file_path in final_outputs:
        print(f" - {file_path.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except UsageError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        sys.exit(1)
