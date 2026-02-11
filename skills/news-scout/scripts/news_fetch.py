#!/usr/bin/env python3
"""Fetch multilingual news from a SearXNG instance and translate summaries to Chinese."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from itertools import chain
from typing import Iterable, Mapping, Sequence

SEARX_TIMEOUT = 15
TRANSLATE_TIMEOUT = 15


def get_searx_base_url() -> str:
    url = os.environ.get("SEARXNG_URL", "").strip()
    if not url:
        return ""
    url = url.rstrip("/")
    if url.endswith("/search"):
        url = url[: -len("/search")]
    return url


def call_searx(query: str, count: int, lang: str | None) -> Mapping[str, object]:
    base = get_searx_base_url()
    if not base:
        raise RuntimeError("SEARXNG_URL environment variable is not set")

    params = {"q": query, "format": "json"}
    if lang:
        params["language"] = lang
    if count:
        params["n"] = str(count)

    url = f"{base}/search?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "news-scout/1.0",
        },
    )

    with urllib.request.urlopen(request, timeout=SEARX_TIMEOUT) as resp:
        data = json.load(resp)
    return data


def translate_text(text: str, dest: str = "zh-CN", src: str = "auto") -> str:
    if not text.strip():
        return text
    params = {
        "client": "gtx",
        "sl": src,
        "tl": dest,
        "dt": "t",
        "q": text,
    }
    url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TRANSLATE_TIMEOUT) as resp:
            payload = json.load(resp)
    except Exception:  # pragma: no cover - network
        return text

    translated_chunks = []
    if isinstance(payload, list) and payload:
        for chunk in payload[0]:
            if isinstance(chunk, list) and chunk:
                translated_chunks.append(chunk[0] or "")
    return "".join(translated_chunks) or text


def summarize_results(results: Sequence[Mapping[str, object]], translate: bool, trans_src: str, trans_dest: str) -> list[Mapping[str, object]]:
    summary = []

    for item in results:
        title = str(item.get("title", "")).strip()
        description = str(item.get("content", "") or item.get("description", "") or "").strip()
        url = str(item.get("url", ""))
        category = str(item.get("category", ""))
        engine = ", ".join(map(str, item.get("engines", [])))

        if translate and title:
            title = translate_text(title, dest=trans_dest, src=trans_src)
        if translate and description:
            description = translate_text(description, dest=trans_dest, src=trans_src)

        summary.append(
            {
                "title": title,
                "description": description,
                "url": url,
                "category": category,
                "engine": engine,
            }
        )
    return summary


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multilingual news fetcher using SearXNG + Google Translate")
    parser.add_argument("query", help="Search keywords in the source language")
    parser.add_argument("-l", "--language", help="SearXNG language code to restrict the search")
    parser.add_argument("-c", "--count", type=int, default=10, help="Number of results to return")
    parser.add_argument("--no-translate", action="store_true", help="Skip translating titles/descriptions")
    parser.add_argument("--source-lang", default="auto", help="Source language for translation (default: auto detect)")
    parser.add_argument("--target-lang", default="zh-CN", help="Target language for translation (default: Chinese)")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_arguments(argv)
    try:
        data = call_searx(args.query, args.count, args.language)
    except Exception as exc:
        sys.stdout.write(json.dumps({"error": str(exc)}))
        sys.exit(1)

    results = data.get("results", [])
    summary = summarize_results(results, not args.no_translate, args.source_lang, args.target_lang)

    output = {
        "query": args.query,
        "language": args.language or "all",
        "count": len(summary),
        "source": "SearXNG",
        "results": summary,
    }

    if suggestions := data.get("suggestions"):
        output["suggestions"] = [str(item) for item in suggestions if item]

    sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
