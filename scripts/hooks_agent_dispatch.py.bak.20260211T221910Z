#!/usr/bin/env python3
"""OpenClaw hook dispatcher (agent).

Usage:
  hooks_agent_dispatch.py --task "..." --tier hard|medium|free [--channel last|telegram|discord|line] [--to ID]
"""
import argparse
import json
import urllib.request

from secrets_loader import (
    resolve_gateway_port,
    resolve_hook_source_token,
    resolve_hook_token,
    resolve_hooks_path,
)

TIERS = {
    "hard": "openai-codex/gpt-5.2-codex",
    "medium": "openai-codex/gpt-5.1-codex-mini",
    "free": "qwen-portal/coder-model",
}


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
    ap.add_argument("--source", default="", help="source validation token")
    args = ap.parse_args()

    token = resolve_hook_token()
    if not token:
        raise SystemExit("hooks.token missing (openclaw.json or credentials)")

    source_token = resolve_hook_source_token()
    if source_token:
        if not args.source or args.source != source_token:
            raise SystemExit("invalid hook source token")

    port = resolve_gateway_port()
    base_path = resolve_hooks_path()

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
    if args.source:
        req.add_header("X-Openclaw-Source", args.source)
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
