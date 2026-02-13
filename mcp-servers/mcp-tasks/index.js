import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import fs from "node:fs";
import path from "node:path";

const ws = process.env.WS_DIR || path.join(process.env.HOME, ".openclaw", "workspace");
const todoFile = path.join(ws, "memory", "todos.md");

function ensure() {
  const dir = path.dirname(todoFile);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  if (!fs.existsSync(todoFile)) fs.writeFileSync(todoFile, "# TODOs\n\n", "utf8");
}

const server = new Server({ name: "mcp-tasks", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "add_todo",
      description: "Append a TODO line to workspace/memory/todos.md",
      inputSchema: {
        type: "object",
        properties: { text: { type: "string" } },
        required: ["text"]
      }
    },
    {
      name: "list_todos",
      description: "Return the current todos.md content",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  ensure();
  if (req.params.name === "add_todo") {
    const { text } = req.params.arguments;
    fs.appendFileSync(todoFile, `- [ ] ${text}\n`, "utf8");
    return { content: [{ type: "text", text: `OK: added to ${todoFile}` }] };
  }
  if (req.params.name === "list_todos") {
    const t = fs.readFileSync(todoFile, "utf8");
    return { content: [{ type: "text", text: t }] };
  }
  throw new Error("Tool not found");
});

await server.connect(new StdioServerTransport());
