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
    """
    List available tools.
    Each tool specifies its name, description, and input schema.
    """
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
            description="Adopt a pet by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "animal_id": {
                        "type": "string", 
                        "description": "The ID of the animal to adopt"
                    }
                },
                "required": ["animal_id"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """
    Handle tool execution requests.
    """
    if name == "list_animals":
        animals = animal_rescue_service.list_animals()
        text = "Available animals for adoption:\\n\\n" + "\\n".join([
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
            text = (f"Animal Details:\\n\\n"
                   f"Name: {animal['name']}\\n"
                   f"Species: {animal['species']}\\n"
                   f"Breed: {animal['breed']}\\n"
                   f"Age: {animal['age']} years\\n"
                   f"Gender: {animal['gender']}\\n"
                   f"Size: {animal['size']}\\n"
                   f"Color: {animal['color']}\\n"
                   f"Description: {animal['description']}\\n"
                   f"Vaccinated: {'Yes' if animal['vaccinated'] else 'No'}\\n"
                   f"Spayed/Neutered: {'Yes' if animal['spayed_neutered'] else 'No'}\\n"
                   f"Good with kids: {'Yes' if animal['good_with_kids'] else 'No'}\\n"
                   f"Good with pets: {'Yes' if animal['good_with_pets'] else 'No'}\\n"
                   f"Energy level: {animal['energy_level']}\\n"
                   f"Adoption fee: ${animal['adoption_fee']}\\n"
                   f"Date arrived: {animal['date_arrived']}")
            return [TextContent(type="text", text=text)]
        else:
            return [TextContent(type="text", text=f"No animal found with ID: {animal_id}")]
    
    elif name == "get_animal_by_name":
        animal_name = arguments.get("name")
        if not animal_name:
            return [TextContent(type="text", text="Error: name is required")]
        
        animal = animal_rescue_service.get_animal_by_name(animal_name)
        if animal:
            text = (f"Found animal: {animal['name']}\\n"
                   f"Species: {animal['species']}\\n"
                   f"Breed: {animal['breed']}\\n"
                   f"Age: {animal['age']} years\\n"
                   f"Description: {animal['description']}\\n"
                   f"Adoption fee: ${animal['adoption_fee']}")
            return [TextContent(type="text", text=text)]
        else:
            return [TextContent(type="text", text=f"No animal found with name: {animal_name}")]
    
    elif name == "adopt_pet":
        animal_id = arguments.get("animal_id")
        if not animal_id:
            return [TextContent(type="text", text="Error: animal_id is required")]
        
        certificate = animal_rescue_service.adopt_animal(animal_id)
        if certificate:
            text = (f"🎉 Adoption successful!\\n\\n"
                   f"Adoption Certificate:\\n"
                   f"Animal ID: {certificate['animal_id']}\\n"
                   f"Adoption Date: {certificate['timestamp']}\\n"
                   f"Pickup Location: {certificate['pickup_location']}\\n\\n"
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
