#!/usr/bin/env python3
"""Cross-agent session-watch helper.

Incrementally tails all ~/.openclaw/agents/*/sessions/*.jsonl user messages,
extracts preference-like statements, and appends structured notes into
workspace MEMORY.md + daily memory log.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
AGENTS_ROOT = Path("/home/ubuntu/.openclaw/agents")
WATCH_FILE = WORKSPACE / "memory" / "session-watch.json"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
TOKYO_TZ = timezone(timedelta(hours=9))
MAX_ITEM_LEN = 180
MAX_PREF_ITEMS = 20

PREFERENCE_KEYWORDS = [
    "喜欢", "不喜欢", "希望", "想要", "必须", "需要", "一定", "以后", "永远",
    "记住", "别忘", "不要", "只能", "请你", "偏好", "规则", "要求",
]
PREFERENCE_LOWER = [k.lower() for k in PREFERENCE_KEYWORDS]
SENTENCE_SPLIT_REGEX = re.compile(r"[。！？!?\n]+|\.\s+")


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_text(content: Iterable | str | None) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if content.get("type") == "text":
            return content.get("text", "")
        return _extract_text(content.get("content") or content.get("text"))
    if isinstance(content, Iterable):
        return "".join(_extract_text(item) for item in content)
    return ""


def _split_sentences(text: str) -> list[str]:
    chunks = SENTENCE_SPLIT_REGEX.split(text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _iter_session_files() -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    if not AGENTS_ROOT.exists():
        return out
    for agent_dir in sorted(AGENTS_ROOT.iterdir()):
        if not agent_dir.is_dir():
            continue
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.is_dir():
            continue
        for session_file in sorted(sessions_dir.glob("*.jsonl")):
            out.append((agent_dir.name, session_file))
    return out


def _collect_new_user_messages(offsets: dict[str, int]) -> tuple[list[tuple[str, str]], dict[str, int], dict[str, int]]:
    messages: list[tuple[str, str]] = []
    source_counts: dict[str, int] = {}

    for agent_name, session_file in _iter_session_files():
        key = f"{agent_name}:{session_file.stem}"
        lines = session_file.read_text(encoding="utf-8", errors="ignore").splitlines()

        if key not in offsets:
            # First seen session: start from EOF to avoid stale backfill.
            offsets[key] = len(lines)
            continue

        start = int(offsets.get(key, 0) or 0)
        if start < 0 or start > len(lines):
            start = 0

        for raw in lines[start:]:
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "message":
                continue
            message = entry.get("message") or {}
            if message.get("role") != "user":
                continue
            text = _extract_text(message.get("content")) or _extract_text(message.get("text"))
            if not text:
                continue
            messages.append((agent_name, text))
            source_counts[agent_name] = source_counts.get(agent_name, 0) + 1

        offsets[key] = len(lines)

    return messages, offsets, source_counts


def _extract_preferences(messages: list[tuple[str, str]]) -> list[str]:
    seen = set()
    prefs: list[str] = []
    for agent_name, text in messages:
        for sentence in _split_sentences(text):
            lowered = sentence.lower()
            if not any(k in lowered for k in PREFERENCE_LOWER):
                continue
            item = f"[{agent_name}] {sentence.strip()}"
            if len(item) > MAX_ITEM_LEN:
                item = item[: MAX_ITEM_LEN - 1].rstrip() + "…"
            if item in seen:
                continue
            seen.add(item)
            prefs.append(item)
            if len(prefs) >= MAX_PREF_ITEMS:
                return prefs
    return prefs


def _append_memory(stamp: str, source_counts: dict[str, int], prefs: list[str]) -> None:
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text("# MEMORY.md\n\n", encoding="utf-8")

    lines = ["", f"## 自动汇总 {stamp}", "- 来源会话统计:"]
    if source_counts:
        for name in sorted(source_counts):
            lines.append(f"  - {name}: {source_counts[name]}")
    else:
        lines.append("  - 无")

    lines.append("- 偏好候选:")
    if prefs:
        for item in prefs:
            lines.append(f"  - {item}")
    else:
        lines.append("  - 本轮无新增偏好句。")
    lines.append("")

    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _append_daily(stamp: str, messages: list[tuple[str, str]]) -> None:
    date_str = datetime.now(TOKYO_TZ).date().isoformat()
    daily = WORKSPACE / "memory" / f"{date_str}.md"
    daily.parent.mkdir(parents=True, exist_ok=True)
    if not daily.exists():
        daily.write_text(f"# 记忆日志 {date_str}（摘要）\n\n", encoding="utf-8")

    tail = messages[-8:]
    lines = ["", f"## {stamp} 跨 agent 会话汇总", f"- 新增用户消息: {len(messages)} 条", "- 最近消息:"]
    for agent_name, text in tail:
        lines.append(f"  - [{agent_name}] {text[:140]}")
    lines.append("")

    with daily.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    state = _load_json(WATCH_FILE)
    offsets = state.get("offsets", {}) if isinstance(state.get("offsets"), dict) else {}

    messages, offsets, source_counts = _collect_new_user_messages(offsets)

    state["offsets"] = offsets
    state["updatedAt"] = int(time.time())
    _write_json(WATCH_FILE, state)

    if not messages:
        print("NO_REPLY")
        return

    stamp = datetime.now(TOKYO_TZ).strftime("%Y-%m-%dT%H:%M:%SZ")
    prefs = _extract_preferences(messages)
    _append_memory(stamp, source_counts, prefs)
    _append_daily(stamp, messages)
    print("NO_REPLY")


if __name__ == "__main__":
    main()
