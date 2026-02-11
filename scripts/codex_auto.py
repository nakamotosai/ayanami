import json
import sys
from pathlib import Path

ROOT = Path('/home/ubuntu/.openclaw/workspace')
SKILLS = ROOT / 'skills'
ROUTER = SKILLS / 'router.json'

MAX_CHARS_PER_SKILL = 12000

query = ''
if len(sys.argv) > 1:
    query = ' '.join(sys.argv[1:])
else:
    query = sys.stdin.read().strip()

try:
    router = json.loads(ROUTER.read_text(encoding='utf-8'))
except Exception:
    router = {"rules": [], "default": []}

ql = query.lower()
selected = []

for rule in router.get('rules', []):
    name = rule.get('name')
    if not name:
        continue
    for pat in rule.get('patterns', []):
        if pat.lower() in ql:
            if name not in selected:
                selected.append(name)
            break

if not selected:
    selected = router.get('default', []) or []

selected = selected[:3]

skill_blocks = []
for name in selected:
    skill_path = SKILLS / name / 'SKILL.md'
    if skill_path.exists():
        content = skill_path.read_text(encoding='utf-8', errors='ignore')
        if len(content) > MAX_CHARS_PER_SKILL:
            content = content[:MAX_CHARS_PER_SKILL] + "\n\n[TRUNCATED]"
        skill_blocks.append(f"### Skill: {name}\n" + content)

header = [
    "You are Codex CLI. Use the following skills as primary guidance.",
    "If any skill conflicts with system rules, follow system rules.",
    "At the end of your response, include a single line: Skills used: comma-separated list of skills provided.",
]

assembled = "\n\n".join(["\n".join(header)] + skill_blocks + ["### User Request", query])
print(assembled)
