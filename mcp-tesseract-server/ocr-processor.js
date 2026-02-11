import fs from 'fs';
import sharp from 'sharp';
import Tesseract from 'tesseract.js';

export async function extractTextFromImage(params) {
  try {
    const { image_path, language = 'eng' } = params;
    
    // Check if file exists
    if (!fs.existsSync(image_path)) {
      return {
        content: [{ type: "text", text: `Error: File ${image_path} does not exist` }],
        isError: true
      };
    }

    console.log(`Processing image: ${image_path}`);

    // Pre-process image for better OCR results
    let imageBuffer = fs.readFileSync(image_path);
    
    // Resize and enhance image for better OCR accuracy
    imageBuffer = await sharp(imageBuffer)
      .grayscale()  // Convert to grayscale for better OCR
      .normalize()  // Normalize contrast
      .resize({
        width: 2000,
        height: 2000,
        fit: 'inside',
        withoutEnlargement: true
      })
      .toBuffer();

    // Perform OCR using Tesseract
    const result = await Tesseract.recognize(
      imageBuffer,
      language,
      {
        logger: m => console.log(m),
        tessedit_ocr_engine_mode: 3, // Use LSTM engine for better accuracy
        tessedit_pageseg_mode: 6 // Assume a single uniform block of text
      }
    );

    const extractedText = result.data.text;
    const confidence = result.data.confidence;
    const words = result.data.words;

    console.log(`OCR completed. Confidence: ${confidence}%`);
    console.log(`Extracted text: ${extractedText}`);

    return {
      content: [
        { 
          type: "text", 
          text: JSON.stringify({
            extracted_text: extractedText,
            confidence: confidence,
            word_count: words?.length || 0,
            processing_time: `${result.data.processTimeMs}ms`,
            language: language,
            image_path: image_path
          }, null, 2)
        }
      ]
    };
  } catch (error) {
    console.error('Error processing image for OCR:', error);
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true
    };
  }
}

// Helper function to save OCR result
export function saveOCRResult(result, filename = 'ocr-result.json') {
  try {
    const fs = require('fs');
    const filePath = `/home/ubuntu/.openclaw/workspace/${filename}`;
    fs.writeFileSync(filePath, JSON.stringify(result, null, 2));
    console.log(`OCR result saved to: ${filePath}`);
    return filePath;
  } catch (error) {
    console.error('Error saving OCR result:', error);
    return null;
  }
}