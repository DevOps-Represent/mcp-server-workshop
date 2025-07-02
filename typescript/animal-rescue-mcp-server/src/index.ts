import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { AnimalRescueService, animalSchema } from "./animal-rescue-service";

// Define our MCP agent with tools
export class MyMCP extends McpAgent {
	server = new McpServer({
		name: "Animal Rescue",
		version: "1.0.0",
	});

  animalRescueService = new AnimalRescueService();

  // animalRescueServer 

	async init() {		
		// Tool 1: list_animals
		this.server.registerTool(
			"list_animals",
			{
				title: "List all animals",
				description: "List all animals in the animal rescue service",
				outputSchema: {
					animals: z.array(animalSchema)
				}
			},
			async () => ({
				content: [],
				structuredContent: { animals: this.animalRescueService.listAnimals() }
			})
		);

		// Tool 2: get_animal_by_id
		this.server.registerTool(
			"get_animal_by_id",
			{
				title: "Get an animal",
				description: "Get an animal by id, only use this if you know the id of the animal",
				outputSchema: {
					animal: z.nullable(animalSchema)
				},
				inputSchema: {
					id: z.string()
				}
			},
			async ({ id }) => ({
				content: [],
				structuredContent: { animal: this.animalRescueService.getAnimalById(id) }
			})
		);

		// Tool 3: get_animal_by_name
		this.server.registerTool(
			"search_animals_by_name",
			{
				title: "Get an animal",
				description: "Find an animal by name, only use this if you know the name of the animal",
				outputSchema: {
					animal: z.nullable(animalSchema)
				},
				inputSchema: {
					name: z.string()
				}
			},
			async ({ name }) => ({
				content: [],
				structuredContent: { animal: this.animalRescueService.getAnimalByName(name) }
			})
		);

		// Simple addition tool
		this.server.tool(
			"add",
			{ a: z.number(), b: z.number() },
			async ({ a, b }) => ({
				content: [{ type: "text", text: String(a + b) }],
			})
		);

		// Calculator tool with multiple operations
		this.server.tool(
			"calculate",
			{
				operation: z.enum(["add", "subtract", "multiply", "divide"]),
				a: z.number(),
				b: z.number(),
			},
			async ({ operation, a, b }) => {
				let result: number;
				switch (operation) {
					case "add":
						result = a + b;
						break;
					case "subtract":
						result = a - b;
						break;
					case "multiply":
						result = a * b;
						break;
					case "divide":
						if (b === 0)
							return {
								content: [
									{
										type: "text",
										text: "Error: Cannot divide by zero",
									},
								],
							};
						result = a / b;
						break;
				}
				return { content: [{ type: "text", text: String(result) }] };
			}
		);
	}
}

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
