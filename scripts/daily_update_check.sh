#!/bin/bash
# OpenClaw每日自动更新检查脚本
# 每天凌晨5点执行

LOG_FILE="/home/ubuntu/.openclaw/logs/daily_update_check.log"
mkdir -p "/home/ubuntu/.openclaw/logs"

echo "=== OpenClaw每日更新检查 - $(date) ===" >> "$LOG_FILE"

# 检查当前版本
CURRENT_VERSION=$(openclaw --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "当前版本: $CURRENT_VERSION" >> "$LOG_FILE"
else
    echo "无法获取当前版本" >> "$LOG_FILE"
    exit 1
fi

# 检查最新版本
LATEST_VERSION_JSON=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null)
if [ $? -eq 0 ]; then
    LATEST_VERSION=$(echo "$LATEST_VERSION_JSON" | grep -o '"tag_name": "v[^"]*' | cut -d'"' -f4 | cut -dv -f2)
    echo "最新版本: $LATEST_VERSION" >> "$LOG_FILE"
else
    echo "无法获取最新版本信息" >> "$LOG_FILE"
    exit 1
fi

# 比较版本
if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
    echo "✅ 无需更新 - 当前已是最新版本 $CURRENT_VERSION" >> "$LOG_FILE"
    
    # 通过cron系统发送无更新通知
    curl -s -X POST "http://localhost:18789/api/cron/wake" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "OpenClaw每日更新检查完成：当前版本 '"$CURRENT_VERSION"'已是最新，无需升级",
           "mode": "next-heartbeat"
         }' >> "$LOG_FILE" 2>&1
    
    exit 0
else
    echo "🚀 发现新版本 $LATEST_VERSION，开始升级..." >> "$LOG_FILE"
    
    # 执行升级
    UPDATE_RESULT=$(gateway update.run 2>&1)
    UPDATE_EXIT_CODE=$?
    
    echo "升级过程:" >> "$LOG_FILE"
    echo "$UPDATE_RESULT" >> "$LOG_FILE"
    
    if [ $UPDATE_EXIT_CODE -eq 0 ]; then
        # 获取新版本亮点
        CHANGELOG=$(echo "$LATEST_VERSION_JSON" | grep -A 50 '"body": "' | sed 's/.*"body": "//' | sed 's/", "assets_url":.*//')
        
        # 提取亮点功能
        HIGHLIGHTS=$(echo "$CHANGELOG" | grep -E "### Added|### Fixes" -A 20 | grep -E "[-*]\s+" | head -10 | sed 's/^[*-] //')
        
        # 通过cron系统发送升级成功通知
        curl -s -X POST "http://localhost:18789/api/cron/wake" \
             -H "Content-Type: application/json" \
             -d '{
               "text": "🎯 OpenClaw自动升级完成！\n\n✅ 版本: '"$CURRENT_VERSION"' → '"$LATEST_VERSION"'\n\n🚀 主要新功能：'"$HIGHLIGHTS"'",
               "mode": "next-heartbeat"
             }' >> "$LOG_FILE" 2>&1
        
        echo "✅ 升级成功，已发送新版本亮点通知" >> "$LOG_FILE"
        exit 0
    else
        echo "❌ 升级失败，退出代码: $UPDATE_EXIT_CODE" >> "$LOG_FILE"
        
        # 发送失败通知
        curl -s -X POST "http://localhost:18789/api/cron/wake" \
             -H "Content-Type: application/json" \
             -d '{
               "text": "❌ OpenClaw自动升级失败！请手动检查。\n\n版本: '"$CURRENT_VERSION"' → '"$LATEST_VERSION"'\n\n错误信息: '"$(echo "$UPDATE_RESULT" | head -3)"'",
               "mode": "next-heartbeat"
             }' >> "$LOG_FILE" 2>&1
        
        exit 1
    fi
fi