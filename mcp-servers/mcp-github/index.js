import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const token = process.env.GITHUB_TOKEN || "";
const server = new Server({ name: "mcp-github", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_issues",
      description: "List issues for a repo. Requires GITHUB_TOKEN.",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          state: { type: "string", default: "open" },
          limit: { type: "number", default: 10 }
        },
        required: ["owner", "repo"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  if (req.params.name !== "list_issues") throw new Error("Tool not found");
  if (!token) {
    return { content: [{ type: "text", text: "ERROR: missing GITHUB_TOKEN" }], isError: true };
  }
  const { owner, repo, state = "open", limit = 10 } = req.params.arguments;
  const url = `https://api.github.com/repos/${owner}/${repo}/issues?state=${encodeURIComponent(state)}&per_page=${encodeURIComponent(limit)}`;
  const r = await fetch(url, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "X-GitHub-Api-Version": "2022-11-28"
    }
  });
  const j = await r.json();
  const out = Array.isArray(j) ? j.map(x => ({ number: x.number, title: x.title, url: x.html_url })) : j;
  return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }] };
});

await server.connect(new StdioServerTransport());
