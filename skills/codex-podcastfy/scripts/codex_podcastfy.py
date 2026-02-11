#!/usr/bin/env python3
import argparse
import asyncio
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import edge_tts
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Podcastfy/1.0; +https://github.com/openclaw)"
}


def fetch_url_text(url: str, max_chars: int = 6000) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["nav", "header", "footer", "script", "style"]):
        tag.decompose()
    paragraphs = []
    for elem in soup.find_all(["article", "p", "li"]):
        text = elem.get_text(" ", strip=True)
        if len(text) > 40:
            paragraphs.append(text)
        if len("\n".join(paragraphs)) > max_chars:
            break
    result = "\n".join(paragraphs)
    return result[:max_chars].strip()


def fetch_top_japan_news(count: int = 10) -> list[str]:
    rss = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    resp = requests.get(rss, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else []
    news = []
    for idx, item in enumerate(items):
        if idx >= count:
            break
        title = item.findtext("title", default="").strip()
        if title:
            news.append(f"{idx + 1}. {title}")
    return news


def codex_model_short() -> str:
    model = os.environ.get("CODEX_MODEL", "gpt-5.1-codex-mini")
    return model.split("/")[-1]


def build_prompt(texts: list[str], longform: bool, news: list[str]) -> str:
    tone = "long-form, two-minute" if longform else "punchy"
    joined = "\n\n---\n\n".join(texts)
    news_block = "\n".join(news)
    if news_block:
        news_block = f"最新的 10 条日本新闻：\n{news_block}\n"
    intro = "欢迎收听今日日本新闻速览，预计收听时间：约2分钟。"
    outro = "以上就是今天的新闻速览，感谢您的收听！"
    return f"""You are a podcast writer creating a conversational transcript for a human-hosted show.
The source material is below. Produce:
1. A single-narrator transcript in Chinese (not a dialogue).
2. Do not use any markdown like ** or * around speaker names or other text.
3. Do not include any English words or phrases in the transcript.
4. Three bullet-point highlights after the transcript.
5. A short note about estimated listening time (~2 min if not longform, ~4 min if longform).
Keep the style friendly, curious, and easy to read. {tone} tone.
{intro}

{news_block}
Source material:\n{joined}\n
Transcript:
{outro}
"""


def run_codex(prompt: str) -> str:
    model = codex_model_short()
    cmd = [
        "codex",
        "exec",
        "-m",
        model,
        "--sandbox",
        "danger-full-access",
        "--dangerously-bypass-approvals-and-sandbox",
    ]
    print(f"Running Codex model {model}…", file=sys.stderr)
    proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Codex failed (code {proc.returncode}): {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


async def synthesize(text: str, voice: str, dest: Path) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(dest))


def convert_mp3_to_ogg(mp3_path: Path, ogg_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(mp3_path),
        "-c:a",
        "libopus",
        "-b:a",
        "64k",
        str(ogg_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def ensure_dirs(base: Path) -> tuple[Path, Path]:
    audio = base / "output" / "audio"
    transcripts = base / "output" / "transcripts"
    audio.mkdir(parents=True, exist_ok=True)
    transcripts.mkdir(parents=True, exist_ok=True)
    return audio, transcripts


def main() -> None:
    parser = argparse.ArgumentParser(description="Codex-based Podcast generator")
    parser.add_argument("--url", action="append", help="Page(s) to summarize")
    parser.add_argument("--voice", default="en-US-JennyNeural", help="Edge TTS voice ID")
    parser.add_argument("--longform", action="store_true", help="Ask Codex for a longer script")
    parser.add_argument("--japan-news", action="store_true", help="Use top 10 Japanese news instead of URLs")
    parser.add_argument("--output-dir", default="~/.openclaw/workspace", help="Root directory for output (default workspace)")
    args = parser.parse_args()

    if not args.japan_news and not args.url:
        parser.error("either --url or --japan-news is required")

    roots = Path(os.path.expanduser(args.output_dir))
    audio_dir, transcript_dir = ensure_dirs(roots)

    snippets: list[str] = []
    news_list: list[str] = []
    if args.japan_news:
        news_list = fetch_top_japan_news(10)
        snippets.append("\n".join(news_list))
    if args.url:
        for url in args.url:
            try:
                text = fetch_url_text(url)
            except Exception as exc:
                raise SystemExit(f"Failed to fetch {url}: {exc}")
            if not text:
                raise SystemExit(f"Nothing to summarize at {url}")
            snippets.append(text)

    prompt = build_prompt(snippets, args.longform, news_list)
    transcript = run_codex(prompt)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    audio_path = audio_dir / f"podcastfy-{timestamp}.mp3"
    transcript_path = transcript_dir / f"podcastfy-{timestamp}.txt"
    transcript_path.write_text(transcript, encoding="utf-8")
    
    # Use single narrator voice for transcript
    full_text = transcript.replace("\n", " ")
    
    asyncio.run(synthesize(full_text, args.voice, audio_path))
    ogg_path = audio_path.with_suffix(".ogg")
    convert_mp3_to_ogg(audio_path, ogg_path)

    print(f"Transcript saved: {transcript_path}")
    print(f"Audio saved: {audio_path}")
    print(f"OGG saved: {ogg_path}")


if __name__ == "__main__":
    main()
