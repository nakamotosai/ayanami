#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
from pathlib import Path

RUNS_DIR = Path("/home/ubuntu/.openclaw/cron/runs")
STATE_FILE = Path("/home/ubuntu/.openclaw/cron/cron-failure-state.json")
OPENCLAW_CLI = Path("/home/ubuntu/.npm-global/bin/openclaw")
NOTIFY_TARGET = "8138445887"
WINDOW_SEC = 3600

ERROR_PATTERNS = [
    re.compile(r"\bHTTP\s*[45]\d{2}\b", re.IGNORECASE),
    re.compile(r"\b(error|failed|exception|invalid|unauthorized|forbidden)\b", re.IGNORECASE),
]

IGNORED_SUMMARY_PATTERNS = [
    re.compile(r"Unsupported channel", re.IGNORECASE),
]


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iter_runs():
    if not RUNS_DIR.exists():
        return
    for path in RUNS_DIR.glob("*.jsonl"):
        try:
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if not line.strip():
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
        except FileNotFoundError:
            continue


def send_message(message: str) -> None:
    if not OPENCLAW_CLI.exists():
        return
    import subprocess

    subprocess.run(
        [
            str(OPENCLAW_CLI),
            "message",
            "send",
            "--channel",
            "telegram",
            "--target",
            NOTIFY_TARGET,
            "--message",
            message,
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def is_error_summary(summary: str) -> bool:
    if not summary:
        return False
    return any(pattern.search(summary) for pattern in ERROR_PATTERNS)


def is_ignored_summary(summary: str) -> bool:
    if not summary:
        return False
    return any(pattern.search(summary) for pattern in IGNORED_SUMMARY_PATTERNS)


def main() -> None:
    now_ms = int(time.time() * 1000)
    cutoff_ms = now_ms - WINDOW_SEC * 1000
    state = load_state()
    notified = False

    for run in iter_runs():
        if run.get("action") != "finished":
            continue
        status = (run.get("status") or "").lower()
        summary = run.get("summary") or ""
        errorish = status != "ok" or is_error_summary(summary)
        if not errorish:
            continue
        if is_ignored_summary(summary):
            continue
        ts = int(run.get("ts", 0) or 0)
        if ts < cutoff_ms:
            continue
        job_id = run.get("jobId") or "unknown"
        last_notified = int(state.get(job_id, 0) or 0)
        if ts <= last_notified:
            continue
        message = f"Cron 异常：job={job_id}\nstatus={status}\nsummary={summary or '(no summary)'}"
        send_message(message)
        state[job_id] = ts
        notified = True

    if notified:
        save_state(state)


if __name__ == "__main__":
    main()
