#!/usr/bin/env node
import fs from 'fs';
import { extractTextFromImage } from './ocr-processor.js';

// Demonstrate OCR capabilities with a sample
async function demonstrateOCR() {
  try {
    console.log('🎯 MCP OCR 工具功能演示');
    console.log('=============================');
    
    // List available tools
    console.log('\n✅ 可用的OCR工具:');
    console.log('1. extract_text_from_image - 单张图片文字提取');
    console.log('2. extract_text_from_images_batch - 批量处理');
    console.log('3. list_ocr_languages - 语言列表');
    
    console.log('\n🌍 支持的语言:');
    console.log('- eng: 英文');
    console.log('- chi_sim: 简体中文');
    console.log('- chi_tra: 繁体中文');
    console.log('- jpn: 日语');
    console.log('- kor: 韩语');
    console.log('- fra: 法语');
    console.log('- deu: 德语');
    console.log('- spa: 西班牙语');
    console.log('- rus: 俄语');
    console.log('- 多语言组合: chi_sim+eng');
    
    console.log('\n📋 使用方法:');
    console.log('- "请识别这张图片中的文字"');
    console.log('- "提取图片中的英文内容"');
    console.log('- "识别这个聊天截图"');
    
    console.log('\n🔧 当前配置:');
    console.log('- Tesseract OCR引擎: 已安装');
    console.log('- 图像预处理: 已启用');
    console.log('- MCP协议: 已配置');
    console.log('- 多语言支持: 已启用');
    
    // Test with existing image if available
    const testImages = [
      '/tmp/line-media-599888580492132558-1770392762456.jpg',
      '/home/ubuntu/.openclaw/workspace/skills/learner-docs/reports/openclaw-docs-flow.png'
    ];
    
    for (const imagePath of testImages) {
      if (fs.existsSync(imagePath)) {
        console.log(`\n🧪 测试图片: ${imagePath}`);
        console.log('================================');
        
        const result = await extractTextFromImage({
          image_path: imagePath,
          language: 'chi_sim+eng'
        });
        
        const extracted = JSON.parse(result.content[0].text);
        console.log('识别结果:');
        console.log(extracted.extracted_text.substring(0, 200) + '...');
        console.log(`置信度: ${extracted.confidence}%`);
        break;
      }
    }
    
    console.log('\n📞 请上传你的聊天截图，我立即识别其中的对话内容！');
    
  } catch (error) {
    console.error('演示失败:', error.message);
  }
}

demonstrateOCR().catch(console.error);