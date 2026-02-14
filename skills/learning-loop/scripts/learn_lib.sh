#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
BASE="$WS/memory/learn"

slugify() {
  python3 - <<'PY' "$1"
import re, sys
s=sys.argv[1].strip().lower()
# keep ascii-ish slug; chinese becomes removed, so preserve by hashing fallback
s2=re.sub(r'\s+', '_', s)
s2=re.sub(r'[^a-z0-9_.-]+', '', s2)
if not s2:
    import hashlib
    s2='topic_'+hashlib.sha1(s.encode('utf-8')).hexdigest()[:10]
print(s2)
PY
}

ensure_topic() {
  local topic="$1"
  local slug
  slug=$(slugify "$topic")
  local dir="$BASE/$slug"
  mkdir -p "$dir/sources"

  if [[ ! -f "$dir/state.json" ]]; then
    python3 - <<PY
import json, time
from pathlib import Path
p=Path("$dir/state.json")
obj={
  "topic": "$topic",
  "slug": "$slug",
  "round": 0,
  "status": "idle",
  "createdAtUtc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
}
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
PY
  fi

  [[ -f "$dir/questions.md" ]] || printf "# Questions (%s)\n\n" "$topic" >"$dir/questions.md"
  [[ -f "$dir/kb.md" ]] || printf "# KB (%s)\n\n" "$topic" >"$dir/kb.md"
  [[ -f "$dir/sources.md" ]] || printf "# Sources (%s)\n\n" "$topic" >"$dir/sources.md"

  echo "$dir"
}

jina_wrap() {
  # Best-effort readable proxy to bypass JS-heavy pages.
  local url="$1"
  if [[ "$url" == https://r.jina.ai/http* ]]; then
    echo "$url"; return
  fi
  if [[ "$url" == https://* ]]; then
    echo "https://r.jina.ai/https://$${url#https://}" | sed 's/\$\$//'
    return
  fi
  if [[ "$url" == http://* ]]; then
    echo "https://r.jina.ai/http://$${url#http://}" | sed 's/\$\$//'
    return
  fi
  echo "$url"
}

append_md() {
  local file="$1"
  shift
  printf "%s\n" "$@" >>"$file"
}

qmd_update() {
  qmd update >/dev/null 2>&1 || true
}
