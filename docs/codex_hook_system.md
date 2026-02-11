# Codex Hook 系统使用指南

## 🚀 概述
Codex Hook系统是为Codex CLI任务设计的hook机制，实现了以下核心功能：
- **无轮询执行**: 不进行token消耗的轮询
- **自动通知**: 任务开始和完成时自动发送Telegram通知
- **后台执行**: 直接返回控制权，不等待任务完成
- **结果保存**: 自动保存任务结果供后续使用

## ⚡ 核心优势

### 🎯 效率提升
- **节省Token**: 避免轮询消耗大量token
- **快速响应**: 立即返回控制权，无需等待
- **并行处理**: 可同时执行多个Codex任务

### 📱 自动通知
- **开始通知**: 🚀 包含任务描述、开始时间、模型信息
- **完成通知**: ✅ 包含执行结果、Token使用、统计信息
- **失败处理**: 自动识别并报告失败任务

### 🔧 简化调用
- **一键调用**: 只需一个命令即可启动任务
- **统一接口**: 所有Codex任务通过hook调用
- **无需关注**: 后台自动处理所有细节

## 📋 使用方法

### 基本调用
```bash
# 使用默认模型
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "你的任务描述"

# 指定模型
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "你的任务描述" gpt-5.1-codex-mini
```

### 工作目录调用
```bash
cd /home/ubuntu/.openclaw/workspace
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "在OpenClaw工作目录执行的任务"
```

## 🔄 工作流程

### 1. 任务启动
```
用户调用 → Hook脚本 → 发送开始通知 → 启动后台Codex进程 → 立即返回控制权
```

### 2. 任务执行
```
后台进程 → 执行Codex CLI → 收集结果 → 保存结果文件 → 发送完成通知
```

### 3. 结果处理
```
结果保存 → 自动通知 → 供后续使用 → 可查看或处理
```

## 📊 通知格式

### 任务开始通知
```
🚀 Codex任务开始执行
📋 任务描述: [任务描述]
⏰ 开始时间: 2026-02-11 19:30:00
🤖 执行模型: gpt-5.1-codex-mini
```

### 任务完成通知
```
✅ Codex任务执行完成
📋 任务描述: [任务描述]
⏰ 开始时间: 2026-02-11 19:30:00
⏰ 完成时间: 2026-02-11 19:31:30
⏱️ 用时: 1分30秒
💰 Token使用: 2,900
🔗 会话ID: 019c4c77-8c4c-7c60-b332-41d97787e803
📊 执行状态: 成功
📋 执行结果预览: [结果预览]
```

## 📁 相关文件

### Hook脚本
- **位置**: `/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh`
- **权限**: 可执行 (chmod +x)
- **功能**: 核心hook逻辑实现

### 测试脚本
- **位置**: `/home/ubuntu/.openclaw/workspace/scripts/test_codex_hook.sh`
- **功能**: 测试hook系统各项功能

### 结果文件
- **位置**: `/tmp/codex_result_*.txt`
- **格式**: 自动生成的带时间戳的结果文件
- **用途**: 保存完整任务结果供后续使用

### 日志文件
- **位置**: `/home/ubuntu/.openclaw/logs/daily_reflection.log`
- **功能**: 记录hook系统执行日志

## ⚠️ 注意事项

### 1. Telegram配置
目前通知功能需要配置Telegram bot token，当前为占位符模式：
```bash
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
TELEGRAM_CHAT_ID="8138445887"
```

### 2. 任务状态
- Hook系统不保存任务状态，依赖通知结果
- 结果文件临时存储，建议及时处理
- 如需持久化存储，需要额外实现

### 3. 并发处理
- Hook系统支持并发执行多个任务
- 每个任务使用独立的结果文件
- 无锁机制，确保任务独立性

## 🔧 故障排除

### 常见问题
1. **Hook脚本无法执行**
   - 检查文件权限: `chmod +x codex_hook.sh`
   - 检查脚本路径是否正确

2. **通知不发送**
   - 检查Telegram bot token配置
   - 确认网络连接正常
   - 检查chat ID是否正确

3. **Codex任务失败**
   - 检查模型参数是否正确
   - 查看详细错误日志
   - 确认任务描述清晰明确

### 调试方法
```bash
# 测试基本Codex功能
echo "test" | codex exec "respond with test"

# 查看Hook脚本详细输出
./codex_hook.sh --start-hook "debug task"

# 检查后台进程
pgrep -f "codex exec"

# 查看结果文件
ls -la /tmp/codex_result_*.txt
```

## 🎯 最佳实践

### 1. 任务描述优化
- 使用清晰、具体的任务描述
- 避免模糊或多义的表达
- 包含必要的上下文信息

### 2. 模型选择
- 优先使用gpt-5.1-codex-mini
- 根据任务复杂度选择合适的模型
- 注意不同模型的token消耗差异

### 3. 结果处理
- 及时处理生成的结果文件
- 重要结果建议复制到永久存储
- 定期清理临时结果文件

---
*设置时间: 2026-02-11*
*维护者: ちぃ (Chii)*