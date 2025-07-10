# 🧠 Part 2: More Tools & Prompt Engineering

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
* Where to add it: In the `handle_list_tools()` function and `handle_call_tool()` function

**Add the tool definition to handle_list_tools()**

In your `handle_list_tools()` function, add this new tool to the list:

‼️ Remember to put a great tool description ‼️
```python
Tool(
    name="get_animal_by_id", 
    description="Get an animal by its ID, only use this if you know the exact ID of the animal",
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
)
```

**Add the tool handling logic**

In your `handle_call_tool()` function, add this elif block:

```python
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
        return [TextContent(type="text", text=text)]
    else:
        return [TextContent(type="text", text=f"No animal found with ID: {animal_id}")]
```

Test with a prompt like:
"Can you show me the details for animal with ID cat-002?"

<details>
<summary>🐞 Common Errors + Debugging Tips</summary>

* ❌ TextContent is not defined
    * Make sure you're importing it: `from mcp.types import Tool, TextContent`
* ❌ animal_rescue_service is not defined
    * Check that it's initialized at the top of the file
* ❌ No result or empty response?
    * Confirm that the ID you're testing actually exists in the dataset (check `animal_data.py`)
* ❌ Claude/client says "no tools available"?
    * Make sure the tool is added to the list in `handle_list_tools()`

</details>

### 2. 🐾 Add get_animal_by_name

Same idea, but matching by name.

🧠 What this tool does:
* Tool name: get_animal_by_name
* Input: the name of the animal (like "Charlie")
* Output: the animal's full info if found, or error message if it doesn't exist
* Where to add it: In both `handle_list_tools()` and `handle_call_tool()` functions

**Add the tool definition to handle_list_tools()**

Add this tool to your tools list:
‼️ Remember to put a great tool description ‼️
```python
Tool(
    name="get_animal_by_name",
    description="Find an animal by name, only use this if you know the name of the animal",
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
)
```

**Add the tool handling logic**

Add this elif block to your `handle_call_tool()` function:

```python
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
               f"Description: {animal['description']}\n"
               f"Adoption fee: ${animal['adoption_fee']}")
        return [TextContent(type="text", text=text)]
    else:
        return [TextContent(type="text", text=f"No animal found with name: {animal_name}")]
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

**Add the tool definition to handle_list_tools()**

Add this tool to your tools list:
```python
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
```

**Add the tool handling logic**

Add this elif block to your `handle_call_tool()` function:

```python
elif name == "adopt_pet":
    animal_id = arguments.get("animal_id")
    if not animal_id:
        return [TextContent(type="text", text="Error: animal_id is required")]
    
    # Check if the provided ID is actually a name, and convert it to ID
    if not animal_id.startswith(('dog-', 'cat-', 'rabbit-')):
        # Looks like a name, try to find the animal by name first
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
```

Test with a prompt like:
"Adopt Cocoa"

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

### 5. 🧠 Prompt Engineering

Refine the descriptions in your tools to guide Claude's behavior.
Try things like:

`"Only return the pet's name, type, and personality. No extra text."`

or

`"Make recommendations based on compatibility with young children."`

Your prompt is your agent's operating system — tweak it and test!

🎉 Great job on getting this far!! 

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
