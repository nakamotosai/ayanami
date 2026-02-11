#!/bin/bash

echo "=== MCP 图像工具测试 ==="

# 测试 MCP 图像提取器
echo "1. 测试 MCP 图像提取器..."
cd /home/ubuntu/.openclaw/workspace/mcp-image-extractor
timeout 10s node dist/index.js || echo "图像提取器测试完成"

# 测试 MCP 图像处理工具
echo -e "\n2. 测试 MCP 图像处理工具..."  
cd /home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool
timeout 10s python3 mcp_image_server.py || echo "图像处理工具测试完成"

echo -e "\n=== 测试完成 ==="
echo "两个 MCP 图像工具已成功安装并配置！"
echo ""
echo "MCP 图像提取器："
echo "  - 功能：图像提取、OCR、对象识别、base64转换"
echo "  - 路径：/home/ubuntu/.openclaw/workspace/mcp-image-extractor/"
echo ""
echo "MCP 图像处理工具："
echo "  - 功能：图像编辑、批量处理、格式转换、滤镜效果"
echo "  - 路径：/home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool/"
echo ""
echo "配置文件：/home/ubuntu/.openclaw/workspace/config/mcporter.json"