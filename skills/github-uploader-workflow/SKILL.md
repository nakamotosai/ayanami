---
name: github-uploader-workflow
description: "Guidance for a dedicated github-uploader agent to stage, commit, and push changes to a GitHub repository while keeping its workspace isolated. Use this skill whenever you're asked to upload files (commits, docs, configs) so you know how to interpret the request, inspect the repo, and report back."
---

# GitHub uploader workflow

## Purpose
Make sure every github-uploader subagent knows exactly how to inspect a workspace, reconcile the requested changes, and deliver them to the configured repository without accidentally touching unrelated files.

## Workflow
## Exclude sensitive/large files
- Always exclude secrets, tokens, credentials, and large binaries.
- Respect .gitignore + add a local exclude list if needed (examples: *.zip, *.tar.gz, *.mp4, *.mov, *.sqlite, *.db, *.log, *.env, credentials.json).
- If unsure, stop and ask the owner before staging.

1. **Clarify the task.** Read the latest user instructions in the main session; note the target repo (URL/remote name), branch, files to include, and overall goal. Ask follow-up questions if anything is ambiguous (which files, what commit message, which branch / tag to push to).
2. **Prepare the isolated workspace.** Change directory into the dedicated workspace (e.g., `/home/ubuntu/.openclaw/workspace`). Ensure it points to the correct Git remote; run `git status -sb` to confirm a clean baseline, and `git remote -v` to verify the repo URL.
3. **Stage and commit changes.** Add only the files mentioned in the instructions (or other files you touched). Run `git status` again to confirm staging. Craft a concise, descriptive commit message summarizing both the files changed and the reason (if the user didn’t supply one, ask for preferences first). Commit with `git commit -m "..."`.
4. **Push the work.** Push to the requested remote/branch (e.g., `git push origin master`). If authentication or remote configuration fails, report the exact error and say which step to fix before retrying.

## Communication rules
- Keep the main session informed: before staging, after committing, and after pushing (success or failure). Include the remote URL, branch, and whether the push reached GitHub.
- If there are no changes to upload, explicitly say the workspace is clean and that you’re standing by for new instructions.
- When a push fails, explain whether the blocker is credentials, remote misconfiguration, merge conflicts, or network issues. Suggest the next action (e.g., re-authenticate, set remote, resolve conflicts).
- Always wrap up with a concise summary of what you accomplished and what you need next.
