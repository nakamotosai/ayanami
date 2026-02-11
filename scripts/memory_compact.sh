#!/usr/bin/env bash
set -euo pipefail
MEMORY_FILE="/home/ubuntu/.openclaw/workspace/MEMORY.md"
MAX_CHARS=4000
if [[ ! -f "$MEMORY_FILE" ]]; then
  exit 0
fi
python3 - <<'PY'
from pathlib import Path
MAX_CHARS = 4000
p = Path("/home/ubuntu/.openclaw/workspace/MEMORY.md")
text = p.read_text(encoding="utf-8")
if len(text) <= MAX_CHARS:
    raise SystemExit(0)
text = text[: MAX_CHARS - 1].rstrip() + "…\n"
p.write_text(text, encoding="utf-8")
PY