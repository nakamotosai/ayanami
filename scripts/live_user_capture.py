from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

BASE_DIR = Path("/home/ubuntu/.openclaw")
WORKSPACE = BASE_DIR / "workspace"
AGENTS_ROOT = BASE_DIR / "agents"
STATE_FILE = WORKSPACE / "memory" / "live_capture_state.json"
NOW_FILE = WORKSPACE / "memory" / "NOW.md"
TOKYO_TZ = timezone(timedelta(hours=9))

PREF_KW = ["喜欢", "不喜欢", "希望", "想要", "必须", "需要", "请你", "不要", "只能", "记住", "偏好", "规则"]


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
        NOW_FILE.write_text("# NOW（滚动短期记忆·摘要）\n\n", encoding="utf-8")


def _ensure_daily_file(date_str: str) -> Path:
    target = WORKSPACE / "memory" / f"{date_str}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(f"# 记忆日志 {date_str}（摘要）\n\n", encoding="utf-8")
    return target


def _extract_text(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if content.get("type") == "text":
            return content.get("text", "")
        return _extract_text(content.get("content") or content.get("text"))
    if isinstance(content, list):
        return "".join(_extract_text(item) for item in content)
    return ""


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


def main() -> None:
    state = _load_json(STATE_FILE)
    offsets = state.get("offsets", {}) if isinstance(state.get("offsets"), dict) else {}

    collected: list[tuple[str, str, str]] = []
    for agent_name, session_file in _iter_session_files():
        key = f"{agent_name}:{session_file.stem}"
        lines = session_file.read_text(encoding="utf-8", errors="ignore").splitlines()

        if key not in offsets:
            # First seen: pin cursor at EOF to avoid importing stale history.
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
                node = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if node.get("type") != "message":
                continue
            message = node.get("message") or {}
            if message.get("role") != "user":
                continue
            text = _extract_text(message.get("content")) or _extract_text(message.get("text"))
            if text:
                collected.append((agent_name, session_file.stem, text))

        offsets[key] = len(lines)

    state["offsets"] = offsets
    state["updatedAt"] = int(datetime.now(TOKYO_TZ).timestamp())
    _save_json(STATE_FILE, state)

    if not collected:
        return

    stamp = datetime.now(TOKYO_TZ).strftime("%Y-%m-%dT%H:%M:%SZ")
    _ensure_now_file()
    daily = _ensure_daily_file(datetime.now(TOKYO_TZ).date().isoformat())

    prefs = [f"[{a}] {t}" for (a, _, t) in collected if any(k in t for k in PREF_KW)]
    prefs = prefs[-8:]
    last_msgs = [f"[{a}] {t}" for (a, _, t) in collected[-8:]]

    by_agent: dict[str, int] = {}
    for a, _, _ in collected:
        by_agent[a] = by_agent.get(a, 0) + 1

    now_block = ["", f"## {stamp} cross-agent", f"- 本次新增用户消息条数: {len(collected)}"]
    if by_agent:
        now_block.append("- 来源 agent:")
        for name in sorted(by_agent):
            now_block.append(f"  - {name}: {by_agent[name]}")
    if prefs:
        now_block.append("- 偏好类要点:")
        for p in prefs:
            now_block.append(f"  - {p[:140]}")
    now_block.append("- 最近用户消息摘要:")
    for m in last_msgs:
        now_block.append(f"  - {m[:140]}")
    now_block.append("")
    NOW_FILE.open("a", encoding="utf-8").write("\n".join(now_block))

    daily_block = ["", f"## {stamp} 跨 agent 摘要", f"- 新增用户消息: {len(collected)} 条"]
    for m in last_msgs:
        daily_block.append(f"- {m[:140]}")
    daily_block.append("")
    daily.open("a", encoding="utf-8").write("\n".join(daily_block))


if __name__ == "__main__":
    main()
