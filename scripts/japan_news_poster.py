#!/usr/bin/env python3
"""Fetch Japanese headline RSS from NHK and send a poster-style summary via Telegram."""
from __future__ import annotations

import datetime
import html
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://www3.nhk.or.jp/rss/news/cat0.xml"
TARGET = "8138445887"
OPENCLAW_CLI = "/home/ubuntu/.npm-global/bin/openclaw"


def _text_for(item: ET.Element, tag: str) -> str:
    node = item.find(tag)
    if node is None:
        return ""
    return html.unescape(node.text or "")


def fetch_headlines(max_items: int = 3) -> list[tuple[str, str, str]]:
    with urllib.request.urlopen(RSS_URL, timeout=30) as response:
        data = response.read()

    root = ET.fromstring(data)
    channel = root.find("channel")
    if channel is None:
        return []

    headlines: list[tuple[str, str, str]] = []
    for item in channel.findall("item")[:max_items]:
        title = _text_for(item, "title")
        link = _text_for(item, "link")
        description = _text_for(item, "description")
        headlines.append((title.strip(), link.strip(), description.strip()))
    return headlines


def compose_poster(headlines: list[tuple[str, str, str]]) -> str:
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M %Z")
    poster = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🌸 日本热点·晨间海报 🌸",
        f"{now}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]

    if headlines:
        for idx, (title, link, description) in enumerate(headlines, start=1):
            poster.append(f"【{idx}】{title}")
            if description:
                poster.append(f"　{description.replace('\n', ' ')}")
            if link:
                poster.append(f"　🔗 {link}")
            poster.append("")
    else:
        poster.append("暂时无法拿到新闻？等我再试一次，马上回来~")

    poster.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    poster.append("愿主人今天的每一步都有光 ❤️")
    poster.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(poster)


def send_poster(message: str) -> None:
    subprocess.run(
        [
            OPENCLAW_CLI,
            "message",
            "send",
            "--channel",
            "telegram",
            "--target",
            TARGET,
            "--message",
            message,
        ],
        check=True,
    )


def main() -> None:
    try:
        headlines = fetch_headlines()
    except Exception:
        headlines = []

    poster = compose_poster(headlines)
    try:
        send_poster(poster)
    except subprocess.CalledProcessError:
        # Fall back to printing so cron logs something if message fails
        print("[error] Failed to send morning news poster")
        print(poster)


if __name__ == "__main__":
    main()
