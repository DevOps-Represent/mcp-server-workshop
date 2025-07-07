

# 🐾 Part 1: MCP Server Workshop: Animal Rescue Edition

Welcome! In this workshop, we’ll explore what an MCP server is, how it connects to AI models like Claude, and how to use tools and prompts to build a smart backend — all while helping match humans with adoptable pets 🐕🐍🐔

You’ll be using the **TypeScript MCP SDK**, but don’t worry — this workshop is about understanding **how MCP servers work**, not mastering every line of code.

---

## 🧩 Part 1: Set Up Your Server & List Animals

### 1. 🚀 Clone the repo via your command line of choice

```
git clone https://github.com/devops-represent/animal-rescue-mcp.git
cd animal-rescue-mcp
```

### 2. 📁 Repo Overview

Open your newly cloned repo in your IDE of choice and let's take a look at what's inside the **Typescript** version of this workshop.

* 📄 index.ts: Your main entry point — this starts your server and registers the tools - this is where you'll be working the most.
* 📄 animal-rescue-service.ts: This file contains some pre-built logic for the workshop — like functions to get animal data and schemas that describe what a valid animal looks like.
    * We’ve already defined things like:
        * animalSchema: What each animal object includes (name, type, medical needs, etc.)
        * AnimalRescueService: A helper class with methods to list animals, find them by name or ID, and simulate adoptions.
* 📄 animal-data.ts: Static JSON-like data that contains info on adoptable pets
* 📄 TODO brief description of other files that are important

Imports!

📦 index.ts Import Descriptions
```
import { McpAgent } from "agents/mcp";
```
McpAgent is something we’ve created for this project to make it easier to build your own MCP server. It’s not from the SDK itself — but it uses the SDK behind the scenes.

Your Class → McpAgent (custom wrapper) → MCP SDK tools (McpServer, etc.)

```
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
```
McpServer: This is the actual server that communicates with Claude (or another MCP-compatible client).
It listens for requests, manages tool registration, and handles sending back structured responses.

```
import { z } from "zod";
```
z: This is from the Zod library — used to define and validate input/output schemas for your tools.
Helps ensure that your client sends structured data you can work with (and avoids weird bugs).

```
import {
  AnimalRescueService,
  animalSchema,
  adoptionCertificateSchema
} from "./animal-rescue-service";
```
We've done some work to create the animal rescue service, so you're not creating is from scratch. Importing the following means we focus more on the mcp server set up and less about the animal rescue service creation!
* AnimalRescueService: A helper class that contains all the logic for managing pets — listing them, looking them up, simulating adoptions, etc.
* animalSchema: A Zod schema that describes what a valid animal object looks like (e.g., name, type, home requirements).
* adoptionCertificateSchema: Another Zod schema — likely used for generating structured confirmation when a pet is adopted (e.g., name, date, adopter).


### 3. 📦 Install dependencies
Install the required packages and start your MCP server so it can run locally and accept connections from your AI client.

```
npm install
```

### 4. ▶️ Start your server

```
npm start
```

You should see your MCP server booting up on http://localhost:3333

⸻

### 5. 🔌 Connect your MCP client

Open your MCP-compatible client of choice and connect it to your running server:
* Claude Desktop → Settings > Developer > Add MCP URL: http://localhost:3333
* Cursor → Uses Claude under the hood — configure in .cursor settings
* Cloudflare Playground → Use endpoint-compatible format if deploying

You’ll see the server log connections when the model starts chatting with it. Try the following prompt and see what happens:
```
Hi! What tools do you have for animal rescue service?
```

⸻

### 6. 🧱 Understand the MCP Scaffolding

Inside this class, we set up everything your AI-powered server needs — including:
* ✨ A name and version
* 🧰 The tools it can call, which we will create in this workshop
* 📄 Any resources it might return (like adoption info)


Your setup might look like this:
```
export class MyMCP extends McpAgent {
  server = new McpServer({
    name: "Animal Rescue",
    version: "1.0.0",
    title: "Animal Rescue",
  }, {
    capabilities: {
      resources: {},
      tools: {}
    }
  });
}
```

This structure keeps all your server logic tidy and makes it easy to add more tools or features as you go.


### 7. 🛠️ Add Tool 1: list_animals

Let’s register your first tool — list_animals — which lets your MCP client request a list of all available pets.

This tool connects your MCP server to your animal data and makes it available to your client via tool-calling.


📌 What This Tool Does
* 🐾 Name: list_animals
* 📝 Description: “List all animals in the animal rescue service”
* 📄 Returns:
* 🐱 A plain text object with all animals 🐔

🧠 Where Do I Add This?

Add this inside your init() method in your MyMCP class (in index.ts - which is where all your tools will be added).


<details>

<summary>🆘 Break Glass Code: Copy/paste version of list_animals</summary>

```
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
        // some clients dont yet support structured content, so we need to return text
				content: [{
          type: "text",
          text: JSON.stringify(this.animalRescueService.listAnimals())
        }],
				structuredContent: { animals: this.animalRescueService.listAnimals() }
			})
		);
    }
```

</details>


### 8. 🧪 Test It Out

Now open Claude/Cloudflare Playground/Cursor (or your client) and type:

```
Can you list all the animals available for adoption?
```

Claude should call your tool and reply with a list of pets! 🎉

<details>
<summary>🐞 Common Errors + Debugging Tips</summary>

* ❌ “Cannot find module ‘./animal-data’”
    * Make sure animal-data.ts is in the same folder and you’re importing it properly!
* ❌ Tool not called?
    * Check your prompt or tool name. Use specific trigger phrases like “list all pets” or “available animals.”
* ❌ Server not responding?
    * Make sure you’re on the right port (3333) and your client is pointing at http://localhost:3333

</details>



Nice work on getting this far. Now that we've created our first tool, let's imbed that knowledge further and creation some more tools in Part 2!

## [Part 2](part-2-instructions.md)