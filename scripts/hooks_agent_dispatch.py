#!/usr/bin/env python3
"""OpenClaw hook dispatcher (agent).

Usage:
  hooks_agent_dispatch.py --task "..." --tier hard|medium|free [--channel last|telegram|discord|line] [--to ID]

Reads hooks token + gateway port from /home/ubuntu/.openclaw/openclaw.json and POSTs to /hooks/agent.
"""
import argparse
import json
import re
import urllib.request
from pathlib import Path

CFG_PATH = Path("/home/ubuntu/.openclaw/openclaw.json")

TIERS = {
    "hard": "openai-codex/gpt-5.2-codex",
    "medium": "openai-codex/gpt-5.1-codex-mini",
    "free": "qwen-portal/coder-model",
}


def load_cfg():
    text = CFG_PATH.read_text(encoding="utf-8")
    # Remove trailing commas before ] or }
    cleaned = re.sub(r",\s*([\]}])", r"\1", text)
    return json.loads(cleaned)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="task description")
    ap.add_argument("--tier", choices=TIERS.keys(), default="medium")
    ap.add_argument("--channel", default="last", help="last|telegram|discord|line")
    ap.add_argument("--to", default="", help="channel recipient id")
    ap.add_argument("--name", default="Webhook", help="hook name")
    ap.add_argument("--wake", default="now", choices=["now", "next-heartbeat"])
    ap.add_argument("--thinking", default="", help="optional thinking level")
    ap.add_argument("--timeout", type=int, default=0, help="timeout seconds")
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
        "message": args.task,
        "name": args.name,
        "wakeMode": args.wake,
        "channel": args.channel,
        "model": TIERS[args.tier],
    }
    if args.to:
        payload["to"] = args.to
    if args.thinking:
        payload["thinking"] = args.thinking
    if args.timeout and args.timeout > 0:
        payload["timeoutSeconds"] = args.timeout

    url = f"http://127.0.0.1:{port}{base_path}/agent"
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
