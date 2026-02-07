#!/usr/bin/env python3
"""OpenClaw hook dispatcher (wake).

Usage:
  hooks_wake.py --text "..." [--mode now|next-heartbeat]
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="system event text")
    ap.add_argument("--mode", default="now", choices=["now", "next-heartbeat"])
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
        "text": args.text,
        "mode": args.mode,
    }

    url = f"http://127.0.0.1:{port}{base_path}/wake"
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
