#!/usr/bin/env python3
import argparse
from pathlib import Path

import yaml

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
CATALOG = WORKSPACE / "knowledge-hub" / "catalog.yaml"


def load_catalog():
    if not CATALOG.exists():
        raise SystemExit("knowledge hub catalog missing")
    with CATALOG.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    entries = {entry.get("id"): entry for entry in data.get("entries", [])}
    return entries


def main():
    parser = argparse.ArgumentParser(description="Rehydrate raw context from Knowledge Hub entry")
    parser.add_argument("--id", required=True, help="Entry ID from catalog")
    args = parser.parse_args()
    entries = load_catalog()
    if args.id not in entries:
        raise SystemExit(f"Entry {args.id} not found")
    entry = entries[args.id]
    path = WORKSPACE / entry.get("path", "")
    if not path.exists():
        raise SystemExit(f"Referenced path does not exist: {path}")
    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
