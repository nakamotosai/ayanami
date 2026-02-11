import fs from 'fs';
import path from 'path';

// Find the most recently received image
function findLatestReceivedImage() {
  // Check common temporary directories and download locations
  const searchPaths = [
    '/tmp',
    '/home/ubuntu/Downloads',
    '/var/tmp',
    process.env.HOME + '/Downloads',
    process.env.HOME + '/Pictures'
  ];
  
  for (const searchPath of searchPaths) {
    try {
      if (!fs.existsSync(searchPath)) continue;
      
      const files = fs.readdirSync(searchPath);
      const recentImages = files
        .filter(file => {
          const filePath = path.join(searchPath, file);
          const stats = fs.statSync(filePath);
          const twoHoursAgo = Date.now() - (2 * 60 * 60 * 1000);
          
          return (file.match(/\.(jpg|jpeg|png|gif|webp|heic)$/i) || 
                  file.includes('line-media') || 
                  file.includes('IMG') ||
                  file.includes('image') ||
                  file.includes('screenshot') ||
                  file.includes('google') ||
                  file.includes('ai')) &&
                 stats.mtime.getTime() > twoHoursAgo;
        })
        .map(file => ({
          name: file,
          path: path.join(searchPath, file),
          time: fs.statSync(path.join(searchPath, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time);
      
      if (recentImages.length > 0) {
        console.log(`Found ${recentImages.length} recent images in ${searchPath}`);
        return recentImages[0].path;
      }
    } catch (error) {
      console.log(`Cannot access ${searchPath}: ${error.message}`);
    }
  }
  
  return null;
}

async function processLatestImage() {
  const latestImage = findLatestReceivedImage();
  
  if (latestImage) {
    console.log(`🎯 Processing latest image: ${latestImage}`);
    
    try {
      // Import our OCR processor
      const { extractTextFromImage, saveOCRResult } = await import('./ocr-processor.js');
      
      // Process the image with English language for Google AI Studio
      const result = await extractTextFromImage({
        image_path: latestImage,
        language: 'eng'  // English for Google AI Studio interface
      });
      
      // Save the result
      const resultPath = saveOCRResult(result, 'google-ai-studio-ocr-result.json');
      
      console.log('✅ OCR Processing Complete!');
      console.log('📊 Result:', JSON.stringify(result, null, 2));
      
      return {
        result,
        image_path: latestImage,
        result_path: resultPath
      };
    } catch (error) {
      console.error('❌ OCR processing failed:', error);
      return { error: error.message };
    }
  } else {
    console.log('❌ No recent images found');
    return { error: 'No recent images found' };
  }
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  processLatestImage().catch(console.error);
}

export { findLatestReceivedImage, processLatestImage };