# MCP 图像工具使用指南

## 📋 概述

已成功安装并配置了两个强大的 MCP 图像处理工具：

1. **MCP 图像提取器** - 专注于图像数据提取和格式转换
2. **MCP 图像处理工具** - 专注于图像编辑、批量处理和效果处理

---

## 🔍 MCP 图像提取器

### 核心功能
- 📁 从本地文件路径提取图像
- 🔗 从URL提取图像  
- 🔢 图像转 base64 编码
- 🔍 OCR 文本提取
- 🎯 对象识别
- 👁️ 视觉内容理解
- 📊 图像信息分析

### 安装状态
✅ **已安装** - TypeScript/Node.js 版本
📍 **路径**: `/home/ubuntu/.openclaw/workspace/mcp-image-extractor/`
🔧 **配置**: 已添加到 `mcporter.json`

### 使用场景
- 📄 AI 模型输入准备
- 🔍 图像内容分析
- 📝 从图片提取文字（OCR）
- 🎯 对象检测

---

## 🎨 MCP 图像处理工具

### 核心功能
- 🔄 数组与图像转换
- 🧩 大图像分块处理
- 📦 批量图像处理
- 🎨 图像格式转换
- 📏 图像尺寸调整
- 🌈 图像滤镜效果
- 🖼️ 多格式支持 (PNG, JPEG, BMP等)
- 🌈 多通道支持 (灰度、RGB、RGBA)

### 安装状态
✅ **已安装** - Python 版本
📍 **路径**: `/home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool/`
🔧 **配置**: 已添加到 `mcporter.json`
📦 **依赖**: 已安装 Pillow, NumPy, MCP

### 使用场景
- 🖼️ 专业图像编辑
- 📊 大量图片优化
- 🔄 批量格式转换
- ⚡ 性能优化处理
- 🎨 图像增强和特效

---

## 🚀 快速开始

### 1. 图像提取器使用示例

```bash
# 提取图片中的文字
image_extractor --mode ocr --input photo.jpg

# 识别图片中的对象
image_extractor --mode detect --input image.png

# 转换为 base64 格式
image_extractor --mode base64 --input image.jpg
```

### 2. 图像处理工具使用示例

```python
# 数组转图像
array_to_image(array_3d, format="png", quality=95)

# 图像转数组
image_to_array(base64_image, channels=3)

# 批量调整尺寸
batch_process("*.jpg", resize=(800, 600))

# 应用滤镜
apply_filter(image_data, filter_type="blur", strength=5)
```

---

## 🔧 技术配置

### MCP 服务器配置

两个工具都已配置在 `/home/ubuntu/.openclaw/workspace/config/mcporter.json`：

```json
{
  "mcpServers": {
    "image-extractor": {
      "command": "/home/ubuntu/.openclaw/workspace/mcp-image-extractor/dist/index.js",
      "args": []
    },
    "image-processing-tool": {
      "command": "python3",
      "args": [
        "/home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool/mcp_image_server.py"
      ]
    }
  }
}
```

### 系统依赖
- ✅ Node.js (图像提取器)
- ✅ Python 3.8+ (图像处理工具)
- ✅ Pillow (图像处理)
- ✅ NumPy (数组处理)
- ✅ MCP (Model Context Protocol)

---

## 🎯 适用场景对比

| 任务场景 | 推荐工具 | 原因 |
|---------|---------|------|
| AI 模型数据准备 | 图像提取器 | 专为AI分析优化 |
| 文字识别 (OCR) | 图像提取器 | 内置OCR功能 |
| 对象检测 | 图像提取器 | 计算机视觉能力 |
| 批量格式转换 | 图像处理工具 | 高性能批量处理 |
| 图像尺寸调整 | 图像处理工具 | 灵活的尺寸控制 |
| 滤镜效果应用 | 图像处理工具 | 丰富的滤镜库 |
| 数组 ↔ 图像转换 | 图像处理工具 | 双向转换支持 |

---

## 📞 支持与维护

- **问题反馈**: 请检查对应工具的 GitHub 仓库
- **更新维护**: 工具已集成到 OpenClaw 技能系统
- **配置更新**: 修改 `config/mcporter.json` 可调整MCP服务器配置

---

## 🎉 总结

两个 MCP 图像工具已成功安装并集成到您的 OpenClaw 工作流中！

- 🔄 **功能互补**: 一个负责理解，一个负责处理
- 🚀 **工作流完整**: 从分析到处理的完整链路
- 🎯 **最佳选择**: 根据不同任务选择合适的工具

现在您可以在任何支持 MCP 的AI工具中使用这些强大的图像处理功能！