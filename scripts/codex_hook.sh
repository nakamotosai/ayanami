#!/bin/bash

# Codex Hook Script
# Purpose: 为Codex任务提供hook机制，自动发送开始和完成通知

# 配置
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
TELEGRAM_CHAT_ID="8138445887"  # 主人ID
CODX_WORKSPACE="/home/ubuntu/.openclaw/workspace"

# 发送Telegram通知函数
send_telegram_notification() {
    local message="$1"
    local emoji="$2"
    
    # 如果设置了Telegram配置，则发送通知
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ "$TELEGRAM_BOT_TOKEN" != "your_telegram_bot_token_here" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$emoji $message" \
            -d "parse_mode=HTML" > /dev/null 2>&1
    fi
}

# Codex任务执行函数
codex_with_hook() {
    local task_description="$1"
    local model="${2:-gpt-5.1-codex-mini}"
    
    echo "🔧 Codex Hook: Starting task execution"
    
    # 任务开始通知
    start_notification="🚀 Codex任务开始执行
📋 任务描述: $task_description
⏰ 开始时间: $(date '+%Y-%m-%d %H:%M:%S')
🤖 执行模型: $model"
    
    send_telegram_notification "$start_notification" "🚀"
    
    # 执行Codex任务（后台运行）
    echo "📝 Executing Codex task: $task_description"
    
    # 使用后台进程执行Codex，不阻塞当前进程
    (
        # 记录任务开始时间
        task_start_time=$(date '+%Y-%m-%d %H:%M:%S')
        
        # 执行Codex任务
        cd "$CODX_WORKSPACE"
        MODEL_SHORT="${model##*/}" 
        codex_result=$(printf "%s\n" "$task_description" | codex exec -m "$MODEL_SHORT" --sandbox danger-full-access --dangerously-bypass-approvals-and-sandbox 2>&1)
        
        # 记录任务结束时间
        task_end_time=$(date '+%Y-%m-%d %H:%M:%S')
        
        # 提取token使用情况
        tokens_used=$(echo "$codex_result" | grep -o "tokens used [0-9,]*" | tail -1 || echo "无法统计")
        
        # 提取session ID
        session_id=$(echo "$codex_result" | grep -o "session id: [a-f0-9-]*" | tail -1 || echo "无法获取")
        
        # 构建完成通知
        completion_notification="✅ Codex任务执行完成
📋 任务描述: $task_description
⏰ 开始时间: $task_start_time
⏰ 完成时间: $task_end_time
⏱️  用时: $(dateutils.ddiff "$task_start_time" "$task_end_time" 2>/dev/null || echo "未知")
💰 Token使用: $tokens_used
🔗 会话ID: $session_id
📊 执行状态: 成功

📋 执行结果预览:
$(echo "$codex_result" | head -500 | sed 's/^/   /')"
        
        # 发送完成通知
        send_telegram_notification "$completion_notification" "✅"
        
        # 输出完整结果到文件供后续使用
        echo "$codex_result" > "/tmp/codex_result_$(date +%s).txt"
        
        echo "✅ Codex task completed and notifications sent"
    ) &
    
    # 返回控制权，不等待任务完成
    echo "🔄 Codex task started in background. Hook notifications will be sent automatically."
    echo "📝 Task: $task_description"
    echo "⏱️  No polling - will report completion when done"
}

# 如果直接调用此脚本
if [ "$1" = "--start-hook" ]; then
    codex_with_hook "$2" "$3"
fi