#!/usr/bin/env python3
"""Subagent dispatch helper.

Usage:
  subagent_dispatch.py --task "..." [--tier hard|medium|free] [--json]

Returns a model + role + a short task template for subagent execution.
"""
import argparse
import json

TIERS = {
    "hard": {
        "role": "worker-strong",
        "model": "openai-codex/gpt-5.2-codex",
    },
    "medium": {
        "role": "worker-medium",
        "model": "openai-codex/gpt-5.1-codex-mini",
    },
    "free": {
        "role": "worker-free",
        "model": "qwen-portal/coder-model",
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="task description")
    ap.add_argument(
        "--tier",
        choices=TIERS.keys(),
        default="medium",
        help="routing tier",
    )
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    picked = TIERS[args.tier]
    payload = {
        "tier": args.tier,
        "role": picked["role"],
        "model": picked["model"],
        "task": args.task,
        "template": (
            "请作为子 agent 执行任务：" + args.task + "\n"
            "要求：仅专注任务；输出结果 + 证据；结束后停止子 agent；"
            "创建时请带 runTimeoutSeconds=180。"
        ),
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"role: {payload['role']}")
        print(f"model: {payload['model']}")
        print("task:")
        print(payload["template"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
