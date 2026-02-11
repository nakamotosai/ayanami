#!/usr/bin/env python3
import argparse
from pathlib import Path

import yaml

SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = SKILL_ROOT / "config" / "sources.yaml"


def load_sources():
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    sources = data.get("sources", [])
    return data, sources


def write_sources(sources):
    data = {"sources": sources}
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def normalize(name):
    return name.strip()


def main():
    parser = argparse.ArgumentParser(description="Add a new source for Learner docs skill.")
    parser.add_argument("name", help="Logical short name for the source (no spaces)")
    parser.add_argument("sitemap", help="Sitemap URL or entry point to read")
    parser.add_argument("--max-pages", type=int, default=30, help="Max pages to fetch")
    parser.add_argument("--note", default="", help="Optional note")
    args = parser.parse_args()

    data, sources = load_sources()
    for src in sources:
        if src.get("name") == args.name:
            raise SystemExit(f"Source with name '{args.name}' already exists")
        if src.get("sitemap") == args.sitemap:
            raise SystemExit(f"Source with sitemap '{args.sitemap}' already exists")

    new_source = {
        "name": normalize(args.name),
        "sitemap": args.sitemap,
        "max_pages": args.max_pages,
        "note": args.note,
    }
    sources.append(new_source)
    write_sources(sources)
    print(f"Added learner source '{args.name}' ({args.sitemap})")


if __name__ == "__main__":
    main()
