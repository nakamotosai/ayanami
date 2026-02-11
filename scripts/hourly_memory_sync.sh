#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/home/ubuntu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$MEMORY_DIR/system-change.log"
HASH_FILE="$MEMORY_DIR/.core_hashes.json"

files=(
  "$WORKSPACE/AGENTS.md"
  "$WORKSPACE/SOUL.md"
  "$WORKSPACE/USER.md"
  "$WORKSPACE/TOOLS.md"
  "$WORKSPACE/MEMORY.md"
)

python3 - <<'PY' "$HASH_FILE" "$LOG_FILE" "$TODAY" "${files[@]}"
import json
import sys
from pathlib import Path
from hashlib import sha256

hash_path = Path(sys.argv[1])
log_path = Path(sys.argv[2])
today = sys.argv[3]
files = [Path(p) for p in sys.argv[4:]]

prev = {}
if hash_path.exists():
    try:
        prev = json.loads(hash_path.read_text(encoding='utf-8'))
    except Exception:
        prev = {}

changed = []
current = {}
for f in files:
    if not f.exists():
        continue
    data = f.read_bytes()
    digest = sha256(data).hexdigest()
    current[str(f)] = digest
    if prev.get(str(f)) != digest:
        changed.append(str(f))

hash_path.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding='utf-8')

if changed:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        log_path.read_text(encoding='utf-8') + f"{today} changed: " + ", ".join(changed) + "\n"
        if log_path.exists() else f"{today} changed: " + ", ".join(changed) + "\n",
        encoding='utf-8'
    )
PY
