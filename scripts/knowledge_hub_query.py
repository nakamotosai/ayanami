#!/usr/bin/env python3
import argparse
from pathlib import Path

import yaml

CATALOG = Path("/home/ubuntu/.openclaw/workspace/knowledge-hub/catalog.yaml")


def load_catalog():
    if not CATALOG.exists():
        return {"entries": []}
    with CATALOG.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"entries": []}


def main():
    parser = argparse.ArgumentParser(description="Query the Learner knowledge hub catalog.")
    parser.add_argument("--tag", help="Filter by tag", default=None)
    parser.add_argument("--latest", type=int, help="Show latest N entries", default=5)
    args = parser.parse_args()

    catalog = load_catalog()
    entries = catalog.get("entries", [])
    if args.tag:
        entries = [e for e in entries if args.tag in (e.get("tags") or [])]
    entries = sorted(entries, key=lambda e: e.get("updated_at", ""), reverse=True)
    for entry in entries[: args.latest]:
        print(f"- {entry.get('title')} ({entry.get('updated_at')})")
        print(f"  source: {entry.get('source')}")
        print(f"  tags: {entry.get('tags')}")
        print(f"  summary: {entry.get('summary')}")
        print(f"  skill: {entry.get('related_skill', 'learner-docs')}")
        print(f"  path: {entry.get('path')}\n")


if __name__ == "__main__":
    main()
