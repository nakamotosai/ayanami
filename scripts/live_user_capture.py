#!/usr/bin/env python3
"""Capture user messages periodically into NOW.md and daily log.

Runs safely on cron; only appends new user messages since last run.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable

BASE_DIR = Path("/home/ubuntu/.openclaw")
WORKSPACE = BASE_DIR / "workspace"
SESSIONS_DIR = BASE_DIR / "agents" / "main" / "sessions"
SESSIONS_JSON = SESSIONS_DIR / "sessions.json"
STATE_FILE = WORKSPACE / "memory" / "live_capture_state.json"
NOW_FILE = WORKSPACE / "memory" / "NOW.md"
TOKYO_TZ = timezone(timedelta(hours=9))


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _ensure_now_file() -> None:
    NOW_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not NOW_FILE.exists():
        NOW_FILE.write_text("# NOW（滚动短期记忆）\n\n", encoding="utf-8")


def _ensure_daily_file(date_str: str) -> Path:
    target = WORKSPACE / "memory" / f"{date_str}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(f"# 记忆日志 {date_str}\n\n", encoding="utf-8")
    return target


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


def _load_current_session_id() -> str | None:
    sessions = _load_json(SESSIONS_JSON)
    return sessions.get("agent:main:main", {}).get("sessionId")


def main() -> None:
    current = _load_current_session_id()
    if not current:
        return

    session_file = SESSIONS_DIR / f"{current}.jsonl"
    if not session_file.exists():
        return

    state = _load_json(STATE_FILE)
    last_idx = int(state.get(current, 0) or 0)

    lines = session_file.read_text(encoding="utf-8", errors="ignore").splitlines()
    if last_idx >= len(lines):
        return

    user_texts: list[str] = []
    for idx in range(last_idx, len(lines)):
        raw = lines[idx].strip()
        if not raw:
            continue
        try:
            node = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if node.get("type") != "message":
            continue
        message = node.get("message") or {}
        role = message.get("role")
        if role != "user":
            continue
        text = _extract_text(message.get("content")) or _extract_text(message.get("text"))
        if text:
            user_texts.append(text)

    state[current] = len(lines)
    _save_json(STATE_FILE, state)

    if not user_texts:
        return

    stamp = datetime.now(TOKYO_TZ).strftime("%Y-%m-%dT%H:%M:%SZ")
    _ensure_now_file()
    daily = _ensure_daily_file(datetime.now(TOKYO_TZ).date().isoformat())

    now_block = ["", f"## {stamp} session {current[:8]}"]
    for i, text in enumerate(user_texts, 1):
        now_block.append(f"- {i}. {text}")
    now_block.append("")
    NOW_FILE.open("a", encoding="utf-8").write("\n".join(now_block))

    daily_block = ["", f"### 用户原话（实时捕捉 @ {stamp} / session {current[:8]}）"]
    for i, text in enumerate(user_texts, 1):
        daily_block.append(f"- {i}. {text}")
    daily_block.append("")
    daily.open("a", encoding="utf-8").write("\n".join(daily_block))


if __name__ == "__main__":
    main()
