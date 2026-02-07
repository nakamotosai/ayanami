#!/usr/bin/env python3
"""OpenClaw hook dispatcher (wake).

Usage:
  hooks_wake.py --text "..." [--mode now|next-heartbeat]
"""
import argparse
import json
import re
import urllib.request
from pathlib import Path

CFG_PATH = Path("/home/ubuntu/.openclaw/openclaw.json")


def load_cfg():
    text = CFG_PATH.read_text(encoding="utf-8")
    cleaned = re.sub(r",\s*([\]}])", r"\1", text)
    return json.loads(cleaned)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="system event text")
    ap.add_argument("--mode", default="now", choices=["now", "next-heartbeat"])
    args = ap.parse_args()

    cfg = load_cfg()
    hooks = cfg.get("hooks", {})
    gateway = cfg.get("gateway", {})
    token = hooks.get("token", "").strip()
    if not token:
        raise SystemExit("hooks.token missing in openclaw.json")
    base_path = hooks.get("path", "/hooks").strip() or "/hooks"
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    port = int(gateway.get("port", 18789))

    payload = {
        "text": args.text,
        "mode": args.mode,
    }

    url = f"http://127.0.0.1:{port}{base_path}/wake"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
