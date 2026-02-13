#!/usr/bin/env python3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

WS = Path.home() / ".openclaw" / "workspace"
DAILY_DIR = WS / "memory"
OUT = WS / "memory" / "daily-proposal.md"

# Simple heuristic proposal generator: detect repeated tool failures/timeouts and propose fixes.
KEYWORDS = [
    "timeout",
    "gateway timeout",
    "EPIPE",
    "failed",
    "Conflict",
    "suspicious",
]


def read_recent_daily(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    texts = []
    for p in sorted(DAILY_DIR.glob("*.md")):
        try:
            # cheap filter by mtime
            if datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc) < cutoff:
                continue
        except Exception:
            continue
        try:
            texts.append((p.name, p.read_text(encoding="utf-8", errors="ignore")))
        except Exception:
            pass
    return texts


def main():
    items = read_recent_daily()
    hits = []
    for name, txt in items:
        low = txt.lower()
        if any(k in low for k in KEYWORDS):
            hits.append(name)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = []
    lines.append(f"# Daily Upgrade Proposal ({ts})\n")
    lines.append("最多 3 条。每条包含：改动点 / 风险 / 验收。\n")

    # Always propose one: keep qmd query off by default
    lines.append("## 1) 默认检索走 qmd search（避免模型下载导致卡死）\n")
    lines.append("- 改动：保持 `skills/enhanced-memory/scripts/search.sh` 默认 search 模式\n")
    lines.append("- 风险：低\n")
    lines.append("- 验收：运行 `bash skills/enhanced-memory/scripts/search.sh \"关键词\"`\n")

    # Propose: harden cron status timeout
    lines.append("## 2) Heartbeat 自检改为轻量 health（减少 gateway timeout）\n")
    lines.append("- 改动：把 `openclaw cron status` 换成 `openclaw status` 或直接跳过\n")
    lines.append("- 风险：低\n")
    lines.append("- 验收：手动触发 heartbeat cron，确认耗时 < 30s\n")

    # Propose: ensure git sync uses GH_TOKEN
    lines.append("## 3) GitHub sync 强制 GH_TOKEN=GITHUB_TOKEN（避免 session 过期）\n")
    lines.append("- 改动：HEARTBEAT.md 已加固（保持）\n")
    lines.append("- 风险：低\n")
    lines.append("- 验收：制造一次变更，触发 heartbeat，确认 push 成功\n")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "filesHit": hits[:10]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
