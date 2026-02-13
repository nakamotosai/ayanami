#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WS = Path.home() / ".openclaw" / "workspace"
SESSIONS_JSON = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
STATE_DIR = WS / "memory" / "state"
RAW_DIR = WS / "memory" / "raw" / "telegram"

LONG_MEMORY = WS / "MEMORY.md"

TRIGGERS = (
    "请记住",
    "记住:",
    "记住：",
)

# Conservative extraction: only store obvious user text messages.

def _utc_iso(ts_ms: int) -> str:
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today_local() -> str:
    # Use local timezone on the VPS; you configured Asia/Tokyo in user prefs,
    # but file naming can stay local. It's fine; content is UTC-stamped.
    return datetime.now().strftime("%Y-%m-%d")


def _load_sessions_meta() -> dict:
    return json.loads(SESSIONS_JSON.read_text(encoding="utf-8"))


def _pick_current_telegram_direct(meta: dict) -> dict:
    # Prefer main session record
    rec = meta.get("agent:main:main")
    if not rec:
        raise RuntimeError("sessions.json missing agent:main:main")
    if rec.get("lastChannel") != "telegram":
        raise RuntimeError(f"lastChannel is not telegram: {rec.get('lastChannel')}")
    if rec.get("chatType") != "direct":
        raise RuntimeError(f"chatType is not direct: {rec.get('chatType')}")
    return rec


def _state_path(session_id: str) -> Path:
    return STATE_DIR / f"telegram_direct_{session_id}.json"


def _load_state(session_id: str) -> dict:
    p = _state_path(session_id)
    if not p.exists():
        return {"sessionId": session_id, "lastOffset": 0}
    return json.loads(p.read_text(encoding="utf-8"))


def _save_state(session_id: str, last_offset: int) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    p = _state_path(session_id)
    p.write_text(json.dumps({"sessionId": session_id, "lastOffset": last_offset}, indent=2), encoding="utf-8")


def _append_raw(peer: str, line: str, ts_ms: int) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    day = _today_local()
    out = RAW_DIR / peer / f"{day}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8") if not out.exists() else None
    with out.open("a", encoding="utf-8") as f:
        f.write(line)
        if not line.endswith("\n"):
            f.write("\n")


def _append_daily(text: str, ts_ms: int) -> None:
    day = _today_local()
    p = WS / "memory" / f"{day}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = _utc_iso(ts_ms)
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts}\n")
        for line in text.strip().splitlines():
            f.write(f"- {line.strip()}\n")


def _write_long_memory(entry: str, ts_ms: int) -> None:
    ts = _utc_iso(ts_ms)
    with LONG_MEMORY.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts}\n")
        f.write(f"- {entry.strip()}\n")


def _run(cmd: list[str]) -> None:
    import subprocess

    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    if not SESSIONS_JSON.exists():
        print(f"MISSING: {SESSIONS_JSON}", file=sys.stderr)
        return 1

    meta = _load_sessions_meta()
    rec = _pick_current_telegram_direct(meta)
    session_id = rec["sessionId"]
    session_file = Path(rec["sessionFile"])

    state = _load_state(session_id)
    last_offset = int(state.get("lastOffset", 0))

    if not session_file.exists():
        print(f"MISSING: {session_file}", file=sys.stderr)
        return 1

    peer = rec.get("lastTo", "telegram:unknown").replace(":", "_")

    new_user_msgs = 0
    promoted = 0

    with session_file.open("rb") as bf:
        bf.seek(last_offset)
        while True:
            line_bytes = bf.readline()
            if not line_bytes:
                break
            last_offset = bf.tell()

            try:
                line = line_bytes.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                obj = json.loads(line)
            except Exception:
                continue

            # Store raw line regardless; we only process user-facing content if it looks like a user message.
            ts_ms = obj.get("ts") or obj.get("tsMs") or obj.get("createdAtMs") or int(datetime.now(tz=timezone.utc).timestamp() * 1000)
            _append_raw(peer, line, int(ts_ms))

            # Heuristic: look for message events that include text and a telegram from.
            # We keep it permissive to avoid missing, but still require 'text' and from prefix.
            from_id = None
            text = None
            if isinstance(obj, dict):
                # Common shapes we observed in OpenClaw logs
                if "from" in obj and isinstance(obj["from"], str):
                    from_id = obj["from"]
                if "text" in obj and isinstance(obj["text"], str):
                    text = obj["text"]
                # nested payload
                if not text:
                    payload = obj.get("payload") or obj.get("message") or obj.get("event")
                    if isinstance(payload, dict):
                        if not from_id and isinstance(payload.get("from"), str):
                            from_id = payload.get("from")
                        if isinstance(payload.get("text"), str):
                            text = payload.get("text")

            if not text:
                continue

            # Only user (your Telegram peer) messages.
            # sessions.json uses telegram:8138445887; we match that.
            if from_id != "telegram:8138445887":
                continue

            new_user_msgs += 1
            _append_daily(text, int(ts_ms))

            stripped = text.strip()
            if stripped.startswith(TRIGGERS):
                entry = stripped
                # Normalize: remove trigger prefix
                for t in TRIGGERS:
                    if entry.startswith(t):
                        entry = entry[len(t):].strip()
                        break
                if entry:
                    _write_long_memory(entry, int(ts_ms))
                    promoted += 1

    _save_state(session_id, last_offset)

    # Reindex after changes
    _run(["qmd", "update"])

    print(json.dumps({
        "sessionId": session_id,
        "sessionFile": str(session_file),
        "peer": peer,
        "newUserMessages": new_user_msgs,
        "promotedToLong": promoted,
        "lastOffset": last_offset,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
