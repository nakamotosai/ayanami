# MCP Image Processing Tool

MCP 图像处理工具技能 - 提供强大的图像编辑和批量处理功能

## 功能特性

- 🔄 数组与图像转换
- 🧩 大图像分块处理
- 📦 批量图像处理
- 🎨 图像格式转换
- 📏 图像尺寸调整
- 🌈 图像滤镜效果
- 🖼️ 多格式支持 (PNG, JPEG, BMP等)
- 🌈 多通道支持 (灰度、RGB、RGBA)

## 核心功能

### Array ↔ Image 转换
- ✅ **Array to Image**: 将3D数组转换为base64编码图像
- ✅ **Image to Array**: 将base64编码图像转换为3D数组

### 高级处理
- ✅ **Chunked Processing**: 支持大图像压缩和解析
- ✅ **Batch Processing**: 批量处理大量图像
- ✅ **Format Conversion**: 多种格式之间转换
- ✅ **Resize Operations**: 图像尺寸调整
- ✅ **Filter Effects**: 各种滤镜效果

## 使用场景

- 🖼️ 专业图像编辑
- 📊 大量图片优化
- 🔄 批量格式转换
- ⚡ 性能优化处理
- 🎨 图像增强和特效

## 安装和配置

此技能已预装在工作区中，通过 MCP 协议提供：

```json
{
  "mcpServers": {
    "image-processing-tool": {
      "command": "/home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool/mcp_image_server.py",
      "args": []
    }
  }
}
```

## 依赖安装

```bash
cd /home/ubuntu/.openclaw/workspace/MCP-Image-Processing-Tool
pip install -r requirements.txt
```

## 可用工具

- `array_to_image` - 3D数组转base64图像
- `image_to_array` - base64图像转3D数组
- `resize_image` - 图像尺寸调整
- `convert_format` - 格式转换
- `apply_filter` - 应用滤镜效果
- `batch_process` - 批量处理
- `chunked_process` - 分块处理大图像

## 示例使用

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

## 支持的格式

- **输入**: PNG, JPEG, BMP, GIF, WebP
- **输出**: PNG, JPEG, WebP, BMP
- **数组格式**: NumPy 3D数组
- **通道支持**: 1ch(灰度), 3ch(RGB), 4ch(RGBA)

## 性能特点

- ⚡ 高性能处理
- 🧠 内存优化
- 🚀 流式处理支持
- 📈 大文件处理能力