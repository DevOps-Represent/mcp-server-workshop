import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { AnimalRescueService, animalSchema, adoptionCertificateSchema } from "./animal-rescue-service";
import { Certificate } from "crypto";

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
				content: [{
					type: "text",
					text: JSON.stringify(this.animalRescueService.listAnimals())
				}],
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

		// Tool 4: adopt_pet
		this.server.registerTool(
			"adopt_pet",
			{
				title: "Adopt a pet",
				description: "Adopt a pet by id, only use this if you know the id of the animal, if the output is null there was an error",
				outputSchema: {
					certificate: z.nullable(adoptionCertificateSchema),
					success: z.boolean()
				},
				inputSchema: {
					id: z.string()
				}
			},
			async ({ id }) => {
				var certificate = this.animalRescueService.adoptAnimal(id);
				var success = certificate !== null;
				return {
					content: [],
					structuredContent: { certificate: certificate, success: success }
				}
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
