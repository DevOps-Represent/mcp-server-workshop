"""Unit tests for AnimalRescueService with proper test isolation."""

import pytest
from datetime import datetime
from src.animal_rescue_service import AnimalRescueService, Animal, AdoptionCertificate


@pytest.mark.unit
class TestAnimalRescueService:
    """Test suite for AnimalRescueService class."""

    def test_list_animals_returns_available_animals(self, animal_service):
        """Test that list_animals returns only non-adopted animals."""
        animals = animal_service.list_animals()
        
        # Should return a list
        assert isinstance(animals, list)
        assert len(animals) > 0
        
        # All animals should be available for adoption
        for animal in animals:
            assert animal['adopted'] is False
        
        # Should contain expected animals from test data
        animal_names = [animal['name'] for animal in animals]
        assert 'Max' in animal_names
        assert 'Luna' in animal_names

    def test_get_animal_by_id_existing_animal(self, animal_service):
        """Test getting an animal by existing ID."""
        animal = animal_service.get_animal_by_id('dog-001')
        
        assert animal is not None
        assert animal['id'] == 'dog-001'
        assert animal['name'] == 'Max'
        assert animal['species'] == 'dog'
        assert animal['breed'] == 'Golden Retriever'

    def test_get_animal_by_id_nonexistent_animal(self, animal_service):
        """Test getting an animal by non-existent ID."""
        animal = animal_service.get_animal_by_id('nonexistent-id')
        
        assert animal is None

    def test_get_animal_by_name_existing_animal(self, animal_service):
        """Test getting an animal by existing name."""
        animal = animal_service.get_animal_by_name('Max')
        
        assert animal is not None
        assert animal['name'] == 'Max'
        assert animal['id'] == 'dog-001'

    def test_get_animal_by_name_case_insensitive(self, animal_service):
        """Test that name search is case insensitive."""
        animal_lower = animal_service.get_animal_by_name('max')
        animal_upper = animal_service.get_animal_by_name('MAX')
        animal_mixed = animal_service.get_animal_by_name('MaX')
        
        assert animal_lower is not None
        assert animal_upper is not None
        assert animal_mixed is not None
        
        # All should return the same animal
        assert animal_lower['id'] == 'dog-001'
        assert animal_upper['id'] == 'dog-001'
        assert animal_mixed['id'] == 'dog-001'

    def test_get_animal_by_name_nonexistent_animal(self, animal_service):
        """Test getting an animal by non-existent name."""
        animal = animal_service.get_animal_by_name('NonexistentName')
        
        assert animal is None

    def test_adopt_animal_successful(self, animal_service):
        """Test successful animal adoption."""
        # First, ensure the animal is available
        animal = animal_service.get_animal_by_id('dog-001')
        assert animal is not None
        assert animal['adopted'] is False
        
        # Adopt the animal
        certificate = animal_service.adopt_animal('dog-001')
        
        # Should return adoption certificate
        assert certificate is not None
        assert certificate['animal_id'] == 'dog-001'
        assert certificate['pickup_location'] == "123 Main St, Anytown, USA"
        assert 'timestamp' in certificate
        
        # Verify timestamp is recent (within last minute)
        timestamp = datetime.fromisoformat(certificate['timestamp'])
        now = datetime.now()
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 60  # Less than 1 minute ago
        
        # Animal should now be marked as adopted
        updated_animal = animal_service.get_animal_by_id('dog-001')
        assert updated_animal['adopted'] is True

    def test_adopt_animal_already_adopted(self, animal_service):
        """Test adopting an animal that's already adopted."""
        # First adoption
        certificate1 = animal_service.adopt_animal('dog-002')
        assert certificate1 is not None
        
        # Second adoption attempt should fail
        certificate2 = animal_service.adopt_animal('dog-002')
        assert certificate2 is None

    def test_adopt_animal_nonexistent_id(self, animal_service):
        """Test adopting an animal with non-existent ID."""
        certificate = animal_service.adopt_animal('nonexistent-id')
        
        assert certificate is None

    def test_list_animals_excludes_adopted(self, animal_service):
        """Test that list_animals excludes adopted animals."""
        # Get initial count
        initial_animals = animal_service.list_animals()
        initial_count = len(initial_animals)
        
        # Adopt an animal
        animal_service.adopt_animal('dog-003')
        
        # List should now have one fewer animal
        updated_animals = animal_service.list_animals()
        assert len(updated_animals) == initial_count - 1
        
        # The adopted animal should not be in the list
        animal_ids = [animal['id'] for animal in updated_animals]
        assert 'dog-003' not in animal_ids

    def test_animal_data_structure(self, animal_service):
        """Test that animal data has expected structure."""
        animals = animal_service.list_animals()
        
        # Test first animal structure
        animal = animals[0]
        expected_keys = {
            'id', 'name', 'species', 'breed', 'age', 'gender', 'size', 
            'color', 'description', 'vaccinated', 'spayed_neutered', 
            'good_with_kids', 'good_with_pets', 'energy_level', 
            'adoption_fee', 'date_arrived', 'adopted'
        }
        
        assert set(animal.keys()) == expected_keys
        
        # Test data types
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

    def test_adoption_certificate_structure(self, animal_service):
        """Test that adoption certificate has expected structure."""
        certificate = animal_service.adopt_animal('cat-001')
        
        assert certificate is not None
        
        expected_keys = {'animal_id', 'timestamp', 'pickup_location'}
        assert set(certificate.keys()) == expected_keys
        
        # Test data types
        assert isinstance(certificate['animal_id'], str)
        assert isinstance(certificate['timestamp'], str)
        assert isinstance(certificate['pickup_location'], str)
        
        # Verify timestamp is valid ISO format
        try:
            datetime.fromisoformat(certificate['timestamp'])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")

    def test_service_initialization(self):
        """Test that service initializes with correct data."""
        service = AnimalRescueService()
        
        # Should have animals available
        animals = service.list_animals()
        assert len(animals) > 0
        
        # Should have specific test animals
        animal_names = [animal['name'] for animal in animals]
        expected_names = ['Max', 'Luna', 'Bella', 'Whiskers', 'Charlie', 'Mittens', 'Cocoa', 'Rocky']
        
        for name in expected_names:
            assert name in animal_names


@pytest.mark.integration
class TestAnimalRescueServiceIntegration:
    """Integration tests for AnimalRescueService."""

    def test_full_adoption_workflow(self, animal_service):
        """Test complete adoption workflow."""
        # 1. List all animals
        all_animals = animal_service.list_animals()
        initial_count = len(all_animals)
        
        # 2. Find a specific animal (use cat-002 instead of Max)
        target_animal = animal_service.get_animal_by_name('Whiskers')
        assert target_animal is not None
        target_id = target_animal['id']
        
        # 3. Get animal by ID
        same_animal = animal_service.get_animal_by_id(target_id)
        assert same_animal == target_animal
        
        # 4. Adopt the animal
        certificate = animal_service.adopt_animal(target_id)
        assert certificate is not None
        assert certificate['animal_id'] == target_id
        
        # 5. Verify animal is no longer available
        updated_animals = animal_service.list_animals()
        assert len(updated_animals) == initial_count - 1
        
        # 6. Verify animal is marked as adopted
        adopted_animal = animal_service.get_animal_by_id(target_id)
        assert adopted_animal['adopted'] is True
        
        # 7. Verify cannot adopt again
        second_certificate = animal_service.adopt_animal(target_id)
        assert second_certificate is None
