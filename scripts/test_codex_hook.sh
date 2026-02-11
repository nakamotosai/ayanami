#!/bin/bash

# Codex Hook 测试脚本
# Purpose: 测试Codex Hook机制的各项功能

echo "🧪 开始测试Codex Hook机制..."

# 1. 检查hook脚本是否存在
echo "1. 检查hook脚本..."
if [ -f "/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh" ]; then
    echo "✅ Hook脚本存在"
    chmod +x /home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh
else
    echo "❌ Hook脚本不存在"
    exit 1
fi

# 2. 检查Codex CLI是否正常
echo "2. 检查Codex CLI..."
if command -v codex &> /dev/null; then
    echo "✅ Codex CLI已安装"
    echo "   版本: $(codex --version | head -1)"
else
    echo "❌ Codex CLI未安装"
    exit 1
fi

# 3. 测试简单的Codex调用（不通过hook）
echo "3. 测试基本Codex调用..."
echo "Hello, this is a test message." | codex exec "Respond with 'Codex basic test successful'" > /tmp/codex_basic_test.txt 2>&1
if grep -q "Codex basic test successful" /tmp/codex_basic_test.txt; then
    echo "✅ 基本Codex调用正常"
else
    echo "❌ 基本Codex调用失败"
    cat /tmp/codex_basic_test.txt
fi

# 4. 测试hook调用（后台模式）
echo "4. 测试Hook机制调用..."
echo "🚀 测试Hook任务开始..."
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "这是一个简单的Hook测试任务，请回应'Hook测试成功'" > /tmp/hook_test_output.txt 2>&1 &

# 等待几秒让hook开始执行
sleep 2

# 检查hook是否启动
if grep -q "Codex task started in background" /tmp/hook_test_output.txt; then
    echo "✅ Hook机制启动正常"
else
    echo "❌ Hook机制启动失败"
    cat /tmp/hook_test_output.txt
fi

# 5. 检查是否有后台进程在运行
echo "5. 检查后台Codex进程..."
if pgrep -f "codex exec" > /dev/null; then
    echo "✅ 发现有Codex进程在后台运行"
    echo "   进程ID: $(pgrep -f 'codex exec')"
else
    echo "ℹ️  当前没有Codex进程运行"
fi

# 6. 等待hook任务完成
echo "6. 等待Hook任务完成..."
sleep 10

# 检查任务结果
if ls /tmp/codex_result_*.txt 1> /dev/null 2>&1; then
    echo "✅ Hook任务完成，结果已保存"
    echo "   结果文件: $(ls /tmp/codex_result_*.txt | tail -1)"
else
    echo "❌ Hook任务结果文件未找到"
fi

# 7. 清理测试文件
echo "7. 清理测试文件..."
rm -f /tmp/codex_basic_test.txt /tmp/hook_test_output.txt

echo "🎯 Codex Hook机制测试完成！"
echo "💡 Hook机制特点："
echo "   - 无需轮询，后台执行"
echo "   - 自动发送Telegram通知"
echo "   - 直接返回控制权"
echo "   - 节省token和时间"