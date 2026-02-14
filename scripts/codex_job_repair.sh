#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
JOBDIR="$WS/logs/codex/jobs"
LOGDIR="$WS/logs/codex"

[[ -d "$JOBDIR" ]] || exit 0

python3 - <<'PY'
import json, os, time
from pathlib import Path

ws = Path.home()/".openclaw"/"workspace"
jobdir = ws/"logs"/"codex"/"jobs"
logdir = ws/"logs"/"codex"

now = time.time()
fixed = 0
failed = 0

for jf in sorted(jobdir.glob("codex-*.json")):
    try:
        obj = json.loads(jf.read_text(encoding="utf-8"))
    except Exception:
        continue

    if obj.get("status") != "running":
        continue

    job_id = obj.get("jobId") or jf.stem
    ts = job_id.replace("codex-", "")
    last = logdir / f"last-{ts}.md"

    # Case 1: completed artifact exists
    if last.exists():
        obj["status"] = "done"
        obj.setdefault("notified", False)
        obj["lastMsg"] = str(last)
        obj.setdefault("finishedAtUtc", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(last.stat().st_mtime)))
        jf.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        fixed += 1
        continue

    # Case 2: runner pid exists but process is gone => fail
    pid = obj.get("runnerPid")
    if isinstance(pid, int) and pid > 0:
        alive = True
        try:
            os.kill(pid, 0)
        except Exception:
            alive = False
        if not alive:
            obj["status"] = "failed"
            obj["failedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
            obj["failReason"] = "runner_exited_without_lastMsg"
            jf.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
            failed += 1
            continue

    # Case 3: no pid and job is stale
    age = now - jf.stat().st_mtime
    if age > 600:
        obj["status"] = "failed"
        obj["failedAtUtc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        obj["failReason"] = "stale_running_no_pid"
        jf.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        failed += 1

print(json.dumps({"fixed": fixed, "failed": failed}, ensure_ascii=False))
PY

bash "$WS/scripts/codex_job_notifier.sh" || true
