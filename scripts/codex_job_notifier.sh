#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
JOBDIR="$WS/logs/codex/jobs"

if [[ ! -d "$JOBDIR" ]]; then
  exit 0
fi

# Notify for completed jobs that haven\x27t been notified.
for jf in "$JOBDIR"/codex-*.json; do
  [[ -f "$jf" ]] || continue
  status=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$jf").read_text(encoding="utf-8"))
print(obj.get("status",""))
PY
)
  notified=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$jf").read_text(encoding="utf-8"))
print(obj.get("notified",""))
PY
)
  if [[ "$status" != "done" || "$notified" == "true" ]]; then
    continue
  fi

  chat_id=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$jf").read_text(encoding="utf-8"))
print(obj.get("chatId", ""))
PY
)
  last_msg=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$jf").read_text(encoding="utf-8"))
print(obj.get("lastMsg", ""))
PY
)
  job_id=$(python3 - <<PY
import json
from pathlib import Path
obj=json.loads(Path("$jf").read_text(encoding="utf-8"))
print(obj.get("jobId", ""))
PY
)

  if [[ -z "$chat_id" || -z "$last_msg" || ! -f "$last_msg" ]]; then
    continue
  fi

  sum=$(head -c 3500 "$last_msg")
  bash "$WS/scripts/telegram_send.sh" "$chat_id" "[Codex 完成] $job_id\n\n$sum\n\n(文件: $last_msg)" || true

  python3 - <<PY
import json
from pathlib import Path
p=Path("$jf")
obj=json.loads(p.read_text(encoding="utf-8"))
obj["notified"] = True
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
PY

done
