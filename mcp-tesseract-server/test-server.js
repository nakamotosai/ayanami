#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as dotenv from 'dotenv';

dotenv.config();

// Test direct MCP server connection
console.log("Starting MCP Tesseract OCR server directly...");

// Quick OCR test function
async function testOCR() {
  try {
    const { extractTextFromImage } = await import('./ocr-test.js');
    
    const result = await extractTextFromImage({
      image_path: '/tmp/line-media-599888580492132558-1770392762456.jpg',
      language: 'chi_sim+eng'
    });
    
    console.log('OCR Result:', result);
    return result;
  } catch (error) {
    console.error('Test failed:', error);
    return { error: error.message };
  }
}

// For direct testing
if (import.meta.url === `file://${process.argv[1]}`) {
  testOCR().then(() => process.exit(0));
}

// Create MCP server
const server = {
  name: "test-tesseract-server",
  description: "Test MCP server for OCR",
  version: "1.0.0"
};

console.log("MCP Tesseract OCR Server test completed");
export default server;