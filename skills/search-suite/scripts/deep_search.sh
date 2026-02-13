#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
TOPIC=${1:-}
Q1=${2:-}
Q2=${3:-}
Q3=${4:-}

if [[ -z "$TOPIC" ]]; then
  echo "usage: $0 \"topic\" [\"q1\" \"q2\" \"q3\"]" >&2
  exit 2
fi

# Defaults tuned for Telegram: lighter + faster.
DEEP_SEARCH_ROUNDS=${DEEP_SEARCH_ROUNDS:-2}
DEEP_SEARCH_SEARX_LIMIT=${DEEP_SEARCH_SEARX_LIMIT:-6}
DEEP_SEARCH_MAX_URLS=${DEEP_SEARCH_MAX_URLS:-3}
DEEP_SEARCH_MAX_CHARS=${DEEP_SEARCH_MAX_CHARS:-8000}
DEEP_SEARCH_CODEX_TIMEOUT=${DEEP_SEARCH_CODEX_TIMEOUT:-300}

# Auto-generate 3-round queries when not provided.
if [[ -z "${Q1}" || -z "${Q2}" || -z "${Q3}" ]]; then
  Q1="$TOPIC 官方 文档 指南 教程"
  Q2="$TOPIC 最佳实践 安全 风险 坑"
  Q3="$TOPIC 实战 经验 例子 配置"
fi

TS=$(date -u +%Y%m%d-%H%M%S)
SAFE_TOPIC=$(python3 - <<"PY"
import re, os
t=os.environ.get("TOPIC", "")
t=t.replace(" ", "_")
t=re.sub(r"[^A-Za-z0-9_.-]+", "", t)
print(t)
PY
)
OUT="$WS/memory/research/deep-${SAFE_TOPIC:-topic}-$TS.md"
LOGDIR="$WS/logs/search/deep-$TS"
mkdir -p "$LOGDIR"

search_round() {
  local idx="$1"
  local q="$2"
  local outf="$LOGDIR/search-$idx.json"
  cd "$WS" && mcporter call searxng.searxng_search query="$q" limit="$DEEP_SEARCH_SEARX_LIMIT" --output json >"$outf" || true
  echo "$outf"
}

FILES=()
if [[ "$DEEP_SEARCH_ROUNDS" -ge 1 ]]; then FILES+=("$(search_round 1 "$Q1")"); fi
if [[ "$DEEP_SEARCH_ROUNDS" -ge 2 ]]; then FILES+=("$(search_round 2 "$Q2")"); fi
if [[ "$DEEP_SEARCH_ROUNDS" -ge 3 ]]; then FILES+=("$(search_round 3 "$Q3")"); fi

python3 - "${FILES[@]}" <<PY > "$LOGDIR/urls.txt"
import json, os, re, sys
from pathlib import Path

max_urls = int(os.environ.get("DEEP_SEARCH_MAX_URLS", "3"))
urls = []

for fp in sys.argv[1:]:
    p = Path(fp)
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8", errors="ignore")
    try:
        obj = json.loads(txt)
    except Exception:
        obj = None

    def harvest(o):
        if o is None:
            return
        if isinstance(o, list):
            for x in o:
                harvest(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k == "url" and isinstance(v, str) and v.startswith("http"):
                    urls.append(v)
                harvest(v)
        elif isinstance(o, str):
            for m in re.findall(r"https?://[^\s\"\)\]]+", o):
                urls.append(m)

    harvest(obj)
    if obj is None:
        urls.extend(re.findall(r"https?://[^\s\"\)\]]+", txt))

seen = set()
out = []
for u in urls:
    if u.startswith("http://127.0.0.1") or u.startswith("http://localhost"):
        continue
    if u not in seen:
        seen.add(u)
        out.append(u)

for u in out[:max_urls]:
    print(u)
PY

mapfile -t URLS < "$LOGDIR/urls.txt"
FETCH_OUT="$WS/logs/search/fetch-$TS"
mkdir -p "$FETCH_OUT"

{
  echo "# Deep Search"
  echo
  echo "- ts_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- topic: $TOPIC"
  echo "- tuning: rounds=$DEEP_SEARCH_ROUNDS searx_limit=$DEEP_SEARCH_SEARX_LIMIT max_urls=$DEEP_SEARCH_MAX_URLS max_chars=$DEEP_SEARCH_MAX_CHARS codex_timeout=${DEEP_SEARCH_CODEX_TIMEOUT}s"
  echo "- queries:"
  echo "  - $Q1"
  echo "  - $Q2"
  echo "  - $Q3"
  echo
  echo "## Candidate URLs (top ${#URLS[@]})"
  for u in "${URLS[@]}"; do echo "- $u"; done
  echo
  echo "## Fetched Excerpts"
  i=0
  for u in "${URLS[@]}"; do
    i=$((i+1))
    echo
    echo "### Source $i"
    echo "$u"
    echo
    txt=$(cd "$WS" && mcporter call fetch.fetch_url url="$u" maxChars="$DEEP_SEARCH_MAX_CHARS" --output text || true)
    printf "%s\n" "$txt" | head -c "$DEEP_SEARCH_MAX_CHARS" > "$FETCH_OUT/$i.txt"
    echo "(stored: $FETCH_OUT/$i.txt)"
  done
} > "$OUT"

SUMMARY_PROMPT=$(cat <<PROMPT
You are writing the final answer for a Telegram user.

Summarize the deep search results for topic: $TOPIC.
Use only the fetched excerpts in $FETCH_OUT/*.txt.
Output MUST be in Simplified Chinese, regardless of the source language.

Output Markdown with sections:
- TL;DR (3 lines)
- Practical Tips (5-9 bullets) each ending with (Source N)
- Pitfalls (3-6 bullets) each ending with (Source N)
- Recommendation
- Next Steps (1-3 actions)
PROMPT
)

WRAP_OUT=$(CODEX_TIMEOUT="$DEEP_SEARCH_CODEX_TIMEOUT" bash "$WS/scripts/codex_run.sh" "$SUMMARY_PROMPT" || true)
LAST_MSG=$(printf "%s\n" "$WRAP_OUT" | rg -o "last_msg=\S+" | sed "s/^last_msg=//" | tail -n 1)

{
  echo
  echo "## Summary"
  if [[ -n "${LAST_MSG:-}" && -f "${LAST_MSG}" ]]; then
    echo "(generated from: $LAST_MSG)"
    echo
    head -c 12000 "$LAST_MSG"
  else
    echo "(summary generation unavailable; missing codex last message)"
  fi
} >> "$OUT"

qmd update >/dev/null 2>&1 || true
bash "$WS/scripts/evidence_snapshot.sh" >/dev/null 2>&1 || true

echo "OK: $OUT"
