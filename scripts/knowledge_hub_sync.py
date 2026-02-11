#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

import yaml

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
CARDS_DIR = WORKSPACE / "skills" / "learner-docs" / "cards"
CATALOG = WORKSPACE / "knowledge-hub" / "catalog.yaml"


def parse_card(path: Path):
    text = path.read_text(encoding="utf-8")
    data = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1]) or {}
            except Exception:
                data = {}
            body = parts[2].strip()
    data.setdefault("title", path.stem)
    data.setdefault("path", str(path.relative_to(WORKSPACE)))
    data.setdefault("updated_at", datetime.utcnow().isoformat() + "Z")
    data.setdefault("tags", [])
    if "summary" not in data:
        data["summary"] = body.splitlines()[0] if body else ""
    data["body"] = body
    return data


def main():
    if not CARDS_DIR.exists():
        CARDS_DIR.mkdir(parents=True)
    cards = []
    for path in sorted(CARDS_DIR.glob("*.md")):
        cards.append(parse_card(path))
    catalog = {"entries": cards, "last_synced": datetime.utcnow().isoformat() + "Z"}
    CATALOG.write_text(yaml.safe_dump(catalog, allow_unicode=True), encoding="utf-8")
    print(f"Synced {len(cards)} cards to {CATALOG}")


if __name__ == "__main__":
    main()
