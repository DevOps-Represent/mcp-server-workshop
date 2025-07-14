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
		this.server.registerTool(
			"list_animals",
			{
				title: "List all animals",
				description: "List all animals in the animal rescue service",
				outputSchema: {
					animals: z.array(animalSchema)
				}
			},
			async () => {
				const structuredContent = {
					animals: await this.animalRescueService.listAnimals()
				};
				return {
					// some clients dont yet support structured content, so we need to return text
					content: [{
						type: "text",
						text: JSON.stringify(structuredContent)
					}],
					structuredContent
				};
			}
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
			async ({ id }) => {
				const structuredContent = {
					animal: await this.animalRescueService.getAnimalById(id)
				};
				return {
					content: [{
						type: "text",
						text: JSON.stringify(structuredContent)
					}],
					structuredContent
				};
			}
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
			async ({ name }) => {
				const structuredContent = {
					animal: await this.animalRescueService.getAnimalByName(name)
				};
				return {
					content: [{
						type: "text",
						text: JSON.stringify(structuredContent)
					}],
					structuredContent
				};
			}
		);

		// Tool 4: adopt_pet
		this.server.registerTool(
			"adopt_pet",
			{
				title: "Adopt a pet",
				description: "Adopt a pet by id, only use this if you know the id of the animal, if the output is null there was an error. If a pet is not compatible with the customer, urge them to reconsider and adopt a more compatible pet.",
				outputSchema: {
					certificate: z.nullable(adoptionCertificateSchema),
					success: z.boolean()
				},
				inputSchema: {
					id: z.string()
				}
			},
			async ({ id }) => {
				const certificate = await this.animalRescueService.adoptAnimal(id);
				const structuredContent = {
					certificate,
					success: certificate !== null
				};
				return {
					content: [{
						type: "text",
						text: JSON.stringify(structuredContent)
					}],
					structuredContent
				};
			}
		);

    // Resources
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
