#!/usr/bin/env node
import { extractTextFromImage } from './ocr-test.js';

async function processNewImage() {
  // Look for the most recent image file
  const fs = await import('fs');
  const path = await import('path');
  
  const imageDir = '/tmp';
  const files = fs.readdirSync(imageDir);
  
  // Find the most recent image file that might be the new one
  const recentImages = files
    .filter(file => 
      file.includes('line-media') || 
      file.includes('IMG') || 
      file.includes('image') ||
      file.includes('photo') ||
      file.endsWith('.jpg') || 
      file.endsWith('.png') ||
      file.endsWith('.jpeg')
    )
    .map(file => ({
      name: file,
      path: path.join(imageDir, file),
      time: fs.statSync(path.join(imageDir, file)).mtime.getTime()
    }))
    .sort((a, b) => b.time - a.time);
  
  if (recentImages.length > 0) {
    const latestImage = recentImages[0];
    console.log(`Processing latest image: ${latestImage.name}`);
    
    const result = await extractTextFromImage({
      image_path: latestImage.path,
      language: 'chi_sim+eng'
    });
    
    console.log('OCR Result:', JSON.stringify(result, null, 2));
    return result;
  } else {
    console.log('No images found');
    return { error: 'No images found' };
  }
}

// Process the image
processNewImage().catch(console.error);