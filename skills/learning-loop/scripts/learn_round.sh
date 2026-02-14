#!/usr/bin/env bash
set -euo pipefail

WS="$HOME/.openclaw/workspace"
. "$WS/skills/learning-loop/scripts/learn_lib.sh"

TOPIC=${1:-}
if [[ -z "$TOPIC" ]]; then
  echo "usage: $0 \"topic\"" >&2
  exit 2
fi

DIR=$(ensure_topic "$TOPIC")
STOP="$DIR/stop.flag"
if [[ -f "$STOP" ]]; then
  echo "STOPPED: $DIR"
  exit 0
fi

LEARN_SEARX_LIMIT=${LEARN_SEARX_LIMIT:-6}
LEARN_MAX_URLS=${LEARN_MAX_URLS:-4}
LEARN_MAX_CHARS=${LEARN_MAX_CHARS:-12000}

# Increment round and mark running
python3 - <<PY
import json, time
from pathlib import Path
p=Path("$DIR/state.json")
obj=json.loads(p.read_text(encoding='utf-8'))
obj['round']=int(obj.get('round',0))+1
obj['status']='running'
obj['updatedAtUtc']=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
print(obj['round'])
PY
ROUND=$(python3 -c 'import json;print(json.load(open("'$DIR'/state.json"))["round"])')
RDIR="$DIR/sources/round-$ROUND"
mkdir -p "$RDIR"

# Query set: general + arbitrage + twitter
Q1="$TOPIC 基础 入门 机制 术语 市场 交易"
Q2="$TOPIC 套利 arbitrage spread 对冲 交易策略 风险"
Q3="$TOPIC site:twitter.com (arbitrage OR 套利 OR strategy OR 风险 OR 对冲)"
Q4="$TOPIC site:x.com (arbitrage OR 套利 OR strategy OR 风险 OR 对冲)"
Q5="Polymarket liquidation fees spread market making risk management"

search_one() {
  local idx="$1"; local q="$2"; local out="$RDIR/search-$idx.json"
  cd "$WS" && mcporter call searxng.searxng_search query="$q" limit="$LEARN_SEARX_LIMIT" --output json >"$out" || true
  echo "$out"
}

F1=$(search_one 1 "$Q1")
F2=$(search_one 2 "$Q2")
F3=$(search_one 3 "$Q3")
F4=$(search_one 4 "$Q4")
F5=$(search_one 5 "$Q5")

python3 - "$F1" "$F2" "$F3" "$F4" "$F5" <<'PY' > "$RDIR/urls.txt"
import json, re, sys
from pathlib import Path

max_urls = int(__import__('os').environ.get('LEARN_MAX_URLS','4'))
urls=[]

def harvest(o):
    if o is None:
        return
    if isinstance(o, list):
        for x in o:
            harvest(x)
    elif isinstance(o, dict):
        for k,v in o.items():
            if k=='url' and isinstance(v,str) and v.startswith('http'):
                urls.append(v)
            harvest(v)

for fp in sys.argv[1:]:
    p=Path(fp)
    if not p.exists():
        continue
    txt=p.read_text(encoding='utf-8', errors='ignore')
    try:
        obj=json.loads(txt)
    except Exception:
        obj=None
    harvest(obj)
    if obj is None:
        urls += re.findall(r'https?://[^\s"\)\]]+', txt)

# de-dupe and prefer non-local
seen=set(); out=[]
for u in urls:
    if u.startswith('http://127.0.0.1') or u.startswith('http://localhost'):
        continue
    if u not in seen:
        seen.add(u); out.append(u)

for u in out[:max_urls]:
    print(u)
PY

mapfile -t URLS < "$RDIR/urls.txt"

# Fetch excerpts (wrap via jina.ai for JS heavy pages)
{
  echo
  echo "## Round $ROUND"
  echo "- queries: $Q1"
  echo "- queries: $Q2"
  echo "- queries: $Q3"
  echo "- queries: $Q4"
  echo "- queries: $Q5"
  echo "- urls:"
  for u in "${URLS[@]}"; do echo "  - $u"; done
} >> "$DIR/sources.md"

idx=0
for u in "${URLS[@]}"; do
  idx=$((idx+1))
  fu=$(jina_wrap "$u")
  txt=$(cd "$WS" && mcporter call fetch.fetch_url url="$fu" maxChars="$LEARN_MAX_CHARS" --output text || true)
  printf "%s\n" "$txt" | head -c "$LEARN_MAX_CHARS" >"$RDIR/src-$idx.txt"
  printf "%s\n" "$u" >"$RDIR/src-$idx.url"
done

# Build a codex prompt to integrate round findings into KB/questions.
PROMPT=$(cat <<PROMPT
你在做一个“强力学习模式”的第 $ROUND 轮学习。
话题：$TOPIC

你只能使用这些本轮抓取到的材料（每个源文件对应一个 URL）：
- $RDIR/src-*.txt 和 $RDIR/src-*.url

任务：
1) 产出“增量沉淀”：把本轮新增/修正的知识点追加写入 $DIR/kb.md（用 Markdown，保留足够细节，不要精简）。
2) 产出“未解问题”：把仍需进一步查证/补洞的问题追加写入 $DIR/questions.md（按优先级）。
3) 每个关键结论末尾必须带来源标注： (Round $ROUND Source N)
4) 输出同时包含“套利玩法/交易策略/风控/常见坑/合规与道德边界（提醒风险，不给非法指导）”。

写入规则：
- 只做追加，不要重写整文件。
- 尽量去重：如果 kb.md 已经有同义内容，只补充缺失部分。
- 全部用中文。

最后给我一个本轮摘要（10-20 条要点）用于回传 Telegram。
PROMPT
)

# Dispatch codex job (async). The notifier will deliver results.
CHAT_ID=8138445887
if [[ "${LEARN_SILENT:-0}" == "1" ]]; then CHAT_ID=""; fi
CODEX_TIMEOUT=${LEARN_CODEX_TIMEOUT:-600} bash "$WS/scripts/codex_dispatch.sh" "$PROMPT" "$CHAT_ID" >/dev/null

echo "OK: round=$ROUND dir=$DIR"
