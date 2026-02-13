#!/usr/bin/env bash
set -euo pipefail
QUERY="${*:-}"
if [[ -z "$QUERY" ]]; then
  echo "usage: $0 <query>" >&2
  exit 2
fi

PROMPT=$(cat <<EOF
你是研究专员。请对下面问题做深度联网检索并输出最终报告。

硬性要求：
1) 只输出最终正文，不要思考过程。
2) 结果必须包含完整来源链接（不少于8条）。
3) 结构：结论摘要、关键发现、证据与来源、不确定项、下一步建议。
4) 涉及时间敏感信息时，使用绝对日期。

问题：$QUERY
EOF
)

RAW=$(mktemp)
set +e
printf "%s" "$PROMPT" | codex exec -m gpt-5.1-codex-mini --sandbox workspace-write --skip-git-repo-check -C "/home/ubuntu/.openclaw/workspace" >"$RAW" 2>&1
RC=$?
set -e

python3 - "$RAW" <<'PY'
import re,sys
from pathlib import Path
src=Path(sys.argv[1]).read_text(encoding='utf-8',errors='ignore').splitlines()
out=[]
start=False
skip_prefix=(
    'Reading prompt from stdin...','OpenAI Codex','workdir:','model:','provider:','approval:','sandbox:','reasoning effort:','reasoning summaries:','session id:','mcp startup:','tokens used'
)
for ln in src:
    s=ln.strip()
    if not s:
        if out and out[-1] != '':
            out.append('')
        continue
    if s == 'codex':
        start=True
        continue
    if s == '--------':
        continue
    if s.startswith(skip_prefix):
        continue
    low=s.lower()
    if low.startswith('thinking') or low.startswith('user'):
        continue
    if s.startswith('🌐') or s.startswith('⚠️'):
        continue
    if re.fullmatch(r'[\d,]+',s):
        continue
    if 'codex_core::rollout::list' in low:
        continue
    if (not start) and ('结论摘要' not in s):
        continue
    start=True
    out.append(ln)
while out and not out[0].strip(): out.pop(0)
while out and not out[-1].strip(): out.pop()
print('\n'.join(out).strip() or '(no output)')
PY

rm -f "$RAW"
exit $RC
