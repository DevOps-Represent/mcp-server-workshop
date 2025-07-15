"""Integration tests for MCP server."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.main import call_tool, list_tools


@pytest.mark.integration
class TestMCPServer:
    """Test suite for MCP server integration."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_expected_tools(self):
        """Test that list_tools returns all expected tools."""
        tools = await list_tools()

        assert isinstance(tools, list)
        assert len(tools) == 4

        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "list_animals",
            "get_animal_by_id",
            "get_animal_by_name",
            "adopt_pet",
        ]

        for expected_tool in expected_tools:
            assert expected_tool in tool_names

    @pytest.mark.asyncio
    async def test_list_tools_structure(self):
        """Test that tools have correct structure."""
        tools = await list_tools()

        for tool in tools:
            # Each tool should have required fields
            assert hasattr(tool, "name")
            assert hasattr(tool, "description")
            assert hasattr(tool, "inputSchema")

            # Input schema should be valid JSON schema
            schema = tool.inputSchema
            assert schema["type"] == "object"
            assert "properties" in schema
            assert "required" in schema

    @pytest.mark.asyncio
    async def test_call_tool_list_animals(self):
        """Test calling list_animals tool."""
        result = await call_tool("list_animals", {})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Available animals for adoption:" in result[0].text
        assert "Max" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_id_valid(self):
        """Test calling get_animal_by_id with valid ID."""
        result = await call_tool("get_animal_by_id", {"animal_id": "dog-001"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"

        text = result[0].text
        assert "Animal Details:" in text
        assert "Name: Max" in text
        assert "Species: dog" in text
        assert "Breed: Golden Retriever" in text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_id_invalid(self):
        """Test calling get_animal_by_id with invalid ID."""
        result = await call_tool("get_animal_by_id", {"animal_id": "invalid-id"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "No animal found with ID: invalid-id" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_id_missing_param(self):
        """Test calling get_animal_by_id without required parameter."""
        result = await call_tool("get_animal_by_id", {})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: animal_id is required" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_name_valid(self):
        """Test calling get_animal_by_name with valid name."""
        result = await call_tool("get_animal_by_name", {"name": "Max"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"

        text = result[0].text
        assert "Found animal: Max" in text
        assert "Species: dog" in text
        assert "Breed: Golden Retriever" in text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_name_case_insensitive(self):
        """Test calling get_animal_by_name with different cases."""
        result_lower = await call_tool("get_animal_by_name", {"name": "max"})
        result_upper = await call_tool("get_animal_by_name", {"name": "MAX"})

        # Both should find the animal
        assert "Found animal: Max" in result_lower[0].text
        assert "Found animal: Max" in result_upper[0].text

    @pytest.mark.asyncio
    async def test_call_tool_get_animal_by_name_invalid(self):
        """Test calling get_animal_by_name with invalid name."""
        result = await call_tool("get_animal_by_name", {"name": "InvalidName"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "No animal found with name: InvalidName" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_adopt_pet_valid(self):
        """Test calling adopt_pet with valid ID."""
        result = await call_tool("adopt_pet", {"animal_id": "dog-002"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"

        text = result[0].text
        assert "🎉 Adoption successful!" in text
        assert "Adoption Certificate:" in text
        assert "Animal ID: dog-002" in text
        assert "Pickup Location: 123 Main St, Anytown, USA" in text

    @pytest.mark.asyncio
    async def test_call_tool_adopt_pet_invalid_id(self):
        """Test calling adopt_pet with invalid ID."""
        result = await call_tool("adopt_pet", {"animal_id": "invalid-id"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "No animal found with name or ID: invalid-id" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_adopt_pet_missing_param(self):
        """Test calling adopt_pet without required parameter."""
        result = await call_tool("adopt_pet", {})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: animal_id is required" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self):
        """Test calling unknown tool."""
        result = await call_tool("unknown_tool", {})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Unknown tool: unknown_tool" in result[0].text

    @pytest.mark.asyncio
    async def test_adoption_workflow(self):
        """Test complete adoption workflow through MCP server."""
        # 1. List animals
        animals_result = await call_tool("list_animals", {})
        assert "Available animals for adoption:" in animals_result[0].text

        # 2. Get specific animal
        animal_result = await call_tool("get_animal_by_id", {"animal_id": "cat-001"})
        assert "Animal Details:" in animal_result[0].text
        assert "Name: Luna" in animal_result[0].text

        # 3. Adopt the animal
        adoption_result = await call_tool("adopt_pet", {"animal_id": "cat-001"})
        assert "🎉 Adoption successful!" in adoption_result[0].text

        # 4. Try to adopt again (should fail)
        second_adoption = await call_tool("adopt_pet", {"animal_id": "cat-001"})
        assert "Unable to adopt animal with ID: cat-001" in second_adoption[0].text

        # 5. List animals again (should not include adopted animal)
        updated_animals = await call_tool("list_animals", {})
        # Luna should not be in the list anymore
        assert "Luna" not in updated_animals[0].text


@pytest.mark.integration
class TestMCPServerErrorHandling:
    """Test error handling in MCP server."""

    @pytest.mark.asyncio
    async def test_call_tool_with_none_arguments(self):
        """Test calling tool with None arguments."""
        result = await call_tool("get_animal_by_id", None)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: animal_id is required" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_with_empty_string_parameter(self):
        """Test calling tool with empty string parameter."""
        result = await call_tool("get_animal_by_id", {"animal_id": ""})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: animal_id is required" in result[0].text

    @pytest.mark.asyncio
    async def test_call_tool_with_wrong_parameter_name(self):
        """Test calling tool with wrong parameter name."""
        result = await call_tool("get_animal_by_id", {"wrong_param": "dog-001"})

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: animal_id is required" in result[0].text


@pytest.mark.integration
@pytest.mark.slow
class TestMCPServerPerformance:
    """Test MCP server performance and concurrent operations."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self):
        """Test concurrent tool calls."""
        # Create multiple concurrent tool calls
        tasks = [
            call_tool("list_animals", {}),
            call_tool("get_animal_by_id", {"animal_id": "dog-001"}),
            call_tool("get_animal_by_name", {"name": "Max"}),
            call_tool("get_animal_by_id", {"animal_id": "cat-001"}),
            call_tool("get_animal_by_name", {"name": "Luna"}),
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # All should succeed
        assert len(results) == 5

        # Verify results
        assert "Available animals for adoption:" in results[0][0].text
        assert "Name: Max" in results[1][0].text
        assert "Found animal: Max" in results[2][0].text
        assert "Name: Luna" in results[3][0].text
        assert "Found animal: Luna" in results[4][0].text

    @pytest.mark.asyncio
    async def test_multiple_adoptions_different_animals(self):
        """Test adopting multiple different animals concurrently."""
        # Create concurrent adoption tasks for different animals
        tasks = [
            call_tool("adopt_pet", {"animal_id": "dog-003"}),
            call_tool("adopt_pet", {"animal_id": "cat-002"}),
            call_tool("adopt_pet", {"animal_id": "rabbit-001"}),
        ]

        results = await asyncio.gather(*tasks)

        # All adoptions should succeed
        for result in results:
            assert "🎉 Adoption successful!" in result[0].text

    @pytest.mark.asyncio
    async def test_response_format_consistency(self):
        """Test that all tool responses have consistent format."""
        test_cases = [
            ("list_animals", {}),
            ("get_animal_by_id", {"animal_id": "dog-001"}),
            ("get_animal_by_name", {"name": "Max"}),
            ("adopt_pet", {"animal_id": "dog-004"}),
            ("unknown_tool", {}),
        ]

        for tool_name, args in test_cases:
            result = await call_tool(tool_name, args)

            # All responses should be lists
            assert isinstance(result, list)
            assert len(result) >= 1

            # Each item should have type and text
            for item in result:
                assert hasattr(item, "type")
                assert hasattr(item, "text")
                assert item.type == "text"
                assert isinstance(item.text, str)
