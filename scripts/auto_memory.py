#!/usr/bin/env python3
"""Auto-detects memory-worthy statements from session transcripts."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path("/home/ubuntu/.openclaw")
WORKSPACE = BASE_DIR / "workspace"
SESSIONS_DIR = BASE_DIR / "agents" / "main" / "sessions"
OUTPUT_FILE = WORKSPACE / "memory" / "auto_memory.md"
STATE_FILE = WORKSPACE / "memory" / "auto_memory_state.json"
KEYWORDS = [
    '记住',
    '记得',
    '记一下',
    '记下',
    '永远',
    '以后',
    '提醒我',
    '保存',
    'remember',
]


def _load_state() -> dict[str, int]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def _save_state(state: dict[str, int]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    STATE_FILE.chmod(0o644)


def _append_memory(entry: str) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not OUTPUT_FILE.exists():
        OUTPUT_FILE.write_text('# Auto memory log\n\n', encoding='utf-8')
    with OUTPUT_FILE.open('a', encoding='utf-8') as out:
        out.write(entry)


def _format_entry(session_key: str, timestamp: int, text: str) -> str:
    when = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    when_str = when.strftime('%Y-%m-%d %H:%M:%S UTC')
    sanitized = re.sub(r"\s+", ' ', text).strip()
    sanitized = sanitized.replace('\n', ' ')
    if not sanitized:
        return ''
    return f"## {when_str} ({session_key})\n- {sanitized}\n\n"


def main() -> None:
    state = _load_state()
    sessions: list[Path] = sorted(SESSIONS_DIR.glob('*.jsonl'))
    added = False
    for session_file in sessions:
        session_key = session_file.stem
        processed = state.get(session_key, 0)
        lines = session_file.read_text(encoding='utf-8').splitlines()
        for idx, raw in enumerate(lines):
            if idx < processed:
                continue
            raw = raw.strip()
            if not raw:
                continue
            try:
                node = json.loads(raw)
            except json.JSONDecodeError:
                continue
            timestamp = node.get('timestamp') or node.get('time')
            content = node.get('content', [])
            for chunk in content:
                if chunk.get('type') != 'text':
                    continue
                text = chunk.get('text', '')
                if any(keyword in text for keyword in KEYWORDS):
                    entry = _format_entry(session_key, timestamp or 0, text)
                    if entry:
                        _append_memory(entry)
                        added = True
        state[session_key] = len(lines)
    if added:
        _append_memory('')
    _save_state(state)


if __name__ == '__main__':
    main()
