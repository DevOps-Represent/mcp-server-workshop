#!/usr/bin/env python3
"""Animal Rescue MCP Server using fastMCP."""

from typing import Any, Dict

from fastmcp import FastMCP

# Handle both relative and absolute imports
try:
    from .animal_rescue_service import AnimalRescueService
except ImportError:
    from animal_rescue_service import AnimalRescueService

# Initialize the animal rescue service
animal_rescue_service = AnimalRescueService()

# Create fastMCP server
mcp = FastMCP("Animal Rescue 🐾")

def _list_animals() -> str:
    """List all available animals for adoption."""
    animals = animal_rescue_service.list_animals()
    text = "Available animals for adoption:\n\n" + "\n".join([
        f"• {animal['name']} ({animal['species']}) - {animal['breed']}, Age: {animal['age']}"
        for animal in animals
    ])
    return text

@mcp.tool()
def list_animals() -> str:
    """List all available animals for adoption."""
    return _list_animals()


def _get_animal_by_id(animal_id: str) -> str:
    """Get an animal by its ID."""
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

@mcp.tool()
def get_animal_by_id(animal_id: str) -> str:
    """Get an animal by its ID.
    
    Args:
        animal_id: The ID of the animal to retrieve
    """
    return _get_animal_by_id(animal_id)

def _get_animal_by_name(name: str) -> str:
    """Get an animal by its name (case insensitive)."""
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

@mcp.tool()
def get_animal_by_name(name: str) -> str:
    """Get an animal by its name (case insensitive).
    
    Args:
        name: The name of the animal to search for
    """
    return _get_animal_by_name(name)

def _adopt_pet(animal_id: str) -> str:
    """Adopt a pet by its unique ID or name."""
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

@mcp.tool()
def adopt_pet(animal_id: str) -> str:
    """Adopt a pet by its unique ID or name.
    
    Args:
        animal_id: The unique ID (e.g., 'dog-001', 'cat-001') or name (e.g., 'Max', 'Luna') of the animal to adopt
    """
    return _adopt_pet(animal_id)


# Compatibility classes for existing test suite
class Tool:
    def __init__(self, name: str, description: str, inputSchema: dict):
        self.name = name
        self.description = description
        self.inputSchema = inputSchema

class TextContent:
    def __init__(self, type: str, text: str):
        self.type = type
        self.text = text

# Helper functions for tests (compatibility with existing test suite)
async def list_tools():
    """Get list of available tools for testing compatibility."""
    tools = [
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
            description="Adopt a pet by its unique ID or name",
            inputSchema={
                "type": "object",
                "properties": {
                    "animal_id": {
                        "type": "string", 
                        "description": "The unique ID or name of the animal to adopt"
                    }
                },
                "required": ["animal_id"]
            }
        )
    ]
    return tools

async def call_tool(name: str, arguments: Dict[str, Any] | None):
    """Call a tool for testing compatibility."""
    if arguments is None:
        arguments = {}
    
    # Map tool calls to our core functions (not the decorated ones)
    if name == "list_animals":
        result = _list_animals()
    elif name == "get_animal_by_id":
        animal_id = arguments.get("animal_id", "")
        if not animal_id:
            result = "Error: animal_id is required"
        else:
            result = _get_animal_by_id(animal_id)
    elif name == "get_animal_by_name":
        animal_name = arguments.get("name", "")
        if not animal_name:
            result = "Error: name is required"
        else:
            result = _get_animal_by_name(animal_name)
    elif name == "adopt_pet":
        animal_id = arguments.get("animal_id", "")
        if not animal_id:
            result = "Error: animal_id is required"
        else:
            result = _adopt_pet(animal_id)
    else:
        result = f"Unknown tool: {name}"
    
    return [TextContent(type="text", text=result)]

def main():
    """Main entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
