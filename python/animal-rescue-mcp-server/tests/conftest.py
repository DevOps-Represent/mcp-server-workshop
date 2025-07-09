"""Test configuration and fixtures."""

import pytest
import asyncio
from typing import Generator
from src.animal_rescue_service import AnimalRescueService


@pytest.fixture
def animal_service() -> AnimalRescueService:
    """Create a fresh AnimalRescueService instance for each test."""
    return AnimalRescueService()


@pytest.fixture
def sample_animal_data() -> dict:
    """Provide sample animal data for tests."""
    return {
        'id': 'test-001',
        'name': 'TestPet',
        'species': 'dog',
        'breed': 'Test Breed',
        'age': 3,
        'gender': 'male',
        'size': 'medium',
        'color': 'brown',
        'description': 'A test animal for testing purposes',
        'vaccinated': True,
        'spayed_neutered': True,
        'good_with_kids': True,
        'good_with_pets': True,
        'energy_level': 'medium',
        'adoption_fee': 200,
        'date_arrived': '2024-01-01',
        'adopted': False
    }


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_animal_ids() -> list:
    """Provide list of known animal IDs for testing."""
    return ['dog-001', 'cat-001', 'dog-002', 'cat-002', 'dog-003', 'cat-003', 'rabbit-001', 'dog-004']


@pytest.fixture
def mock_animal_names() -> list:
    """Provide list of known animal names for testing."""
    return ['Max', 'Luna', 'Bella', 'Whiskers', 'Charlie', 'Mittens', 'Cocoa', 'Rocky']


class TestHelper:
    """Helper class for common test operations."""
    
    @staticmethod
    def assert_animal_structure(animal: dict) -> None:
        """Assert that an animal has the expected structure."""
        required_fields = {
            'id', 'name', 'species', 'breed', 'age', 'gender', 'size',
            'color', 'description', 'vaccinated', 'spayed_neutered',
            'good_with_kids', 'good_with_pets', 'energy_level',
            'adoption_fee', 'date_arrived', 'adopted'
        }
        
        assert set(animal.keys()) == required_fields
        assert isinstance(animal['id'], str)
        assert isinstance(animal['name'], str)
        assert isinstance(animal['species'], str)
        assert isinstance(animal['breed'], str)
        assert isinstance(animal['age'], int)
        assert animal['gender'] in ['male', 'female']
        assert animal['size'] in ['small', 'medium', 'large']
        assert isinstance(animal['color'], str)
        assert isinstance(animal['description'], str)
        assert isinstance(animal['vaccinated'], bool)
        assert isinstance(animal['spayed_neutered'], bool)
        assert isinstance(animal['good_with_kids'], bool)
        assert isinstance(animal['good_with_pets'], bool)
        assert animal['energy_level'] in ['low', 'medium', 'high']
        assert isinstance(animal['adoption_fee'], int)
        assert isinstance(animal['date_arrived'], str)
        assert isinstance(animal['adopted'], bool)
    
    @staticmethod
    def assert_adoption_certificate_structure(certificate: dict) -> None:
        """Assert that an adoption certificate has the expected structure."""
        required_fields = {'animal_id', 'timestamp', 'pickup_location'}
        
        assert set(certificate.keys()) == required_fields
        assert isinstance(certificate['animal_id'], str)
        assert isinstance(certificate['timestamp'], str)
        assert isinstance(certificate['pickup_location'], str)
    
    @staticmethod
    def assert_mcp_response_structure(response: list) -> None:
        """Assert that an MCP response has the expected structure."""
        assert isinstance(response, list)
        assert len(response) >= 1
        
        for item in response:
            assert isinstance(item, dict)
            assert 'type' in item
            assert 'text' in item
            assert item['type'] == 'text'
            assert isinstance(item['text'], str)


@pytest.fixture
def test_helper() -> TestHelper:
    """Provide test helper instance."""
    return TestHelper()
