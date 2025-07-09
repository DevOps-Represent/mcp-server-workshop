# Test Guide for Animal Rescue MCP Server

## Overview

This project includes comprehensive tests for both the business logic and MCP server integration.

## Test Structure

```
tests/
├── __init__.py                        # Test package initialization
├── conftest.py                        # Test fixtures and configuration
├── test_animal_rescue_service_fixed.py # Unit tests for AnimalRescueService
└── test_mcp_server.py                 # Integration tests for MCP server
```

## Running Tests

### Install Test Dependencies

```bash
python3 -m pip install -r requirements-test.txt
```

Or install with development dependencies:

```bash
python3 -m pip install -e .[dev]
```

### Run All Tests

```bash
python3 -m pytest
```

### Run Specific Test Files

```bash
# Unit tests only
python3 -m pytest tests/test_animal_rescue_service_fixed.py

# MCP server tests only  
python3 -m pytest tests/test_mcp_server.py
```

### Run with Coverage

```bash
python3 -m pytest --cov=src --cov-report=html
```

### Run with Verbose Output

```bash
python3 -m pytest -v
```

### Run Specific Test Categories

```bash
# Run only unit tests
python3 -m pytest -m unit

# Run only integration tests
python3 -m pytest -m integration

# Skip slow tests
python3 -m pytest -m "not slow"
```

## Test Categories

### Unit Tests (`test_animal_rescue_service_fixed.py`)

Tests the core business logic without external dependencies:

- **Animal listing**: Test listing available animals
- **Animal retrieval**: Test getting animals by ID and name
- **Adoption workflow**: Test animal adoption process
- **Data validation**: Test data structure and types
- **Error handling**: Test edge cases and invalid inputs

**Key test methods:**
- `test_list_animals_returns_available_animals`
- `test_get_animal_by_id_existing_animal`
- `test_adopt_animal_successful`
- `test_adoption_certificate_structure`

### Integration Tests (`test_mcp_server.py`)

Tests the MCP server protocol and tool integration:

- **Tool registration**: Test that tools are properly registered
- **Tool execution**: Test calling tools with various parameters
- **Response format**: Test MCP protocol response structure
- **Error handling**: Test server error responses
- **Performance**: Test concurrent tool calls

**Key test methods:**
- `test_list_tools_returns_expected_tools`
- `test_call_tool_list_animals`
- `test_adoption_workflow`
- `test_concurrent_tool_calls`

## Test Fixtures

### Available Fixtures (from `conftest.py`)

- `animal_service`: Fresh AnimalRescueService instance per test
- `sample_animal_data`: Sample animal data for testing
- `mock_animal_ids`: List of known animal IDs
- `mock_animal_names`: List of known animal names
- `test_helper`: Helper methods for assertions

### Test Helper Methods

```python
def test_example(test_helper, animal_service):
    animal = animal_service.get_animal_by_id('dog-001')
    test_helper.assert_animal_structure(animal)
    
    certificate = animal_service.adopt_animal('dog-001')
    test_helper.assert_adoption_certificate_structure(certificate)
```

## Test Data

Tests use the same animal data as the main application:

- **8 animals** total (dogs, cats, rabbit)
- **Known IDs**: dog-001, cat-001, dog-002, etc.
- **Known names**: Max, Luna, Bella, Whiskers, Charlie, Mittens, Cocoa, Rocky

## Common Test Patterns

### Testing Animal Retrieval

```python
def test_get_animal_by_id(animal_service):
    animal = animal_service.get_animal_by_id('dog-001')
    assert animal is not None
    assert animal['name'] == 'Max'
```

### Testing Adoption Workflow

```python
def test_adopt_animal(animal_service):
    certificate = animal_service.adopt_animal('dog-001')
    assert certificate is not None
    assert certificate['animal_id'] == 'dog-001'
```

### Testing MCP Tools

```python
@pytest.mark.asyncio
async def test_mcp_tool():
    result = await call_tool('list_animals', {})
    assert isinstance(result, list)
    assert result[0]['type'] == 'text'
```

## Coverage Goals

- **Unit tests**: 100% coverage of AnimalRescueService
- **Integration tests**: 100% coverage of MCP tool handlers
- **Overall**: 80% minimum coverage (configured in pytest.ini)

## Continuous Integration

Tests are configured to run with:
- **pytest**: Test runner
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **pytest.ini**: Test configuration

## Writing New Tests

### For New Service Methods

1. Add unit tests in `test_animal_rescue_service_fixed.py`
2. Use `animal_service` fixture for fresh instances
3. Test both success and failure cases
4. Verify data structure and types

### For New MCP Tools

1. Add integration tests in `test_mcp_server.py`
2. Test tool registration in `test_list_tools_*`
3. Test tool execution in `test_call_tool_*`
4. Test error handling and edge cases

### Example New Test

```python
def test_new_feature(animal_service):
    """Test new feature functionality."""
    # Arrange
    setup_data = {...}
    
    # Act
    result = animal_service.new_method(setup_data)
    
    # Assert
    assert result is not None
    assert result['expected_field'] == 'expected_value'
```

## Debugging Failed Tests

### Common Issues

1. **Test isolation**: Ensure tests don't affect each other
2. **Data state**: Check if animal adoption state affects tests
3. **Async issues**: Ensure proper async/await usage
4. **MCP protocol**: Verify response format matches expected structure

### Debugging Commands

```bash
# Run single test with full output
python3 -m pytest tests/test_file.py::test_method -v -s

# Run with debugger
python3 -m pytest tests/test_file.py::test_method --pdb

# Run with coverage and see missed lines
python3 -m pytest --cov=src --cov-report=term-missing
```

## Performance Testing

The test suite includes performance tests for:
- Concurrent tool calls
- Multiple simultaneous adoptions
- Response time consistency

Run performance tests specifically:
```bash
python3 -m pytest tests/test_mcp_server.py::TestMCPServerPerformance -v
```
