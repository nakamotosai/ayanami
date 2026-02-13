#!/usr/bin/env python3
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not p or not p.exists():
    print("usage: dedupe_memory.py /path/to/MEMORY.md", file=sys.stderr)
    sys.exit(2)

lines = p.read_text(encoding="utf-8").splitlines(True)
seen = set()
out = []

for line in lines:
    key = line.strip()
    # Only dedupe non-empty bullet-like lines; keep headings and blanks.
    if key.startswith("-") and key not in seen:
        seen.add(key)
        out.append(line)
    elif not key.startswith("-"):
        out.append(line)

# Collapse excessive blank lines (max 2 in a row)
collapsed = []
blank = 0
for line in out:
    if line.strip() == "":
        blank += 1
        if blank <= 2:
            collapsed.append(line)
    else:
        blank = 0
        collapsed.append(line)

p.write_text("".join(collapsed), encoding="utf-8")
