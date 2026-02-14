#!/usr/bin/env bash
set -euo pipefail

JOB_ID=${1:-}
if [[ -z "$JOB_ID" ]]; then
  echo "usage: $0 <job_id>" >&2
  exit 2
fi

JF="$HOME/.openclaw/workspace/logs/codex/jobs/${JOB_ID}.json"
if [[ ! -f "$JF" ]]; then
  echo "NOT_FOUND: $JF" >&2
  exit 1
fi

PID=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$JF").read_text(encoding='utf-8'))
print(obj.get('runnerPid',0) or 0)
PY
)

if [[ "$PID" -gt 0 ]] && kill -0 "$PID" 2>/dev/null; then
  kill "$PID" || true
fi

python3 - <<PY
import json, time
from pathlib import Path
p=Path("$JF")
obj=json.loads(p.read_text(encoding='utf-8'))
obj['status']='canceled'
obj['canceledAtUtc']=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
PY

echo "CANCELED: $JOB_ID pid=$PID"
