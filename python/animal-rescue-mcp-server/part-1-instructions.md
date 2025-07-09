# 🐾 Part 1: MCP Server Workshop: Animal Rescue Edition (Python)

Welcome! In this workshop, we'll explore what an MCP server is, how it connects to AI models like Claude, and how to use tools and prompts to build a smart backend — all while helping match humans with adoptable pets 🐕🐍🐔

You'll be using the **Python MCP SDK**, but don't worry — this workshop is about understanding **how MCP servers work**, not mastering every line of code.

---

## 🧩 Part 1: Set Up Your Server & List Animals

### 1. 🚀 Clone the repo via your command line of choice

```bash
git clone https://github.com/DevOps-Represent/mcp-server-workshop.git
cd mcp-server-workshop/python/animal-rescue-mcp-server
```

### 2. 📁 Repo Overview

Open your newly cloned repo in your IDE of choice and let's take a look at what's inside the **Python** version of this workshop.

* 📄 **main.py**: Your main entry point — this starts your server and registers the tools - this is where you'll be working the most.
* 📄 **animal_rescue_service.py**: This file contains some pre-built logic for the workshop — like functions to get animal data and TypedDict schemas that describe what a valid animal looks like.
    * We've already defined things like:
        * **Animal**: TypedDict that defines what each animal object includes (name, species, medical needs, etc.)
        * **AnimalRescueService**: A helper class with methods to list animals, find them by name or ID, and simulate adoptions.
* 📄 **animal_data.py**: Static data that contains info on adoptable pets
* 📄 **pyproject.toml**: Project configuration, dependencies, and build settings
* 📄 **requirements.txt**: Runtime dependencies for the project

#### Imports!

**📦 main.py Import Descriptions**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
```
* **Server**: The core MCP server class that handles protocol communication with Claude Desktop
* **Tool**: Type definition for MCP tools with name, description, and input schema
* **TextContent**: Type for structured text responses to tool calls

```python
from .animal_rescue_service import AnimalRescueService
```
We've done some work to create the animal rescue service, so you're not creating it from scratch. Importing the following means we focus more on the MCP server setup and less about the animal rescue service creation!
* **AnimalRescueService**: A helper class that contains all the logic for managing pets — listing them, looking them up, simulating adoptions, etc.

#### 📥 How Your MCP Server Works (Python Implementation)

In your `main.py`, you'll see the MCP server setup:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

# Create MCP server
server = Server("animal-rescue")

# Initialize the animal rescue service
animal_rescue_service = AnimalRescueService()

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_animals",
            description="List all available animals for adoption",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        # ... other tools
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool execution requests."""
    if name == "list_animals":
        animals = animal_rescue_service.list_animals()
        text = "Available animals for adoption:\n\n" + "\n".join([
            f"• {animal['name']} ({animal['species']}) - {animal['breed']}, Age: {animal['age']}"
            for animal in animals
        ])
        return [TextContent(type="text", text=text)]
```

**🧠 What This Is Doing**

This section creates your MCP server and registers tools using the official MCP protocol. The Server class handles all the protocol communication with Claude Desktop.

**🔁 @server.list_tools() decorator**

This decorator registers a function that returns the list of available tools. Each tool has a name, description, and input schema.

**🔁 @server.call_tool() decorator**

This decorator handles actual tool execution. It receives the tool name and arguments, then returns structured TextContent responses.

### 3. 📦 Install dependencies

Install the required packages to run your MCP server locally:

```bash
python3 -m pip install -r requirements.txt
```

### 4. 📦 Install in development mode (optional)

For development, install the package in editable mode:

```bash
python3 -m pip install -e .
```

### 5. ▶️ Start your server

```bash
python3 -m src.main
```

You should see your MCP server initializing with a list of available tools.

### 6. 🔌 Connect your MCP client

#### Option 1: Claude Desktop (Local Development)

For local development, you'll need to configure Claude Desktop to connect to your MCP server via stdio:

1. Open Claude Desktop
2. Go to Settings > Developer
3. Add MCP server configuration:

```json
{
  "mcpServers": {
    "animal-rescue": {
      "command": "python3",
      "args": ["-m", "src.main"],
      "cwd": "/path/to/your/mcp-server-workshop/python/animal-rescue-mcp-server"
    }
  }
}
```

#### Option 2: Cloudflare AI Playground (Hosted)

For the Cloudflare AI Playground, you'll need to deploy your MCP server as a web service:

1. **Deploy to a hosting service** (like Railway, Heroku, or Cloudflare Workers)
2. **Configure your server** to handle HTTP requests instead of stdio
3. **Add HTTP endpoints** for MCP protocol communication
4. **Use the hosted URL** in the Cloudflare playground

**Example HTTP wrapper for FastMCP:**
```python
from fastapi import FastAPI
from mcp.server import FastMCP

# Create both FastAPI and FastMCP instances
web_app = FastAPI()
mcp_app = FastMCP("Animal Rescue")

@web_app.post("/mcp")
async def mcp_endpoint(request: dict):
    # Handle MCP protocol over HTTP
    return await mcp_app.handle_request(request)
```

#### Option 3: Testing with MCP Client Libraries

You can also test your server programmatically:

```python
import asyncio
from mcp.client import ClientSession

async def test_server():
    async with ClientSession() as session:
        # Connect to your server
        await session.connect("python3", ["-m", "src.main"])
        
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {tools}")
        
        # Call a tool
        result = await session.call_tool("list_animals", {})
        print(f"Animals: {result}")

# Run the test
asyncio.run(test_server())
```

### 7. 🧪 Test your connection

Try the following prompt in your MCP client:

```
Hi! What tools do you have for animal rescue service?
```

You should see the server respond with information about the available tools.

### 8. 🛠️ Understanding Your Tools

Let's examine your tools — which let your MCP client interact with the animal rescue system.

📌 **Available Tools**
* 🐾 **list_animals**: List all available animals for adoption
* 🔍 **get_animal_by_id**: Get detailed information about a specific animal
* 🔍 **get_animal_by_name**: Find an animal by name (case insensitive)
* 💝 **adopt_pet**: Adopt a pet using either its ID or name

🧠 **How Tools Are Defined**

Look in your `main.py` file for the tool definitions:

**1. Tool Registration (`@server.list_tools()`):**
```python
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_animals",
            description="List all available animals for adoption",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="adopt_pet",
            description="Adopt a pet by its unique ID or name. If you provide a name, it will automatically find the corresponding ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "animal_id": {
                        "type": "string", 
                        "description": "The unique ID (e.g., 'dog-001', 'cat-001') or name (e.g., 'Max', 'Luna') of the animal to adopt."
                    }
                },
                "required": ["animal_id"]
            }
        )
    ]
```

**2. Tool Execution (`@server.call_tool()`):**
```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    if name == "list_animals":
        animals = animal_rescue_service.list_animals()
        text = "Available animals for adoption:\n\n" + "\n".join([
            f"• {animal['name']} ({animal['species']}) - {animal['breed']}, Age: {animal['age']}"
            for animal in animals
        ])
        return [TextContent(type="text", text=text)]
    
    elif name == "adopt_pet":
        animal_id = arguments.get("animal_id")
        if not animal_id:
            return [TextContent(type="text", text="Error: animal_id is required")]
        
        # Smart adoption: accepts both names and IDs
        if not animal_id.startswith(('dog-', 'cat-', 'rabbit-')):
            # Looks like a name, find the animal by name first
            animal = animal_rescue_service.get_animal_by_name(animal_id)
            if animal:
                animal_id = animal['id']
                text_note = f"Found '{arguments.get('animal_id')}' -> ID: {animal_id}\n\n"
            else:
                return [TextContent(type="text", text=f"No animal found with name or ID: {arguments.get('animal_id')}")]
        else:
            text_note = ""
        
        certificate = animal_rescue_service.adopt_animal(animal_id)
        if certificate:
            text = (f"{text_note}🎉 Adoption successful!\n\n"
                   f"Adoption Certificate:\n"
                   f"Animal ID: {certificate['animal_id']}\n"
                   f"Adoption Date: {certificate['timestamp']}\n"
                   f"Pickup Location: {certificate['pickup_location']}\n\n"
                   f"Congratulations on your new pet!")
            return [TextContent(type="text", text=text)]
```

**Let's break this down:**

1. **Tool Registration**: Each tool is defined with a name, description, and input schema
2. **Tool Execution**: The `handle_call_tool` function receives the tool name and arguments
3. **Smart Features**: The `adopt_pet` tool accepts both animal names and IDs
4. **Structured Response**: All tools return `TextContent` objects with formatted text

**🤔 Understanding Tool Descriptions**

Tool descriptions are important — they're like SEO for your tool. The better you write them, the easier it is for Claude to discover and use them correctly.

<details>
<summary>⚔ Side Quest: Writing Good Tool Descriptions</summary>

Picking the right description for your tool helps your MCP client know when (and how) to use it. This isn't just documentation — it's **part of the prompt**.

---

### ✅ Good Examples

| Tool Name         | Description                                                                 |
|------------------|------------------------------------------------------------------------------|
| `list_animals`       | List all animals currently available for adoption.                        |
| `get_animal_by_id`   | Look up an animal by its unique ID and return its full profile.           |
| `adopt_pet`          | Mark an animal as adopted and remove it from the list of available pets.  |
| `get_adoption_costs` | Return the adoption fee and any medical costs for a specific animal.       |
| `suggest_matches`    | Suggest animals based on a person's home type, activity level, and preferences. |

---

### ❌ Not-So-Great Examples

| Tool Name         | Description        |
|------------------|--------------------|
| `list_animals`       | Shows animals.      |
| `get_animal_by_id`   | Get pet stuff from ID. |
| `adopt_pet`          | Do adoption.        |
| `get_adoption_costs` | Costs.              |
| `suggest_matches`    | Find good animal.   |

---

### 💡 Tips:
- Use **clear verbs**: list, return, mark, suggest, look up  
- Think: "How would I describe this tool in one sentence to another human?"
- The model sees this — so make it *MCP-client-friendly*, not just code-friendly

</details>

<br>

**🔍 How the Tools Work**

When your MCP client calls a tool, here's what happens:

1. **Client request**: "Can you list all the animals available for adoption?"
2. **MCP server**: Recognizes this matches the `list_animals` tool
3. **Tool execution**: Calls `animal_rescue_service.list_animals()`
4. **Data processing**: Formats the data into a user-friendly text response
5. **Client response**: Receives the `TextContent` and displays it to the user

**🎯 Special Feature: Smart Adoption**

The `adopt_pet` tool is particularly smart — it accepts both names and IDs:
- Input: `{"animal_id": "Max"}` → Automatically finds Max's ID (dog-001) and adopts
- Input: `{"animal_id": "dog-001"}` → Directly adopts using the ID

<details>
<summary>🆘 Break Glass Code: Complete MCP server implementation</summary>

```python
#!/usr/bin/env python3
"""Simple MCP server for Animal Rescue - following exact MCP patterns."""

import asyncio
from typing import Any, Dict, Sequence

from mcp.server import Server
from mcp.types import Tool, TextContent
from .animal_rescue_service import AnimalRescueService

# Initialize the animal rescue service
animal_rescue_service = AnimalRescueService()

# Create MCP server
server = Server("animal-rescue")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_animals",
            description="List all available animals for adoption",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_animal_by_id", 
            description="Get an animal by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "animal_id": {
                        "type": "string",
                        "description": "The ID of the animal to retrieve"
                    }
                },
                "required": ["animal_id"]
            }
        ),
        Tool(
            name="get_animal_by_name",
            description="Get an animal by its name (case insensitive)",
            inputSchema={
                "type": "object", 
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the animal to search for"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="adopt_pet",
            description="Adopt a pet by its unique ID or name. If you provide a name, it will automatically find the corresponding ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "animal_id": {
                        "type": "string", 
                        "description": "The unique ID (e.g., 'dog-001', 'cat-001') or name (e.g., 'Max', 'Luna') of the animal to adopt."
                    }
                },
                "required": ["animal_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool execution requests."""
    if name == "list_animals":
        animals = animal_rescue_service.list_animals()
        text = "Available animals for adoption:\n\n" + "\n".join([
            f"• {animal['name']} ({animal['species']}) - {animal['breed']}, Age: {animal['age']}"
            for animal in animals
        ])
        return [TextContent(type="text", text=text)]
    
    elif name == "get_animal_by_id":
        animal_id = arguments.get("animal_id")
        if not animal_id:
            return [TextContent(type="text", text="Error: animal_id is required")]
        
        animal = animal_rescue_service.get_animal_by_id(animal_id)
        if animal:
            text = (f"Animal Details:\n\n"
                   f"Name: {animal['name']}\n"
                   f"Species: {animal['species']}\n"
                   f"Breed: {animal['breed']}\n"
                   f"Age: {animal['age']} years\n"
                   f"Adoption fee: ${animal['adoption_fee']}")
            return [TextContent(type="text", text=text)]
        else:
            return [TextContent(type="text", text=f"No animal found with ID: {animal_id}")]
    
    elif name == "get_animal_by_name":
        animal_name = arguments.get("name")
        if not animal_name:
            return [TextContent(type="text", text="Error: name is required")]
        
        animal = animal_rescue_service.get_animal_by_name(animal_name)
        if animal:
            text = (f"Found animal: {animal['name']}\n"
                   f"Species: {animal['species']}\n"
                   f"Breed: {animal['breed']}\n"
                   f"Age: {animal['age']} years\n"
                   f"Adoption fee: ${animal['adoption_fee']}")
            return [TextContent(type="text", text=text)]
        else:
            return [TextContent(type="text", text=f"No animal found with name: {animal_name}")]
    
    elif name == "adopt_pet":
        animal_id = arguments.get("animal_id")
        if not animal_id:
            return [TextContent(type="text", text="Error: animal_id is required")]
        
        # Smart adoption: accepts both names and IDs
        if not animal_id.startswith(('dog-', 'cat-', 'rabbit-')):
            animal = animal_rescue_service.get_animal_by_name(animal_id)
            if animal:
                animal_id = animal['id']
                text_note = f"Found '{arguments.get('animal_id')}' -> ID: {animal_id}\n\n"
            else:
                return [TextContent(type="text", text=f"No animal found with name or ID: {arguments.get('animal_id')}")]
        else:
            text_note = ""
        
        certificate = animal_rescue_service.adopt_animal(animal_id)
        if certificate:
            text = (f"{text_note}🎉 Adoption successful!\n\n"
                   f"Adoption Certificate:\n"
                   f"Animal ID: {certificate['animal_id']}\n"
                   f"Adoption Date: {certificate['timestamp']}\n"
                   f"Pickup Location: {certificate['pickup_location']}\n\n"
                   f"Congratulations on your new pet!")
            return [TextContent(type="text", text=text)]
        else:
            return [TextContent(type="text", text=f"Unable to adopt animal with ID: {animal_id}. Animal may not exist or may already be adopted.")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the server using stdin/stdout streams."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

</details>

### 9. 🧪 Test It Out

Now open Claude Desktop (or your MCP client) and try these commands:

**List all animals:**
```
Can you list all the animals available for adoption?
```

**Get animal details:**
```
Can you get details for animal ID dog-001?
```

**Find an animal by name:**
```
Can you find an animal named Max?
```

**Adopt a pet (using name):**
```
I want to adopt Max
```

**Adopt a pet (using ID):**
```
I want to adopt animal ID cat-001
```

Claude should call your tools and reply with helpful information! 🎉

<details>
<summary>🐞 Common Errors + Debugging Tips</summary>

* ❌ **"Cannot import module 'src.main'"**
    * Make sure you're running from the correct directory and using `python3 -m src.main`
* ❌ **Tool not called?**
    * Check your prompt or tool name. Use specific trigger phrases like "list all pets" or "available animals."
* ❌ **Server not responding?**
    * Make sure your MCP client is configured correctly and pointing to the right command/path
* ❌ **Import errors?**
    * Ensure all dependencies are installed with `python3 -m pip install -r requirements.txt`

</details>

### 10. 🚀 Advanced: HTTP Deployment for Web Clients

If you want to use your MCP server with web-based clients like the Cloudflare AI Playground, you'll need to wrap it in an HTTP server:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI wrapper
web_app = FastAPI()

# Add CORS middleware
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://playground.ai.cloudflare.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@web_app.post("/mcp")
async def mcp_endpoint(request: dict):
    """Handle MCP protocol over HTTP."""
    # Process MCP request and return response
    # This requires additional implementation
    pass

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
```

---

Nice work on getting this far! Now that we've created our first tool, let's embed that knowledge further and create some more tools in Part 2!

## [Part 2](part-2-instructions.md)
