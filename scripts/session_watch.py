#!/usr/bin/env python3
"""Session-watch helper that auto-summarizes ended sessions into memory + todos."""
from __future__ import annotations

import json
import re
import textwrap
import time
from collections import deque
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable, Sequence

WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
SESSION_DIR = Path("/home/ubuntu/.openclaw/agents/main/sessions")
SESSIONS_JSON = SESSION_DIR / "sessions.json"
WATCH_FILE = WORKSPACE / "memory" / "session-watch.json"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
TODAY_MEMORY_DIR = WORKSPACE / "memory"
TODOS_FILE = TODAY_MEMORY_DIR / "todos.md"
NOW_FILE = TODAY_MEMORY_DIR / "NOW.md"
TOKYO_TZ = timezone(timedelta(hours=9))
MAX_TAIL_LINES = 200
MAX_TODO_UPDATES = 7

KEYWORDS = [
    "规则",
    "偏好",
    "喜欢",
    "记住",
    "Preference",
    "remember",
    "always",
    "should",
    "必须",
    "需要",
    "长期",
    "固定",
    "约定",
]
DECISION_KEYWORDS = [
    "决定",
    "计划",
    "安排",
    "打算",
    "准备",
    "需要",
    "应当",
    "will",
    "shall",
    "should",
    "next step",
    "下一步",
]
RISK_KEYWORDS = [
    "风险",
    "坑",
    "注意",
    "提醒",
    "问题",
    "警惕",
    "障碍",
    "bug",
    "risk",
    "error",
]
TASK_KEYWORDS = [
    "todo",
    "待办",
    "任务",
    "记得",
    "请",
    "需要",
    "下一步",
    "跟进",
    "联系",
    "检查",
    "安排",
    "写",
    "更新",
    "准备",
    "修复",
    "完成",
    "整理",
    "回复",
]

EMOTION_KEYWORDS = [
    "生气", "很气", "气死", "愤怒", "怒", "火大", "烦", "讨厌", "不爽", "不满", "不满意", "失望", "很失望", "不开心", "生我的气",
    "太烂", "很差", "不好", "糟糕", "受不了", "别再", "不要再", "不可以", "禁止", "不准",
]
PREFERENCE_KEYWORDS = [
    "喜欢", "不喜欢", "希望", "想要", "必须", "需要", "一定", "以后", "永远", "记住", "别忘", "不要", "只能", "请你",
]
IMMEDIATE_KEYWORDS = [
    "现在就", "马上", "立刻", "今天就", "务必", "必须", "非常",
]

EMOTION_LOWER = [keyword.lower() for keyword in EMOTION_KEYWORDS]
PREFERENCE_LOWER = [keyword.lower() for keyword in PREFERENCE_KEYWORDS]
IMMEDIATE_LOWER = [keyword.lower() for keyword in IMMEDIATE_KEYWORDS]

DEFAULT_TODOS_CONTENT = textwrap.dedent("""\
    # TODOs（主人未完成事项清单）

    > 规则：这里是“唯一真相源”。ちぃ会在心跳/复盘中持续更新状态，不会写完就丢。

    ## 🔥 Active（进行中）

    ## ⏳ Waiting（等主人/等外部条件）

    ## ✅ Done（已完成，保留最近 20 条）

""")

KEYWORDS_LOWER = [keyword.lower() for keyword in KEYWORDS]
DECISION_LOWER = [keyword.lower() for keyword in DECISION_KEYWORDS]
RISK_LOWER = [keyword.lower() for keyword in RISK_KEYWORDS]
TASK_LOWER = [keyword.lower() for keyword in TASK_KEYWORDS]

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


def _tail_lines(path: Path, limit: int) -> list[str]:
    dq: deque[str] = deque(maxlen=limit)
    if not path.exists():
        return []
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            dq.append(line.rstrip("\n"))
    return list(dq)


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


def _parse_session_lines(lines: Iterable[str]) -> list[dict]:
    parsed = []
    for raw in lines:
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "message":
            continue
        message = entry.get("message") or {}
        role = message.get("role")
        text = _extract_text(message.get("content")) or _extract_text(message.get("text"))
        if not text:
            continue
        parsed.append({
            "role": role,
            "text": text,
            "timestamp": entry.get("timestamp") or message.get("timestamp"),
        })
    return parsed


def _split_sentences(text: str) -> list[str]:
    chunks = SENTENCE_SPLIT_REGEX.split(text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _sentence_candidates(texts: Sequence[str]) -> list[str]:
    candidates = []
    for text in texts:
        for sentence in _split_sentences(text):
            lowered = sentence.lower()
            if any(keyword in lowered for keyword in KEYWORDS_LOWER):
                candidates.append(sentence)
    return candidates


def _truncate(text: str, limit: int = 180) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _append_memory(candidates: Sequence[str], stamp: str) -> bool:
    if not candidates:
        return False
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = MEMORY_FILE.read_text(encoding="utf-8") if MEMORY_FILE.exists() else ""
    unique: list[str] = []
    for sentence in candidates:
        candidate = f"- {sentence}"
        if candidate in existing:
            continue
        unique.append(candidate)
    if not unique:
        return False
    block = ["", f"## 自动会话钩子（{stamp}）"] + unique
    with MEMORY_FILE.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(block))
        handle.write("\n")
    return True


def _ensure_daily_file(date_str: str) -> Path:
    target = TODAY_MEMORY_DIR / f"{date_str}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(f"# 记忆日志 {date_str}\n\n", encoding="utf-8")
    return target


def _ensure_now_file() -> Path:
    target = NOW_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("# NOW（滚动短期记忆）\n\n", encoding="utf-8")
    return target


def _append_now(user_texts: Sequence[str], stamp: str, session_id: str) -> bool:
    if not user_texts:
        return False
    now_file = _ensure_now_file()
    block = ["", f"## {stamp} session {session_id[:8]}"]
    for idx, text in enumerate(user_texts, 1):
        block.append(f"- {idx}. {text}")
    with now_file.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(block))
        handle.write("\n")
    return True


def _append_daily_user_log(user_texts: Sequence[str], stamp: str, session_id: str) -> None:
    if not user_texts:
        return
    daily = _ensure_daily_file(datetime.now(TOKYO_TZ).date().isoformat())
    block = ["", f"### 用户原话（session {session_id[:8]} @ {stamp}）"]
    for idx, text in enumerate(user_texts, 1):
        block.append(f"- {idx}. {text}")
    block.append("")
    with daily.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(block))


def _priority_candidates(texts: Sequence[str]) -> list[str]:
    candidates: list[str] = []
    for text in texts:
        for sentence in _split_sentences(text):
            lowered = sentence.lower()
            if any(keyword in lowered for keyword in EMOTION_LOWER):
                candidates.append(sentence)
                continue
            if any(keyword in lowered for keyword in PREFERENCE_LOWER):
                candidates.append(sentence)
                continue
            if any(keyword in lowered for keyword in IMMEDIATE_LOWER):
                candidates.append(sentence)
                continue
    return candidates


def _append_daily_log(summary: str, decision: str, risk: str, todos: str, stamp: str) -> None:
    daily = _ensure_daily_file(datetime.now(TOKYO_TZ).date().isoformat())
    lines = [
        f"- [{stamp}] Summary: {summary}",
        f"- [{stamp}] Decision: {decision}",
        f"- [{stamp}] Risk/Pitfall: {risk}",
        f"- [{stamp}] Open todo: {todos}",
        "",
    ]
    with daily.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(f"{line}\n")


def _extract_tasks(texts: Sequence[str]) -> list[str]:
    tasks: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for sentence in _split_sentences(text):
            lowered = sentence.lower()
            if any(keyword in lowered for keyword in TASK_LOWER):
                normalized = sentence.strip()
                if len(normalized) > 200:
                    normalized = normalized[:197].rstrip() + "…"
                if normalized in seen:
                    continue
                seen.add(normalized)
                tasks.append(normalized)
    return tasks


def _compose_summary(texts: Sequence[str], last: str, current: str) -> str:
    if not texts:
        return f"Session {last[:8]} → {current[:8]} 结束；提交的尾部没有用户对话。"
    snippets = [ _truncate(item) for item in texts[-3:] ]
    joined = " | ".join(snippets)
    return f"Session {last[:8]} → {current[:8]} 结尾片段：{joined}"


def _choose_sentence(texts: Sequence[str], lookups: Sequence[str], default: str) -> str:
    for text in reversed(texts[-6:]):
        for sentence in _split_sentences(text):
            lowered = sentence.lower()
            if any(keyword in lowered for keyword in lookups):
                return _truncate(sentence, 260)
    return default


def _compose_decision(texts: Sequence[str]) -> str:
    default = "⚠️ 本次会话没有明确的“决定/计划”描述。"
    return _choose_sentence(texts, DECISION_LOWER, default)


def _compose_risk(texts: Sequence[str]) -> str:
    default = "⚠️ 回顾依赖最后 200 行记录，可能遗漏更早的上下文；如有疑问请补充。"
    return _choose_sentence(texts, RISK_LOWER, default)


def _compose_todo_field(tasks: Sequence[str]) -> str:
    if not tasks:
        return "暂无新增 todo。"
    snippet = "；".join(tasks[:3])
    return f"{snippet}（已同步到 TODOs）"


def _split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections = {"pre": [], "active": [], "waiting": [], "done": []}
    current = "pre"
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("## 🔥 Active"):
            current = "active"
        elif stripped.startswith("## ⏳ Waiting"):
            current = "waiting"
        elif stripped.startswith("## ✅ Done"):
            current = "done"
        sections[current].append(line)
    return sections


def _ensure_section_header(section: list[str], header: str) -> None:
    if not section:
        section.extend([header, ""])
    elif not section[0].strip().startswith("##"):
        section.insert(0, "")
        section.insert(0, header)


def _insert_done_entry(done_lines: list[str], entry: str) -> None:
    _ensure_section_header(done_lines, "## ✅ Done（已完成，保留最近 20 条）")
    insert_idx = 1
    while insert_idx < len(done_lines) and done_lines[insert_idx].strip() == "":
        insert_idx += 1
    done_lines.insert(insert_idx, "")
    done_lines.insert(insert_idx, entry)


def _prune_done_entries(done_lines: list[str], limit: int = 20) -> None:
    entry_indices = [idx for idx, line in enumerate(done_lines) if line.strip().startswith("- [x]")]
    if len(entry_indices) <= limit:
        return
    for idx in reversed(entry_indices[limit:]):
        if 0 <= idx < len(done_lines):
            done_lines.pop(idx)
            if idx < len(done_lines) and done_lines[idx].strip() == "":
                done_lines.pop(idx)


def _remove_hook_entry(active_lines: list[str], session_id: str) -> bool:
    pattern = re.compile(rf"- \[ \] Hooked session {re.escape(session_id)}")
    for idx, line in enumerate(active_lines):
        if pattern.search(line):
            active_lines.pop(idx)
            if idx < len(active_lines) and active_lines[idx].strip() == "":
                active_lines.pop(idx)
            return True
    return False


def _insert_active_tasks(active_lines: list[str], tasks: Sequence[str], session_id: str) -> bool:
    if not tasks:
        return False
    _ensure_section_header(active_lines, "## 🔥 Active（进行中）")
    insert_idx = 1
    while insert_idx < len(active_lines) and active_lines[insert_idx].strip() == "":
        insert_idx += 1
    added = False
    limit = MAX_TODO_UPDATES
    for task in tasks[:limit]:
        normalized = task.strip()
        if not normalized:
            continue
        entry = f"- [ ] {normalized}（来自 session {session_id[:8]}）"
        if any(normalized in line for line in active_lines):
            continue
        active_lines.insert(insert_idx, "")
        active_lines.insert(insert_idx, entry)
        insert_idx += 2
        added = True
    return added


def _log_session_done(done_lines: list[str], session_id: str, stamp: str) -> bool:
    marker = f"session {session_id}"
    for line in done_lines:
        if marker in line:
            return False
    entry = f"- [x] Hooked session {session_id}（自动总结于 {stamp}）"
    _insert_done_entry(done_lines, entry)
    return True


def _serialize_sections(sections: dict[str, list[str]]) -> list[str]:
    ordered: list[str] = []
    for key in ["pre", "active", "waiting", "done"]:
        ordered.extend(sections[key])
    # Ensure there is a trailing blank line before serialization
    if ordered and ordered[-1].strip() != "":
        ordered.append("")
    return ordered


def _update_todos(session_id: str, stamp: str, tasks: Sequence[str]) -> bool:
    if not TODOS_FILE.exists():
        lines = DEFAULT_TODOS_CONTENT.rstrip().split("\n")
    else:
        lines = TODOS_FILE.read_text(encoding="utf-8").split("\n")
    sections = _split_sections(lines)
    _ensure_section_header(sections["active"], "## 🔥 Active（进行中）")
    _ensure_section_header(sections["waiting"], "## ⏳ Waiting（等主人/等外部条件）")
    _ensure_section_header(sections["done"], "## ✅ Done（已完成，保留最近 20 条）")

    removed = _remove_hook_entry(sections["active"], session_id)
    moved = removed and _log_session_done(sections["done"], session_id, stamp)
    if not removed:
        # still log even if there was no active entry
        logged = _log_session_done(sections["done"], session_id, stamp)
        moved = moved or logged
    added_tasks = _insert_active_tasks(sections["active"], tasks, session_id)
    _prune_done_entries(sections["done"])

    if not (moved or removed or added_tasks):
        return False
    ordered = _serialize_sections(sections)
    TODOS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TODOS_FILE.write_text("\n".join(ordered).rstrip() + "\n", encoding="utf-8")
    return True


def _iso_stamp_from_timestamp(ts: str | int | float | None) -> str:
    if ts is None:
        now = datetime.now(TOKYO_TZ)
    else:
        try:
            ts_float = float(ts)
            if ts_float > 1e10:
                ts_float /= 1000.0
            now = datetime.fromtimestamp(ts_float, timezone.utc).astimezone(TOKYO_TZ)
        except Exception:
            now = datetime.now(TOKYO_TZ)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    sessions = _load_json(SESSIONS_JSON)
    current = sessions.get("agent:main:main", {}).get("sessionId")
    if not current:
        print("NO_REPLY")
        return
    watch = _load_json(WATCH_FILE)
    last = watch.get("lastSessionId")
    if not last:
        _write_json(
            WATCH_FILE,
            {"lastSessionId": current, "updatedAt": int(time.time())},
        )
        print("NO_REPLY")
        return
    if current == last:
        print("NO_REPLY")
        return

    log_path = SESSION_DIR / f"{last}.jsonl"
    lines = _tail_lines(log_path, MAX_TAIL_LINES)
    messages = _parse_session_lines(lines)
    user_texts = [msg["text"] for msg in messages if msg.get("role") == "user"]
    stamp = _iso_stamp_from_timestamp(messages[-1].get("timestamp") if messages else None)

    _append_now(user_texts, stamp, last)
    _append_daily_user_log(user_texts, stamp, last)

    summary = _compose_summary(user_texts, last, current)
    decision = _compose_decision(user_texts)
    risk = _compose_risk(user_texts)
    tasks = _extract_tasks(user_texts)
    todos_field = _compose_todo_field(tasks)

    priority = _priority_candidates(user_texts)
    candidates = _sentence_candidates(user_texts)
    merged = []
    for item in priority + candidates:
        if item not in merged:
            merged.append(item)
    if merged:
        _append_memory(merged, stamp)
    _append_daily_log(summary, decision, risk, todos_field, stamp)
    _update_todos(last, stamp, tasks)

    _write_json(
        WATCH_FILE,
        {"lastSessionId": current, "updatedAt": int(time.time())},
    )
    print("NO_REPLY")


if __name__ == "__main__":
    main()
