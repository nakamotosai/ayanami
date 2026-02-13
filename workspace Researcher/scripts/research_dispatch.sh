#!/usr/bin/env bash
set -euo pipefail
QUERY="${*:-}"
if [[ -z "$QUERY" ]]; then
  echo "usage: $0 <query>" >&2
  exit 2
fi

ROOT="/home/ubuntu/.openclaw/workspace/workspace Researcher"
TMP="/tmp/researcher-search-$RANDOM.json"

# For highly time-sensitive news tasks, prefer deep search quality over noisy recall.
if [[ "$QUERY" == *今天* || "$QUERY" == *最新* || "$QUERY" == *新闻* || "$QUERY" == *news* ]]; then
  exec "$ROOT/scripts/codex_deep_search.sh" "$QUERY"
fi

if python3 "$ROOT/scripts/searxng_search.py" "$QUERY" --count 15 > "$TMP" 2>/dev/null; then
  GOOD=$(python3 - <<PY
import json,re
p="$TMP"
obj=json.load(open(p,'r',encoding='utf-8'))
rows=obj.get('results',[])
black=('baike.baidu.com','mfa.gov.cn','zhidao.baidu.com')
kw_ai=re.compile(r'(ai|人工智能|机器学习|大模型|llm|agent|生成式|genai)',re.I)
kw_jp=re.compile(r'(日本|japan|japanese|东京|tokyo)',re.I)
good=0
for r in rows:
    url=(r.get('url') or '').lower()
    t=(r.get('title') or '')+' '+(r.get('snippet') or '')
    if any(b in url for b in black):
        continue
    if kw_ai.search(t) and kw_jp.search(t+' '+url):
        good += 1
print(good)
PY
)
  if [[ "$GOOD" -ge 5 ]]; then
    cat "$TMP"
    rm -f "$TMP"
    exit 0
  fi
fi

rm -f "$TMP"
exec "$ROOT/scripts/codex_deep_search.sh" "$QUERY"
