#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WS = Path.home() / ".openclaw" / "workspace"
RAW_ROOT = WS / "memory" / "raw" / "telegram"
DAILY_DIR = WS / "memory"
LONG = WS / "MEMORY.md"
STATE = WS / "memory" / "state" / "evolve_hourly.json"

# Only write long-term when it's clearly stable preference/rule/ban/identity fact.
PREF_PAT = re.compile(r"(偏好|喜欢|讨厌|不要|必须|默认|以后|永远|请用|别再|我希望|我需要)")

MAX_NEW_LONG = 8


def utc_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state():
    if not STATE.exists():
        return {"lastRunAt": 0}
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")


def iter_recent_raw_lines(since_ts: float):
    if not RAW_ROOT.exists():
        return
    for peer_dir in sorted(RAW_ROOT.glob("*/")):
        for f in sorted(peer_dir.glob("*.jsonl")):
            try:
                for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    ts_ms = obj.get("ts") or obj.get("tsMs") or obj.get("createdAtMs")
                    ts = (ts_ms / 1000.0) if isinstance(ts_ms, (int, float)) else 0
                    if ts and ts >= since_ts:
                        yield (f, obj, ts)
            except Exception:
                continue


def extract_user_text(obj: dict):
    # Conservative: try top-level and common nested payload fields
    text = obj.get("text") if isinstance(obj.get("text"), str) else None
    from_id = obj.get("from") if isinstance(obj.get("from"), str) else None
    payload = obj.get("payload") or obj.get("message") or obj.get("event")
    if isinstance(payload, dict):
        if not text and isinstance(payload.get("text"), str):
            text = payload.get("text")
        if not from_id and isinstance(payload.get("from"), str):
            from_id = payload.get("from")
    if from_id != "telegram:8138445887":
        return None
    if not text:
        return None
    return text.strip()


def load_long_lines_set():
    if not LONG.exists():
        return set()
    seen = set()
    for line in LONG.read_text(encoding="utf-8", errors="ignore").splitlines():
        t = line.strip()
        if t.startswith("-"):
            seen.add(t)
    return seen


def append_long(entries):
    if not entries:
        return
    LONG.parent.mkdir(parents=True, exist_ok=True)
    with LONG.open("a", encoding="utf-8") as f:
        f.write("\n## Auto-evolve (hourly)\n")
        for e in entries:
            f.write(f"- {e}\n")


def run_cmd(cmd: list[str]):
    import subprocess

    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    st = load_state()
    last = float(st.get("lastRunAt", 0))

    long_seen = load_long_lines_set()
    new_long = []

    for f, obj, ts in iter_recent_raw_lines(last):
        text = extract_user_text(obj)
        if not text:
            continue
        if not PREF_PAT.search(text):
            continue

        # Normalize bullet content
        candidate = text
        candidate = re.sub(r"\s+", " ", candidate).strip()
        bullet = f"- {candidate}"
        if bullet in long_seen:
            continue

        # Add minimal provenance (file + ts) to keep it auditable.
        prov = f"{candidate} (src:{f.name}@{utc_iso(ts)})"
        bullet2 = f"- {prov}"
        if bullet2 in long_seen:
            continue
        new_long.append(prov)
        long_seen.add(bullet2)
        if len(new_long) >= MAX_NEW_LONG:
            break

    append_long(new_long)

    # Re-index for search
    run_cmd(["qmd", "update"])

    st["lastRunAt"] = datetime.now(tz=timezone.utc).timestamp()
    st["lastAdded"] = len(new_long)
    save_state(st)

    print(json.dumps({"ok": True, "added": len(new_long)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
