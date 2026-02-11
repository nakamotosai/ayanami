---
name: codex-executor
description: 将复杂任务交给 Codex CLI 执行（搜索/写代码/改文件/改 OpenClaw 本身），主 agent 直接调用；支持 Telegram 进度通知。
priority: HIGH
---

# Codex Executor

## When to use
Use this skill whenever the user requests complex tasks that require tool use: deep search, code changes, multi-step shell work, or edits to OpenClaw config.

## Hook机制 (NEW)
使用Codex Hook系统，无需轮询，自动通知：
- 任务开始前自动发送通知给主人
- 任务完成后自动发送完成通知和结果
- 无需等待，直接返回控制权
- 节省token，提高效率

## Core rule
Main agent should call Codex CLI via the new hook mechanism. Do NOT spawn subagents unless explicitly asked. NO POLLING - let the hook handle notifications.

## Progress messages (已更新)
使用Hook系统自动发送Telegram通知：
- 开始通知: 🚀 自动发送任务开始信息
- 完成通知: ✅ 自动发送任务完成状态和结果
- 无需手动发送进度消息

## Output length policy (IMPORTANT)
- Default: produce a full answer, not a teaser.
- Codex CLI 输出必须原封不动单独发一条消息，主 agent 不得删改或添油加醋。
- For news or lists, output the full list (e.g., 10 items) with 2-3 bullet points each.
- Always include sources for each item.
- Never replace results with vague commentary or personal remarks.

## How to run Codex (NEW - 使用Hook)
Run via hook system (no polling, automatic notifications):
- /home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "任务描述" [可选模型]

If a repo is involved:
- cd /home/ubuntu/.openclaw/workspace && /home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "任务描述" [可选模型]

## Output expectations
- Return concise summary of what was done AND the full requested content.
- If Codex proposes a diff, apply it using `codex apply` and then summarize changes.

## Failure handling
If Codex fails due to auth or quota, report error and fall back to local tools only if explicitly approved by user.

## Quick Search Mode
Use when the user is waiting live or wants speed. Target 30-60s. Provide a short brief with 3-5 bullets and 2-3 sources.

## Telegram progress templates (已自动化)
现在使用Hook系统自动发送通知：
- 🚀 任务开始: 自动发送包含任务详情的开始通知
- ✅ 任务完成: 自动发送包含执行结果和统计的完成通知
- ⏱️ 无需轮询: Hook系统后台运行，完成后自动汇报

## Evidence Block (MANDATORY)
After any action, output an Evidence block with command output or file verification. Use scripts/verify_and_report.sh when a file is involved.
Format:
[EVIDENCE]
<command output or file verification>
[/EVIDENCE]
