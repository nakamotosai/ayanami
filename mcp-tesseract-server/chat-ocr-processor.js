#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

// Enhanced image finder that looks for recent images across multiple locations
async function findMostRecentImage() {
  const searchLocations = [
    '/tmp',
    '/home/ubuntu/Downloads',
    '/home/ubuntu/Pictures',
    process.env.HOME + '/Downloads',
    process.env.HOME + '/Pictures'
  ];

  let mostRecentImage = null;
  let mostRecentTime = 0;

  for (const location of searchLocations) {
    try {
      if (!fs.existsSync(location)) continue;

      const files = fs.readdirSync(location);
      
      for (const file of files) {
        const filePath = path.join(location, file);
        const stats = fs.statSync(filePath);
        
        // Check if it's an image file and is recent (within last 30 minutes)
        if ((file.match(/\.(jpg|jpeg|png|gif|webp|heic)$/i) || 
             file.includes('line-media') || 
             file.includes('IMG') ||
             file.includes('image') ||
             file.includes('photo') ||
             file.includes('chat') ||
             file.includes('screenshot')) &&
             stats.mtime.getTime() > Date.now() - (30 * 60 * 1000)) {
          
          if (stats.mtime.getTime() > mostRecentTime) {
            mostRecentTime = stats.mtime.getTime();
            mostRecentImage = {
              name: file,
              path: filePath,
              time: stats.mtime,
              size: stats.size
            };
          }
        }
      }
    } catch (error) {
      console.log(`Cannot access ${location}: ${error.message}`);
    }
  }

  return mostRecentImage;
}

// OCR processing function
async function processImageWithOCR(imagePath) {
  try {
    console.log(`🎯 Processing image: ${imagePath}`);
    
    // Import our OCR processor
    const { extractTextFromImage } = await import('./ocr-processor.js');
    
    // Determine language based on image content
    // For chat conversation, likely Chinese or mixed
    const result = await extractTextFromImage({
      image_path: imagePath,
      language: 'chi_sim+eng'  // Chinese simplified + English for mixed content
    });
    
    return {
      success: true,
      image_path: imagePath,
      result: result
    };
  } catch (error) {
    console.error('❌ OCR processing failed:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Main processing function
async function processLatestChatImage() {
  try {
    console.log('🔍 Searching for recent chat images...');
    
    const recentImage = await findMostRecentImage();
    
    if (recentImage) {
      console.log(`📸 Found recent image: ${recentImage.name} (${recentImage.size} bytes, ${recentImage.time})`);
      
      const ocrResult = await processImageWithOCR(recentImage.path);
      
      if (ocrResult.success) {
        console.log('✅ OCR Processing Complete!');
        
        // Extract and display the text
        const extractedText = JSON.parse(ocrResult.result.content[0].text);
        console.log('\n📝 Extracted Text:');
        console.log('================');
        console.log(extractedText.extracted_text);
        console.log('================');
        
        console.log('\n📊 Statistics:');
        console.log(`- Confidence: ${extractedText.confidence}%`);
        console.log(`- Word count: ${extractedText.word_count}`);
        console.log(`- Processing time: ${extractedText.processing_time}`);
        console.log(`- Language: ${extractedText.language}`);
        
        return ocrResult;
      } else {
        console.log('❌ OCR failed:', ocrResult.error);
        return ocrResult;
      }
    } else {
      console.log('❌ No recent images found in search locations');
      return { success: false, error: 'No recent images found' };
    }
  } catch (error) {
    console.error('❌ Error in main processing:', error);
    return { success: false, error: error.message };
  }
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  processLatestChatImage().catch(console.error);
}

export { findMostRecentImage, processImageWithOCR, processLatestChatImage };