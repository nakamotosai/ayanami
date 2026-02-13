import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "mcp-fetch", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "fetch_url",
      description: "Fetch a URL and return plain text (best-effort).",
      inputSchema: {
        type: "object",
        properties: {
          url: { type: "string" },
          maxChars: { type: "number", default: 8000 }
        },
        required: ["url"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  if (req.params.name !== "fetch_url") throw new Error("Tool not found");
  const { url, maxChars = 8000 } = req.params.arguments;
  const r = await fetch(url, { redirect: "follow" });
  const text = await r.text();
  const out = text.slice(0, maxChars);
  return { content: [{ type: "text", text: out }] };
});

await server.connect(new StdioServerTransport());
