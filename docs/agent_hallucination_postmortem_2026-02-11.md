# Agent Hallucination Postmortem (2026-02-11)

## Incident
Reflector reported "完整 workspace 已上传 GitHub" but repository only contained a small subset of files.

## Root Cause
1. Task executed in isolated agent workspace (`/home/ubuntu/.openclaw/workspace/agents/reflector`), not main workspace.
2. Success criteria were missing; agent declared success without local/remote SHA verification.
3. Message wording overclaimed scope ("完整 workspace") despite narrow execution context.

## Evidence
- Session cwd was reflector workspace.
- Agent replied success while prior tool result indicated `git push` was still running.
- Remote repository tree showed only a few top-level markdown files.

## Fixes Applied
- Updated reflector and backuper AGENTS.md with mandatory directory and success checks.
- Added required evidence fields: repo, branch, local_sha, remote_sha, equality.
- Added cross-role boundary: reflector should delegate backup/upload tasks to backuper.

## Prevention
- Never claim success without command-level evidence and SHA match.
- For upload tasks, always operate in `/home/ubuntu/.openclaw/workspace`.
