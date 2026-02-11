#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as dotenv from 'dotenv';
import Tesseract from 'tesseract.js';
import sharp from 'sharp';

dotenv.config();

// Create an MCP server
const server = new McpServer({
  name: "mcp-tesseract-server",
  description: "MCP server for OCR text extraction from images using Tesseract",
  version: "1.0.0"
});

// Add OCR text extraction tool
server.tool(
  "extract_text_from_image",
  "Extract text from images using OCR (Optical Character Recognition). Supports PNG, JPG, and other common image formats.",
  {
    image_path: z.string().describe("Path to the image file to extract text from"),
    language: z.string().default("chi_sim+eng").describe("OCR language codes (e.g., 'chi_sim' for simplified Chinese, 'eng' for English, 'chi_sim+eng' for both)")
  },
  async (args, extra) => {
    try {
      const { image_path, language } = args;
      
      // Check if file exists
      const fs = await import('fs');
      if (!fs.existsSync(image_path)) {
        return {
          content: [{ type: "text", text: `Error: File ${image_path} does not exist` }],
          isError: true
        };
      }

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

      return {
        content: [
          { 
            type: "text", 
            text: JSON.stringify({
              extracted_text: extractedText,
              confidence: confidence,
              word_count: words?.length || 0,
              processing_time: `${result.data.processTimeMs}ms`,
              language: language
            }, null, 2)
          }
        ]
      };
    } catch (error) {
      console.error('Error processing image for OCR:', error);
      return {
        content: [{ type: "text", text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
        isError: true
      };
    }
  }
);

// Add batch text extraction tool
server.tool(
  "extract_text_from_images_batch",
  "Extract text from multiple images using OCR. Useful for processing large numbers of images.",
  {
    image_paths: z.array(z.string()).describe("Array of image file paths to process"),
    language: z.string().default("chi_sim+eng").describe("OCR language codes"),
    output_format: z.enum(["json", "text", "csv"]).default("json").describe("Output format for batch results")
  },
  async (args, extra) => {
    try {
      const { image_paths, language, output_format } = args;
      const fs = await import('fs');
      const results = [];

      for (const image_path of image_paths) {
        if (!fs.existsSync(image_path)) {
          results.push({
            path: image_path,
            error: "File not found"
          });
          continue;
        }

        try {
          let imageBuffer = fs.readFileSync(image_path);
          
          // Pre-process image
          imageBuffer = await sharp(imageBuffer)
            .grayscale()
            .normalize()
            .resize({
              width: 2000,
              height: 2000,
              fit: 'inside',
              withoutEnlargement: true
            })
            .toBuffer();

          const result = await Tesseract.recognize(
            imageBuffer,
            language,
            {
              logger: m => console.log(`Processing ${image_path}: ${m}`),
              tessedit_ocr_engine_mode: 3,
              tessedit_pageseg_mode: 6
            }
          );

          results.push({
            path: image_path,
            extracted_text: result.data.text,
            confidence: result.data.confidence,
            word_count: result.data.words?.length || 0,
            processing_time: `${result.data.processTimeMs}ms`,
            success: true
          });
        } catch (error) {
          results.push({
            path: image_path,
            error: error instanceof Error ? error.message : String(error),
            success: false
          });
        }
      }

      // Format output based on requested format
      let formattedOutput;
      switch (output_format) {
        case 'json':
          formattedOutput = JSON.stringify(results, null, 2);
          break;
        case 'text':
          formattedOutput = results.map(r => 
            `File: ${r.path}\nText: ${r.extracted_text || r.error}\nConfidence: ${r.confidence || 'N/A'}\n${'='.repeat(50)}`
          ).join('\n\n');
          break;
        case 'csv':
          formattedOutput = 'Path,Extracted Text,Confidence,Word Count,Processing Time,Success\n' +
            results.map(r => 
              `"${r.path}","${r.extracted_text || ''}","${r.confidence || ''}","${r.word_count || 0}","${r.processing_time || ''}","${r.success || false}"`
            ).join('\n');
          break;
      }

      return {
        content: [
          { 
            type: "text", 
            text: formattedOutput
          }
        ]
      };
    } catch (error) {
      console.error('Error in batch text extraction:', error);
      return {
        content: [{ type: "text", text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
        isError: true
      };
    }
  }
);

// Add available languages tool
server.tool(
  "list_ocr_languages",
  "List all available OCR language codes that can be used with Tesseract",
  {},
  async (args, extra) => {
    try {
      // Tesseract doesn't have a built-in API to list languages, so we'll list common ones
      const commonLanguages = {
        'eng': 'English',
        'chi_sim': 'Chinese (Simplified)',
        'chi_tra': 'Chinese (Traditional)', 
        'jpn': 'Japanese',
        'kor': 'Korean',
        'fra': 'French',
        'deu': 'German',
        'spa': 'Spanish',
        'rus': 'Russian',
        'ara': 'Arabic',
        'hin': 'Hindi',
        'tha': 'Thai',
        'vie': 'Vietnamese'
      };

      return {
        content: [
          { 
            type: "text", 
            text: JSON.stringify({
              available_languages: commonLanguages,
              note: "Use language codes like 'chi_sim+eng' for multiple languages",
              example_usage: "extract_text_from_image({ image_path: '/path/to/image.jpg', language: 'chi_sim+eng' })"
            }, null, 2)
          }
        ]
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
        isError: true
      };
    }
  }
);

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);

console.log("MCP Tesseract OCR Server started in stdio mode");