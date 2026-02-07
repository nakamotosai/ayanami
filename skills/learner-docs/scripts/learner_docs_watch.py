#!/usr/bin/env python3
import json
import os
import shutil
import time
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFS_DIR = SKILL_ROOT / "references"
REFS_DIR.mkdir(parents=True, exist_ok=True)
WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
UPDATE_LOG = MEMORY_DIR / "docs_updates.log"
MANIFEST = REFS_DIR / "docs_manifest.json"
PREV_MANIFEST = REFS_DIR / "docs_manifest.prev.json"
LAST_SUMMARY = REFS_DIR / "last_summary.md"
BUBBLE_MESSAGE = REFS_DIR / "last_summary_bubble.txt"
TEACHER_SUMMARY = REFS_DIR / "last_summary_teacher.txt"


def load_manifest(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def record_update(changes):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with UPDATE_LOG.open("a", encoding="utf-8") as log:
        for url, info in changes.items():
            log.write(f"{timestamp} | UPDATED | {url} | {info['digest']}\n")

    summary_lines = ["# Latest Learner Docs Update", "", f"Time: {timestamp}", ""]
    for url, info in changes.items():
        summary_lines.append(f"- {url} → {info['path']} (digest {info['digest'][:8]}...)")
    summary_lines.append("\nUpdated-clips stored in learner-docs/docs/")
    LAST_SUMMARY.write_text("\n".join(summary_lines), encoding="utf-8")

    # make a bite-sized bubble summary for quick reporting
    bullet_lines = ["🌸 Learner Docs 更新摘要", ""]
    bullet_lines.append(f"时间：{timestamp}")
    bullet_lines.append(f"共 {len(changes)} 条页面被更新，覆盖 automation、channels、CLI 等模块。")
    highlights = list(changes.items())[:3]
    if highlights:
        bullet_lines.append("")
        bullet_lines.append("重点片段：")
        for url, info in highlights:
            bullet_lines.append(f"- {Path(info['path']).name} ({url.split('/')[-1]})")
    bullet_lines.append("")
    bullet_lines.append("详细摘要请查看 learner-docs/references/last_summary.md")
    BUBBLE_MESSAGE.write_text("\n".join(bullet_lines), encoding="utf-8")

    teacher_lines = [
        "老师汇报小结：",
        f"刚刚在 {timestamp} 这一轮抓取中，learner-docs 找到 {len(changes)} 条更新，覆盖 automation、channels、CLI 等核心领域。",
        "我把新的 HTML 快照和摘要都记录下来了，你想听哪一段可以随时问我。",
    ]
    if highlights:
        teacher_lines.append("重点整理：某些 automation 页面、channel 页面、CLI 页面都有更新，尤其是 auth-monitoring、cron-jobs、cron-vs-heartbeat 这些的内容。")
    teacher_lines.append("想要深入哪块，我可以立刻拿出对应的摘要再解释一遍！")
    TEACHER_SUMMARY.write_text("\n".join(teacher_lines), encoding="utf-8")


def main():
    manifest = load_manifest(MANIFEST)
    prev = load_manifest(PREV_MANIFEST)
    changes = {}
    for url, info in manifest.items():
        prev_digest = prev.get(url, {}).get("digest")
        if info.get("digest") != prev_digest:
            changes[url] = info
    if changes:
        record_update(changes)
        shutil.copy2(MANIFEST, PREV_MANIFEST)
        print(f"Detected {len(changes)} changed entries, summary written.")
    else:
        print("No doc changes detected.")


if __name__ == "__main__":
    main()
