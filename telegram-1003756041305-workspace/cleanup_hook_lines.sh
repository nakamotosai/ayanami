#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"
LOG_FILE="$WORKSPACE_DIR/workspace installer/cleanup_hook_lines.log"

if [[ ! -d "$MEMORY_DIR" ]]; then
  exit 0
fi

mapfile -t files < <(find "$MEMORY_DIR" -maxdepth 1 -type f -name "*.md" -print | sort)
if [[ ${#files[@]} -eq 0 ]]; then
  exit 0
fi

changed_count=0
scanned_count=0
changed_files=()

for file in "${files[@]}"; do
  scanned_count=$((scanned_count + 1))
  if ! grep -q "Hook captured new session" "$file"; then
    continue
  fi

  tmp_file="${file}.tmp"
  # Remove only the auto-generated hook lines, keep other markdown intact.
  # Preserve trailing newline if present.
  python3 - <<'PY' "$file" "$tmp_file"
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
text = src.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
filtered = [ln for ln in lines if "Hook captured new session" not in ln]
if not filtered:
    # Avoid writing an empty file unless original was empty.
    out.write_text("", encoding="utf-8")
else:
    out.write_text("".join(filtered), encoding="utf-8")
PY

  if ! cmp -s "$file" "$tmp_file"; then
    mv "$tmp_file" "$file"
    changed_count=$((changed_count + 1))
    changed_files+=("$(basename "$file")")
  else
    rm -f "$tmp_file"
  fi

done

if [[ $changed_count -gt 0 ]]; then
  ts="$(date '+%Y-%m-%d %H:%M:%S %z')"
  {
    echo "$ts cleaned hook lines in $changed_count/$scanned_count files"
    printf ' - %s\n' "${changed_files[@]}"
  } >> "$LOG_FILE"
fi
