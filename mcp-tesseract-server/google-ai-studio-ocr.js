#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { extractTextFromImage } from './ocr-processor.js';

// Direct OCR processing for Google AI Studio interface
async function processGoogleAIStudioOCR() {
  try {
    // Check if there are any new images in /tmp
    const imageDir = '/tmp';
    const files = fs.readdirSync(imageDir);
    
    // Look for images that might be the Google AI Studio one
    const candidateImages = files.filter(file => {
      const filePath = path.join(imageDir, file);
      const stats = fs.statSync(filePath);
      const threeHoursAgo = Date.now() - (3 * 60 * 60 * 1000);
      
      return (file.match(/\.(jpg|jpeg|png|gif|webp)$/i) || 
              file.includes('line-media') || 
              file.includes('IMG') ||
              file.includes('image') ||
              file.includes('screenshot') ||
              file.includes('google')) &&
             stats.mtime.getTime() > threeHoursAgo;
    });
    
    if (candidateImages.length > 0) {
      // Use the most recent candidate
      const mostRecent = candidateImages
        .map(file => ({
          name: file,
          path: path.join(imageDir, file),
          time: fs.statSync(path.join(imageDir, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time)[0];
      
      console.log(`🎯 Processing: ${mostRecent.name}`);
      
      const result = await extractTextFromImage({
        image_path: mostRecent.path,
        language: 'eng'  // English for Google AI Studio
      });
      
      console.log('✅ OCR Results:');
      console.log(result.content[0].text);
      
      return {
        success: true,
        image_path: mostRecent.path,
        result: result
      };
    } else {
      console.log('📸 No recent images found. Please provide the image path or upload the image again.');
      return {
        success: false,
        error: 'No recent images found'
      };
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

// Execute the function
processGoogleAIStudioOCR().catch(console.error);