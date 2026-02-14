#!/usr/bin/env bash
set -euo pipefail

WS="${MAGI_WORKSPACE:-$HOME/.openclaw/workspace}"
PKG="${1:-}"
TIMEOUT_SEC="${MAGI_AGENT_TIMEOUT:-240}"

if [[ -z "$PKG" ]]; then
  echo "usage: $0 \"decision_package\"" >&2
  exit 2
fi

OUTDIR="$WS/logs/magi"
mkdir -p "$OUTDIR"
TS=$(date -u +%Y%m%d-%H%M%S)
RUN_DIR="$OUTDIR/$TS"
mkdir -p "$RUN_DIR"

call_agent() {
  local agent="$1"
  local out="$RUN_DIR/$agent.json"
  local err="$RUN_DIR/$agent.err"

  echo "magi_vote: calling=$agent"
  if ! timeout "$TIMEOUT_SEC" openclaw agent --agent "$agent" -m "$PKG" --json >"$out" 2>"$err"; then
    echo "MAGI_VOTE_FAIL"
    echo "agent_failed=$agent"
    echo "stderr_file=$err"
    exit 1
  fi

  if ! jq -e '.status == "ok"' "$out" >/dev/null 2>&1; then
    echo "MAGI_VOTE_FAIL"
    echo "agent_status_not_ok=$agent"
    echo "output_file=$out"
    exit 1
  fi

  echo "magi_vote: done=$agent"
}

call_agent "magi-balthasar"
call_agent "magi-melchior"
call_agent "magi-casper"

python3 - "$RUN_DIR" <<'PY'
import datetime as dt
import json
import pathlib
import re
import sys

run_dir = pathlib.Path(sys.argv[1])
outdir = run_dir.parent

agents = [
    ("magi-balthasar", "Balthasar"),
    ("magi-melchior", "Melchior"),
    ("magi-casper", "Casper"),
]


def load_payload_text(path: pathlib.Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    payloads = data.get("result", {}).get("payloads", [])
    chunks = []
    for p in payloads:
        if isinstance(p, dict):
            t = p.get("text")
            if isinstance(t, str) and t.strip():
                chunks.append(t.strip())
    return "\n".join(chunks).strip()


def classify_vote(text: str) -> str:
    # High-risk irreversible or explicit confirmation request wins.
    if re.search(r"需要你确认|请你确认|需你确认|必须先确认|高风险.{0,12}不可逆|不可逆.{0,12}无回滚|无回滚", text):
        return "need_confirm"
    if re.search(r"不通过|否决|拒绝|不建议|不应", text):
        return "reject"
    return "approve"


records = []
for aid, label in agents:
    text = load_payload_text(run_dir / f"{aid}.json")
    vote = classify_vote(text)
    records.append({"agent": aid, "label": label, "vote": vote, "text": text})

counts = {"approve": 0, "reject": 0, "need_confirm": 0}
for r in records:
    counts[r["vote"]] += 1

if counts["need_confirm"] >= 1:
    decision = "need_confirm"
elif counts["approve"] >= 2:
    decision = "pass"
elif counts["reject"] >= 2:
    decision = "reject"
else:
    decision = "need_confirm"

result = {
    "generatedAtUtc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "agentsCalled": len(records),
    "decision": decision,
    "voteCounts": counts,
    "records": records,
}

json_path = run_dir / "result.json"
json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

label_map = {
    "pass": "通过",
    "reject": "不通过",
    "need_confirm": "需要确认",
}

md_lines = []
md_lines.append("# MAGI 决策结果")
md_lines.append("")
md_lines.append(f"- 时间(UTC): {result['generatedAtUtc']}")
md_lines.append(f"- agents_called: {result['agentsCalled']}")
md_lines.append(f"- 决议: {label_map.get(decision, decision)}")
md_lines.append(f"- 票数: approve={counts['approve']} / reject={counts['reject']} / need_confirm={counts['need_confirm']}")
md_lines.append("")
for r in records:
    md_lines.append(f"## {r['label']} ({r['agent']})")
    md_lines.append(f"- vote: {r['vote']}")
    md_lines.append("")
    md_lines.append(r["text"] or "(empty)")
    md_lines.append("")

md_path = run_dir / "result.md"
md_path.write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")

latest_json = outdir / "latest.json"
latest_md = outdir / "latest.md"
latest_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
latest_md.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")

print("MAGI_VOTE_OK")
print(f"agents_called={result['agentsCalled']}")
print(f"decision={decision}")
print(f"vote_counts=approve:{counts['approve']},reject:{counts['reject']},need_confirm:{counts['need_confirm']}")
print(f"result_json={json_path}")
print(f"result_md={md_path}")
print("---")
for r in records:
    preview = (r["text"] or "").strip().replace("\n", " ")
    if len(preview) > 220:
        preview = preview[:220] + "..."
    print(f"{r['label']}: {preview}")
PY
