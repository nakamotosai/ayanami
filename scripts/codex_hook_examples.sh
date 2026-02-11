#!/bin/bash

# 示例：使用Codex Hook执行复杂任务
# Purpose: 展示Codex Hook系统的实际应用场景

echo "🚀 Codex Hook 系统演示"
echo "========================"

# 示例1: 深度搜索任务
echo "🔍 示例1: 深度搜索任务"
echo "任务: 搜索最新的AI技术发展趋势"
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "请搜索分析2024-2025年最新的AI技术发展趋势，包括大语言模型、多模态AI、Agent系统等前沿方向，提供详细的技术分析和市场预测" &
sleep 2

# 示例2: 代码审查任务
echo "📝 示例2: 代码审查任务"
echo "任务: 审查OpenClaw核心文件的代码质量"
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "请审查OpenClaw项目的核心文件(AGENTS.md、SOUL.md、USER.md、MEMORY.md、TOOLS.md)的代码质量、结构设计、最佳实践等方面，提供详细的改进建议和优化方案" &
sleep 2

# 示例3: 技术文档分析
echo "📚 示例3: 技术文档分析"
echo "任务: 分析OpenClaw官方文档的核心概念"
/home/ubuntu/.openclaw/workspace/scripts/codex_hook.sh --start-hook "请分析OpenClaw官方文档中的核心概念，包括Agent、Session、Memory、Context等机制，提取关键的技术要点和实现原理，生成易于理解的总结" &
sleep 2

echo "✅ 所有任务已启动！"
echo "💡 Hook系统特点:"
echo "   - 无需等待，立即返回控制权"
echo "   - 自动发送Telegram通知"
echo "   - 后台并行执行多个任务"
echo "   - 任务完成后自动汇报"
echo ""
echo "📱 请查看Telegram接收任务通知"
echo "📊 任务状态将自动更新"