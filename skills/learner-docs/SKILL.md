---
name: learner-docs
description: Maintain evergreen summaries and skill drafts for docs.openclaw.ai so Learner can teach the owner the freshest knowledge.
---

# Learner Docs Skill

## Purpose
This skill packages Learner's research into reusable artifacts. It keeps a local copy of docs.openclaw.ai highlights, watches for changes, and outputs structured summaries/skill cards that other agents can `skill.run`.

## Features
1. **Doc fetcher** (`scripts/learner_docs_fetch.py`): downloads the sitemap, throttles requests, stores Markdown/html snapshots under `docs/`, and logs file digests.
2. **Change tracker** (`scripts/learner_docs_watch.py`): compares new fetch+headers against `references/docs_manifest.json`, records diffs, and triggers summary updates in `references/last_summary.md` + `memory/docs_updates.log`.
3. **Skill drafting**: updates `SKILL.md` description and writes `references/summary.md` + `references/sources.md` so Learner can teach from a ready-made doc.

## Usage
```
cd /home/ubuntu/.openclaw/workspace
python3 skills/learner-docs/scripts/learner_docs_fetch.py
python3 skills/learner-docs/scripts/learner_docs_watch.py
```

## Integration
Learner should call these scripts after reading a batch of docs, then update the latest study artifacts in:
- `skills/learner-docs/references/summary.md`
- `skills/learner-docs/references/sources.md`

The resulting cards should live under `skills/learner-docs/cards/` with YAML front matter (title/source/version/tags/related_skill/summary). After updating the cards, run `scripts/knowledge_hub_sync.py` to sync them into `/home/ubuntu/.openclaw/workspace/knowledge-hub/catalog.yaml`, making knowledge hub entries queryable by any agent. Use `scripts/knowledge_hub_query.py --tag <tag>` to fetch the freshest cards.

## Latest Study (OpenClaw docs)
- Summary: `skills/learner-docs/references/summary.md`
- Sources: `skills/learner-docs/references/sources.md`
- Fetch log: `skills/learner-docs/references/last_summary.md`
- Snapshot manifest: `skills/learner-docs/references/docs_manifest.json`
