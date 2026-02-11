# MCP Image Extractor

MCP 图像提取器技能 - 提供图像数据提取和格式转换功能

## 功能特性

- 📁 从本地文件路径提取图像
- 🔗 从URL提取图像
- 🔢 图像转 base64 编码
- 🔍 OCR 文本提取
- 🎯 对象识别
- 👁️ 视觉内容理解
- 📊 图像信息分析

## 使用场景

- 📄 AI 模型输入准备
- 🔍 图像内容分析
- 📝 从图片提取文字（OCR）
- 🎯 对象检测

## 安装和配置

此技能已预装在工作区中，通过 MCP 协议提供：

```json
{
  "mcpServers": {
    "image-extractor": {
      "command": "/home/ubuntu/.openclaw/workspace/mcp-image-extractor/dist/index.js",
      "args": []
    }
  }
}
```

## 可用工具

- `extract_image_from_file` - 从文件路径提取图像
- `extract_image_from_url` - 从URL提取图像
- `image_to_base64` - 图像转 base64 编码
- `ocr_text_extraction` - OCR文本提取
- `object_detection` - 对象识别
- `image_analysis` - 图像信息分析

## 示例使用

```bash
# 提取图片中的文字
image_extractor --mode ocr --input photo.jpg

# 识别图片中的对象
image_extractor --mode detect --input image.png

# 转换为 base64 格式
image_extractor --mode base64 --input image.jpg
```

## 支持的格式

- PNG, JPEG, BMP, GIF, WebP
- Base64 编码输出
- JSON 格式分析结果