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
from mcp.server import FastMCP
```
FastMCP is the main class from the MCP SDK that makes it easy to build your own MCP server. It handles all the complex protocol communication for you.

```python
from .animal_rescue_service import AnimalRescueService, Animal, AdoptionCertificate
```
We've done some work to create the animal rescue service, so you're not creating it from scratch. Importing the following means we focus more on the MCP server setup and less about the animal rescue service creation!
* **AnimalRescueService**: A helper class that contains all the logic for managing pets — listing them, looking them up, simulating adoptions, etc.
* **Animal**: A TypedDict that describes what a valid animal object looks like (e.g., name, species, home requirements).
* **AdoptionCertificate**: Another TypedDict — used for generating structured confirmation when a pet is adopted (e.g., timestamp, pickup location).

#### 📥 How Your MCP Server Works (Python Implementation)

In your `main.py`, you'll see the FastMCP server setup:

```python
from mcp.server import FastMCP

# Create FastMCP server instance
app = FastMCP("Animal Rescue")

# Initialize the animal rescue service
animal_rescue_service = AnimalRescueService()

@app.tool()
def list_animals() -> List[Animal]:
    """List all available animals for adoption."""
    return animal_rescue_service.list_animals()
```

**🧠 What This Is Doing**

This section creates your MCP server and registers tools using Python decorators. The FastMCP class handles all the protocol communication for you.

**🔁 @app.tool() decorator**

This decorator automatically registers your Python function as an MCP tool. The function's docstring becomes the tool description, and the type hints define the input/output schema.

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

### 8. 🛠️ Add Tool 1: list_animals

Let's examine your first tool — `list_animals` — which lets your MCP client request a list of all available pets.

This tool connects your MCP server to your animal data and makes it available to your client via tool-calling.

📌 **What This Tool Does**
* 🐾 **Name**: list_animals
* 📝 **Description**: "List all available animals for adoption"
* 📄 **Returns**: A list of Animal objects with all available pets 🐔

🧠 **Where Is This Tool Defined?**

Look in your `main.py` file for the `@app.tool()` decorator:

```python
@app.tool()
def list_animals() -> List[Animal]:
    """List all available animals for adoption."""
    return animal_rescue_service.list_animals()
```

**Let's break this down:**

1. **@app.tool()**: This decorator registers the function as an MCP tool
2. **Function name**: `list_animals` becomes the tool name
3. **Docstring**: "List all available animals for adoption." becomes the tool description
4. **Type hints**: `List[Animal]` defines the return type schema
5. **Function body**: Calls the service method and returns the result

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

**🔍 How the Tool Works**

When your MCP client calls `list_animals`, here's what happens:

1. **Client request**: "Can you list all the animals available for adoption?"
2. **MCP server**: Recognizes this matches the `list_animals` tool
3. **Tool execution**: Calls `animal_rescue_service.list_animals()`
4. **Data processing**: Returns a list of Animal objects (filtered for non-adopted pets)
5. **Client response**: Receives the structured data and formats it for the user

<details>
<summary>🆘 Break Glass Code: Complete list_animals implementation</summary>

```python
from typing import List, Optional
from mcp.server import FastMCP
from .animal_rescue_service import AnimalRescueService, Animal, AdoptionCertificate

# Create FastMCP server instance
app = FastMCP("Animal Rescue")

# Initialize the animal rescue service
animal_rescue_service = AnimalRescueService()

@app.tool()
def list_animals() -> List[Animal]:
    """List all available animals for adoption."""
    return animal_rescue_service.list_animals()

def main() -> None:
    """Main entry point for the MCP server."""
    print("Animal Rescue MCP Server initialized")
    print("Available tools:")
    print("- list_animals: List all available animals for adoption")

if __name__ == "__main__":
    main()
```

</details>

### 9. 🧪 Test It Out

Now open Claude Desktop (or your MCP client) and type:

```
Can you list all the animals available for adoption?
```

Claude should call your tool and reply with a list of pets! 🎉

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
