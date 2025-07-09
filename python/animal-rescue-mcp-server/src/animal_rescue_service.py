"""Animal rescue service for managing adoptions."""

from datetime import datetime
from typing import List, Literal, Optional, TypedDict


class Animal(TypedDict):
    """Animal data structure."""

    id: str
    name: str
    species: str
    breed: str
    age: int
    gender: Literal["male", "female"]
    size: Literal["small", "medium", "large"]
    color: str
    description: str
    vaccinated: bool
    spayed_neutered: bool
    good_with_kids: bool
    good_with_pets: bool
    energy_level: Literal["low", "medium", "high"]
    adoption_fee: int
    date_arrived: str
    adopted: bool


class AdoptionCertificate(TypedDict):
    """Adoption certificate data structure."""

    animal_id: str
    timestamp: str
    pickup_location: str


class AnimalRescueService:
    """Service for managing animal adoptions.

    This is running in memory, ideally this would be a deployed REST API
    that your MCP server communicates with, with a database.
    """

    def __init__(self) -> None:
        """Initialize the service with animal data."""
        from .animal_data import ANIMALS_DATA
        import copy

        self.animals: List[Animal] = copy.deepcopy(ANIMALS_DATA)

    def list_animals(self) -> List[Animal]:
        """List all available animals for adoption."""
        return [animal for animal in self.animals if not animal["adopted"]]

    def get_animal_by_id(self, animal_id: str) -> Optional[Animal]:
        """Get an animal by its ID."""
        for animal in self.animals:
            if animal["id"] == animal_id:
                return animal
        return None

    def get_animal_by_name(self, name: str) -> Optional[Animal]:
        """Get an animal by its name (case insensitive)."""
        print(f"get_animal_by_name: {name}")

        for animal in self.animals:
            if animal["name"].lower() == name.lower():
                print(f"animal: {animal}")
                return animal
        return None

    def adopt_animal(self, animal_id: str) -> Optional[AdoptionCertificate]:
        """Adopt an animal and return an adoption certificate."""
        animal = self.get_animal_by_id(animal_id)

        if animal and not animal["adopted"]:
            # Return a new adoption certificate with fake pickup location and current time
            pickup_location = "123 Main St, Anytown, USA"
            timestamp = datetime.now().isoformat()

            adoption_certificate: AdoptionCertificate = {
                "animal_id": animal_id,
                "timestamp": timestamp,
                "pickup_location": pickup_location,
            }

            animal["adopted"] = True
            return adoption_certificate

        return None
