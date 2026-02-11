import fs from 'fs';
import path from 'path';

// Look for recently added images
function findLatestImage() {
  const imageDir = '/tmp';
  const files = fs.readdirSync(imageDir);
  
  const imageFiles = files.filter(file => {
    const filePath = path.join(imageDir, file);
    const stats = fs.statSync(filePath);
    const oneHourAgo = Date.now() - (60 * 60 * 1000);
    
    // Check if it's an image and was created recently
    return (file.match(/\.(jpg|jpeg|png|gif|webp)$/i) || 
            file.includes('line-media') || 
            file.includes('IMG') ||
            file.includes('image')) &&
           stats.mtime.getTime() > oneHourAgo;
  });
  
  if (imageFiles.length > 0) {
    // Return the most recent image that isn't the B站 one we already processed
    const recentImages = imageFiles
      .filter(file => !file.includes('line-media-599888580492132558-1770392762456'))
      .sort((a, b) => {
        const aTime = fs.statSync(path.join(imageDir, a)).mtime.getTime();
        const bTime = fs.statSync(path.join(imageDir, b)).mtime.getTime();
        return bTime - aTime;
      });
    
    return path.join(imageDir, recentImages[0]);
  }
  
  return null;
}

const latestImage = findLatestImage();
if (latestImage) {
  console.log('Found latest image:', latestImage);
  
  // Process it with OCR
  const { extractTextFromImage } = await import('./ocr-test.js');
  
  const result = await extractTextFromImage({
    image_path: latestImage,
    language: 'eng'  // Use English for Google AI Studio
  });
  
  console.log('OCR Result:', JSON.stringify(result, null, 2));
} else {
  console.log('No recent images found');
}