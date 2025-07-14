import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { AnimalRescueService, animalSchema, adoptionCertificateSchema } from "./animal-rescue-service";

// Define our MCP agent with tools
export class MyMCP extends McpAgent {
	server = new McpServer({
		name: "Animal Rescue",
		version: "1.0.0",
    title: "Animal Rescue",
	}, {
    capabilities: {
      resources: {},
      tools:{}
    }
  });

  animalRescueService = new AnimalRescueService();

  // animalRescueServer 

	async init() {		
		// Tool 1: list_animals
		
		// Tool 2: get_animal_by_id

		// Tool 3: get_animal_by_name
		
		// Tool 4: adopt_pet
		

    // Resources
	}
}
// This section handles how your MCP Server handles incoming requests
export default {
	fetch(request: Request, env: Env, ctx: ExecutionContext) {
		const url = new URL(request.url);
		const allowedOrigins = "https://playground.ai.cloudflare.com";

		if (url.pathname === "/sse" || url.pathname === "/sse/message") {
			return MyMCP
				.serveSSE("/sse", { corsOptions: { origin: allowedOrigins } })
				.fetch(request, env, ctx);
		}

		if (url.pathname === "/mcp") {
			return MyMCP
				.serve("/mcp", { corsOptions: { origin: allowedOrigins } })
				.fetch(request, env, ctx);
		}

		return new Response("Not found", { status: 404 });
	},
};
