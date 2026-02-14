#!/usr/bin/env bash
set -euo pipefail

JOBDIR="$HOME/.openclaw/workspace/logs/codex/jobs"
[[ -d "$JOBDIR" ]] || { echo "NO_JOBDIR"; exit 0; }

python3 - <<'PY'
import json, time
from pathlib import Path

jobdir = Path.home()/'.openclaw/workspace/logs/codex/jobs'
rows=[]
now=time.time()
for jf in sorted(jobdir.glob('codex-*.json'), reverse=True)[:30]:
    try:
        o=json.loads(jf.read_text(encoding='utf-8'))
    except Exception:
        continue
    age=int(now-jf.stat().st_mtime)
    rows.append({
        'jobId': o.get('jobId', jf.stem),
        'status': o.get('status',''),
        'notified': o.get('notified', False),
        'pid': o.get('runnerPid', 0) or 0,
        'age': age,
        'createdAtUtc': o.get('createdAtUtc',''),
    })
for r in rows:
    print(f"{r['jobId']}\t{r['status']}\tnotified={str(r['notified']).lower()}\tpid={r['pid']}\tage_s={r['age']}\t{r['createdAtUtc']}")
PY
