import { ANIMALS_DATA } from './animal-data';

export interface Animal {
  id: string;
  name: string;
  species: string;
  breed: string;
  age: number;
  gender: 'male' | 'female';
  size: 'small' | 'medium' | 'large';
  color: string;
  description: string;
  vaccinated: boolean;
  spayedNeutered: boolean;
  goodWithKids: boolean;
  goodWithPets: boolean;
  energyLevel: 'low' | 'medium' | 'high';
  adoptionFee: number;
  dateArrived: string;
  adopted: boolean;
}

// This is running in memory, ideally this would a deployed REST API that your MCP server communicates with, with a database.
export class AnimalRescueService {
  private animals: Animal[] = [...ANIMALS_DATA];

  listAnimals(): Animal[] {
    return this.animals.filter(animal => !animal.adopted);
  }

  getAnimal(id: string): Animal | null {
    const animal = this.animals.find(animal => animal.id === id);
    return animal || null;
  }

  adoptAnimal(id: string): boolean {
    const animal = this.animals.find(animal => animal.id === id);
    if (animal && !animal.adopted) {
      animal.adopted = true;
      return true;
    }
    return false;
  }
}
