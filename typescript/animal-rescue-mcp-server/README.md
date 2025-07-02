# Animal Rescue

## Part 1

- git clone
- overview of the repo + code (typescript/python)
- npm install
- npm start
- setup your MCP client with the correct URL (playground, cursor, claude etc..)
- show the MCP Server connected?
- explain the MCP scaffolding
- MCP Agent class
- the fetch method + MCP Server
- implement <list_animals> tool
- test out via the client

<Lunch time>

## Part 2

- implement <get_animal_by_id>
- test
- implement <get_animal_by_name>
- test
- implement <adopt_pet>
- E2E test of listing pets, filtering, then adopting
- prompt engineering via tool description

<handover to Cloudflare: bonus content>

- productionising (deploy REST API)
- deployment

## Deploy

<!-- TODO: make sure this button works for our project -->
[![Deploy to Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

This will deploy your MCP server to a URL like: `remote-mcp-server-authless.<your-account>.workers.dev/sse`

Alternatively, you can use the command line below to get the remote MCP Server created on your local machine:

```bash
npm create cloudflare@latest -- my-mcp-server --template=cloudflare/ai/demos/remote-mcp-authless
```

## Customizing your MCP Server

To add your own [tools](https://developers.cloudflare.com/agents/model-context-protocol/tools/) to the MCP server, define each tool inside the `init()` method of `src/index.ts` using `this.server.tool(...)`.

## Connect to Cloudflare AI Playground

You can connect to your MCP server from the Cloudflare AI Playground, which is a remote MCP client:

1. Go to <https://playground.ai.cloudflare.com/>
2. Enter your deployed MCP server URL (`remote-mcp-server-authless.<your-account>.workers.dev/sse`)
3. You can now use your MCP tools directly from the playground!

## Connect Claude Desktop to your MCP server

You can also connect to your remote MCP server from local MCP clients, by using the [mcp-remote proxy](https://www.npmjs.com/package/mcp-remote).

To connect to your MCP server from Claude Desktop, follow [Anthropic's Quickstart](https://modelcontextprotocol.io/quickstart/user) and within Claude Desktop go to Settings > Developer > Edit Config.

Update with this configuration:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "npx",
      "args": [
        "mcp-remote@latest",
        "http://localhost:8787/sse"  // or remote-mcp-server-authless.your-account.workers.dev/sse
      ]
    }
  }
}
```

## Playground

Use `llama-4-scout-17b-16e-instruct`

Restart Claude and you should see the tools become available.
