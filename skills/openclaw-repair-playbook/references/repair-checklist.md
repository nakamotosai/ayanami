# OpenClaw 修复清单（本机验证过的流程）

## 0) 先检查当前状态
- `openclaw doctor`（只看是否有 gateway/skills/agents 报错）
- `systemctl --user status openclaw-gateway.service --no-pager`

## 1) 工具列表为空 / tools [] too short
**现象**：API 报 `tools [] is too short - 'tools'`，Codex 或子 agent 调用失败。
**修复**：检查 `openclaw.json` 内 main agent 的 tools allow/deny 冲突。
- 读取：`python3 - <<'PY'
import json
p='/home/ubuntu/.openclaw/openclaw.json'
print(json.load(open(p)))
PY`
- 确认 `agents.list[].tools` 没有同时 allow/deny 同一工具
- 允许值至少包含：`exec, read, write, edit, apply_patch, web_search, web_fetch`
- 删除 `deny` 或去掉冲突项

## 2) Codex CLI 无法调用
- 确认 CLI 可执行：`codex --help`
- 确认登录：`codex login status`
- 确认调用参数来自 `codex-executor` 技能

## 3) skills 目录丢失/被清空
- 在 workspace 仓库内恢复：`git restore skills`
- 检查 `/home/ubuntu/.openclaw/workspace/skills` 是否完整
- 如果需要禁用某些技能，移除目录并更新 TOOLS.md

## 4) dist 缺失（可选）
- dist 仅用于打包/分发，不是运行必需
- 需要打包时再生成 `.skill` 文件

## 5) 规则冲突（AGENTS/MEMORY/TOOLS）
- AGENTS：强制 Codex 优先 + 禁止改写 Codex 输出
- TOOLS：真实技能列表 + 冲突/优先级
- MEMORY：只保留主人偏好

## 6) 重启 gateway
- `systemctl --user restart openclaw-gateway.service`

## 7) 验证
- 让 bot 执行一次简单 Codex 指令
- 观察是否仍出现 tools 空列表报错

## Evidence 标准
- 所有修复必须附：`cat` / `ls` / `diff` / `systemctl status` 输出
