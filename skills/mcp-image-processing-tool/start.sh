#!/bin/bash

# MCP Image Processing Tool 启动脚本
cd /home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool

# 检查Python依赖
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 检查并安装依赖
if [ ! -f "requirements.txt" ]; then
    echo "错误: requirements.txt 不存在"
    exit 1
fi

echo "正在检查 Python 依赖..."
pip3 install -r requirements.txt

# 启动 MCP 服务器
echo "启动 MCP Image Processing Tool..."
python3 mcp_image_server.py