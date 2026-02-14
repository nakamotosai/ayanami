#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
JOBDIR="$WS/logs/codex/jobs"

[[ -d "$JOBDIR" ]] || exit 0

for jf in "$JOBDIR"/codex-*.json; do
  [[ -f "$jf" ]] || continue

  status=$(python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(obj.get('status',''))
PY
)

  notified=$(python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(str(obj.get('notified','')))
PY
)

  if [[ "$status" != "done" || "$notified" == "True" || "$notified" == "true" ]]; then
    continue
  fi

  chat_id=$(python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(obj.get('chatId',''))
PY
)

  last_msg=$(python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(obj.get('lastMsg',''))
PY
)

  job_id=$(python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(obj.get('jobId',''))
PY
)

  [[ -n "$chat_id" && -n "$last_msg" && -f "$last_msg" ]] || continue

  sum=$(python3 - "$last_msg" <<'PY'
import sys
from pathlib import Path
s=Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')
print(s[:3500])
PY
)

  msg=$(printf "[Codex 完成] %s\n\n%s\n\n(文件: %s)" "$job_id" "$sum" "$last_msg")

  if bash "$WS/scripts/telegram_send.sh" "$chat_id" "$msg"; then
    python3 - "$jf" <<'PY'
import json, sys
from pathlib import Path
p=Path(sys.argv[1])
obj=json.loads(p.read_text(encoding='utf-8'))
obj['notified']=True
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
PY
    echo "SENT: $job_id"
  else
    echo "SEND_FAILED: $job_id" >&2
  fi

done
