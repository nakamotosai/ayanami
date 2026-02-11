#!/usr/bin/env python3
"""Simple DuckDuckGo Instant Answer search skill."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterable, Sequence

DDG_ENDPOINT = (
    "https://api.duckduckgo.com/?format=json&nohtml=1&skip_disambig=1&pretty=1&q="
)


class DDGSearchError(Exception):
    pass


def fetch_results(query: str) -> dict[str, object]:
    encoded = urllib.parse.quote_plus(query)
    url = DDG_ENDPOINT + encoded
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenClaw ddg-search"},
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.URLError as exc:  # pragma: no cover - network
        raise DDGSearchError(f"Failed to contact DuckDuckGo: {exc.reason}") from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - network
        raise DDGSearchError("DuckDuckGo returned invalid JSON") from exc


def extract_related_topics(topics: Sequence[dict[str, object]]) -> list[str]:
    entries: list[str] = []

    def visit(item: dict[str, object]) -> None:
        text = item.get("Text")
        if isinstance(text, str) and text.strip():
            entries.append(text.strip())
        for child in item.get("Topics", []):
            if isinstance(child, dict):
                visit(child)

    for topic in topics:
        visit(topic)
        if len(entries) >= 3:
            break

    return entries[:3]


def render_output(data: dict[str, object]) -> str:
    abstract_text = (data.get("AbstractText") or "").strip()
    abstract_url = (data.get("AbstractURL") or "").strip()
    redirect = (data.get("Redirect") or "").strip()

    if abstract_text:
        lines = [abstract_text]
        if abstract_url:
            lines.append(f"URL: {abstract_url}")
        return "\n".join(lines)

    if redirect:
        return f"Redirect: {redirect}"

    related_topics = extract_related_topics(data.get("RelatedTopics", []))
    if related_topics:
        body = "Related Topics:\n" + "\n".join(related_topics)
        return body

    return "No direct answer or related topics found."


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search DuckDuckGo via the Instant Answer API",
    )
    parser.add_argument("query", nargs="+", help="Query string to search for")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    query = " ".join(args.query).strip()
    if not query:
        raise DDGSearchError("Missing search query")

    data = fetch_results(query)
    output = render_output(data)
    print(output)


if __name__ == "__main__":
    try:
        main()
    except DDGSearchError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        sys.exit(1)
