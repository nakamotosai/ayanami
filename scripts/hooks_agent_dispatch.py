#!/usr/bin/env python3
"""OpenClaw dispatcher via current CLI path.

Usage:
  hooks_agent_dispatch.py --task "..." --tier hard|medium|free [--channel last|telegram|discord|line] [--to ID]
"""

import argparse
import json
import shlex
import subprocess
import sys

TIERS = {
    "hard": "codex-hard",
    "medium": "codex-medium",
    "free": "free-worker",
}


def build_command(args: argparse.Namespace) -> list[str]:
    cmd = [
        "openclaw",
        "agent",
        "--agent",
        TIERS[args.tier],
        "--message",
        args.task,
        "--json",
    ]

    if args.thinking:
        cmd.extend(["--thinking", args.thinking])
    if args.timeout and args.timeout > 0:
        cmd.extend(["--timeout", str(args.timeout)])

    # Optional cross-channel delivery using current CLI interface.
    if args.channel and args.channel != "last":
        cmd.extend(["--deliver", "--reply-channel", args.channel])
        if args.to:
            cmd.extend(["--reply-to", args.to])

    return cmd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="task description")
    ap.add_argument("--tier", choices=TIERS.keys(), default="medium")
    ap.add_argument("--channel", default="last", help="last|telegram|discord|line")
    ap.add_argument("--to", default="", help="channel recipient id")

    # Backward-compatible args from old hook flow; currently ignored.
    ap.add_argument("--name", default="Webhook", help="legacy, ignored")
    ap.add_argument("--wake", default="now", choices=["now", "next-heartbeat"], help="legacy, ignored")
    ap.add_argument("--source", default="", help="legacy, ignored")

    ap.add_argument("--thinking", default="", help="thinking level")
    ap.add_argument("--timeout", type=int, default=0, help="timeout seconds")
    args = ap.parse_args()

    cmd = build_command(args)

    # Emit command for evidence/debugging.
    print(json.dumps({"cmd": cmd, "shell": " ".join(shlex.quote(x) for x in cmd)}, ensure_ascii=False))

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)

    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
