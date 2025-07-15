# 🧠 Part 2: More Tools & Prompt Engineering (FastMCP)

Now let's build out more of your MCP agent's capabilities! In this section, we're going to create the following tools:
* 🏷️ get_animal_by_id 
* 🐩 get_animal_by_name
* 🏡 adopt_pet

### 1. 🔍 Add get_animal_by_id

This tool lets Claude fetch a specific animal based on its ID.

🧠 What this tool does:
* Tool name: get_animal_by_id
* Input: an animal_id (like "cat-002")
* Output: details about a single animal (or error message if not found)
* Implementation: Simple function decorated with `@mcp.tool()`

**Add the tool function**

With FastMCP, creating a new tool is incredibly simple. Just add this function to your `main.py`:

```python
@mcp.tool()
def get_animal_by_id(animal_id: str) -> str:
    """Get an animal by its ID.
    
    Args:
        animal_id: The ID of the animal to retrieve
    """
    animal = animal_rescue_service.get_animal_by_id(animal_id)
    if animal:
        text = (f"Animal Details:\n\n"
               f"Name: {animal['name']}\n"
               f"Species: {animal['species']}\n"
               f"Breed: {animal['breed']}\n"
               f"Age: {animal['age']} years\n"
               f"Gender: {animal['gender']}\n"
               f"Size: {animal['size']}\n"
               f"Color: {animal['color']}\n"
               f"Description: {animal['description']}\n"
               f"Vaccinated: {'Yes' if animal['vaccinated'] else 'No'}\n"
               f"Spayed/Neutered: {'Yes' if animal['spayed_neutered'] else 'No'}\n"
               f"Good with kids: {'Yes' if animal['good_with_kids'] else 'No'}\n"
               f"Good with pets: {'Yes' if animal['good_with_pets'] else 'No'}\n"
               f"Energy level: {animal['energy_level']}\n"
               f"Adoption fee: ${animal['adoption_fee']}\n"
               f"Date arrived: {animal['date_arrived']}")
        return text
    else:
        return f"No animal found with ID: {animal_id}"
```

**🚀 FastMCP Magic**

Notice how FastMCP automatically:
- Creates the tool schema from the function signature
- Uses the docstring as the tool description
- Handles parameter validation
- No need for manual tool registration!
Test with a prompt like:
"Can you show me the details for animal with ID cat-002?"

**🧪 Testing with uv:**
```bash
# Test the server
uv run python -m src.main

# Run the test suite
uv run pytest -v

# Test specific functionality
uv run pytest -k "test_get_animal_by_id" -v
```

<details>
<summary>🐞 Common Errors + Debugging Tips</summary>

* ❌ mcp.server.fastmcp not found
    * Run: `uv sync --dev` to install dependencies
* ❌ animal_rescue_service is not defined
    * Check that it's initialized at the top of the file
* ❌ No result or empty response?
    * Confirm that the ID you're testing actually exists in the dataset (check `animal_data.py`)
* ❌ Claude/client says "no tools available"?
    * Make sure your function is decorated with `@mcp.tool()`
    * Restart Claude Desktop after config changes

</details>

### 2. 🐾 Add get_animal_by_name

Same idea, but matching by name.

🧠 What this tool does:
* Tool name: get_animal_by_name
* Input: the name of the animal (like "Charlie")
* Output: the animal's full info if found, or error message if it doesn't exist
* Implementation: Another simple decorated function

**Add the tool function**

Add this function to your `main.py`:

```python
@mcp.tool()
def get_animal_by_name(name: str) -> str:
    """Get an animal by its name (case insensitive).
    
    Args:
        name: The name of the animal to search for
    """
    animal = animal_rescue_service.get_animal_by_name(name)
    if animal:
        text = (f"Found animal: {animal['name']}\n"
               f"Species: {animal['species']}\n"
               f"Breed: {animal['breed']}\n"
               f"Age: {animal['age']} years\n"
               f"Description: {animal['description']}\n"
               f"Adoption fee: ${animal['adoption_fee']}")
        return text
    else:
        return f"No animal found with name: {name}"
```

Test with a prompt like:
"Can you show me the details for the dog Charlie?"

**👼🏻 We've done the work to ensure the dog name isn't case sensitive for you, try it out! 👼🏻**

### 3. 📝 Add adopt_pet Tool

Simulate an adoption — remove the pet from the list and return a message.

This tool allows your client to **adopt a pet by its ID**. When the tool is used:

- It tries to find and remove the pet from the list.
- If successful, it returns a **certificate of adoption** and marks the action as **successful**.
- If not, it returns an error message.

This tool builds on what you've done before, but introduces:
- A **certificate** object with adoption details
- Error handling for missing or already adopted animals
- Support for adopting by name or ID

**Add the tool function**

Add this function to your `main.py`:

```python
@mcp.tool()
def adopt_pet(animal_id: str) -> str:
    """Adopt a pet by its unique ID or name.
    
    Args:
        animal_id: The unique ID (e.g., 'dog-001', 'cat-001') or name (e.g., 'Max', 'Luna') of the animal to adopt
    """
    # Check if the provided ID is actually a name, and convert it to ID
    if not animal_id.startswith(('dog-', 'cat-', 'rabbit-')):
        # Looks like a name, try to find the animal by name first
        animal = animal_rescue_service.get_animal_by_name(animal_id)
        if animal:
            actual_animal_id = animal['id']
            text_note = f"Found '{animal_id}' -> ID: {actual_animal_id}\n\n"
        else:
            return f"No animal found with name or ID: {animal_id}"
    else:
        actual_animal_id = animal_id
        text_note = ""
    
    certificate = animal_rescue_service.adopt_animal(actual_animal_id)
    if certificate:
        text = (f"{text_note}🎉 Adoption successful!\n\n"
               f"Adoption Certificate:\n"
               f"Animal ID: {certificate['animal_id']}\n"
               f"Adoption Date: {certificate['timestamp']}\n"
               f"Pickup Location: {certificate['pickup_location']}\n\n"
               f"Congratulations on your new pet!")
        return text
    else:
        return f"Unable to adopt animal with ID: {actual_animal_id}. Animal may not exist or may already be adopted."
```



Test with a prompt like:
"Adopt Cocoa"

**🧪 Testing with uv:**
```bash
# Run adoption workflow tests
uv run pytest -k "adoption_workflow" -v

# Test all adopt_pet functionality
uv run pytest -k "adopt_pet" -v
```

### 4. 🧪 Run a Full Scenario (E2E)

Try this flow:

1. "List all available animals."
2. "Tell me about Flopsy."
3. "Okay, I'd like to adopt Flopsy."

You should see Claude:
* Call list_animals
* Use get_animal_by_name
* Then adopt_pet

🙌 This is what tool orchestration looks like!

**🧪 Testing E2E with uv:**
```bash
# Run the full end-to-end test suite
uv run pytest -m integration -v

# Run performance tests
uv run pytest -m slow -v

# Run all tests with coverage
uv run pytest --cov=src --cov-report=html
```

### 5. 🧠 Prompt Engineering

Refine the descriptions in your tools to guide Claude's behavior.
Try things like:

`"Only return the pet's name, type, and personality. No extra text."`

or

`"Make recommendations based on compatibility with young children."`

Your prompt is your agent's operating system — tweak it and test!

🎉 Great job on getting this far!! 

### 6. 🛠️ Development Workflow with uv

**Essential uv commands for development:**

```bash
# Install/update dependencies
uv sync --dev

# Run the server
uv run python -m src.main
uv run animal-rescue-mcp

# Testing
uv run pytest                    # All tests
uv run pytest -v                # Verbose output
uv run pytest --cov=src         # With coverage
uv run pytest -m unit           # Unit tests only
uv run pytest -m integration    # Integration tests only

# Code quality
uv run black .                  # Format code
uv run isort .                  # Sort imports
uv run mypy src/                # Type checking

# Build and package
uv build                        # Build wheel/sdist
```

**🔧 IDE Integration:**
Most IDEs will automatically detect the `.venv` created by uv. For VS Code:
1. Open the project folder
2. Press `Cmd+Shift+P` → "Python: Select Interpreter"
3. Choose the interpreter from `.venv/bin/python`

### 🚀 Advanced: HTTP Deployment for Web Clients

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

## Let's try this as a hosted option using Cloudflare!
