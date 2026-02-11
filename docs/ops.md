# OPS.md

## 备份策略
- 定时：每 12 小时
- 保留：最近 7 份
- 归档范围：openclaw.json + workspace
- 排除：workspace/venv, .venv, MCP node_modules, output/audio, memory_archive, .git

## 清理策略
- 每周清理 coverage 与 __pycache__
- 超过 7 天的 *.bak.* 自动清理
- 历史恢复目录统一移入 workspace/.cleanup_archive

## 认证与模型
- qwen-portal 使用 OAuth，不使用 API key
- OAuth 失效时执行：openclaw models auth login --provider qwen-portal

## 变更原则
- 先备份后改动
- 关键改动必须保留回滚点
- 证据化汇报（命令输出/文件片段）
