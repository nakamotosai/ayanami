#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = SCRIPT_ROOT / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)
KROKI_URL = "https://kroki.io/mermaid/png"


def render_mermaid(text: str, outfile: Path):
    resp = requests.post(KROKI_URL, data=text.encode("utf-8"), headers={"Content-Type": "text/plain"})
    resp.raise_for_status()
    outfile.write_bytes(resp.content)
    return outfile


def main():
    parser = argparse.ArgumentParser(description="Render Mermaid via kroki for Learner diagrams.")
    parser.add_argument("--mermaid", required=True, help="Path to Mermaid .mmd file")
    parser.add_argument("--output", help="Output PNG path", default="/tmp/learner-diagram.png")
    args = parser.parse_args()

    mermaid_path = Path(args.mermaid)
    if not mermaid_path.exists():
        raise SystemExit(f"Mermaid file not found: {mermaid_path}")
    text = mermaid_path.read_text(encoding="utf-8")
    out = Path(args.output)
    render_mermaid(text, out)
    print(f"Rendered remote diagram to {out}")

    card_path = OUTPUT_DIR / f"diagram-{out.stem}.png"
    card_path.write_bytes(out.read_bytes())
    print(f"Saved copy to {card_path}")


if __name__ == "__main__":
    main()
