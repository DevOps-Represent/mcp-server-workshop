import { z } from 'zod';
import { ANIMALS_DATA } from './animal-data';

export const animalSchema = z.object({
  id: z.string(),
  name: z.string(),
  species: z.string(),
  breed: z.string(),
  age: z.number(),
  gender: z.enum(['male', 'female']),
  size: z.enum(['small', 'medium', 'large']),
  color: z.string(),
  description: z.string(),
  vaccinated: z.boolean(),
  spayedNeutered: z.boolean(),
  goodWithKids: z.boolean(),
  goodWithPets: z.boolean(),
  energyLevel: z.enum(['low', 'medium', 'high']),
  adoptionFee: z.number(),
  dateArrived: z.string(),
  adopted: z.boolean(),
});

export type Animal = z.infer<typeof animalSchema>;

// This is running in memory, ideally this would a deployed REST API that your MCP server communicates with, with a database.
export class AnimalRescueService {
  private animals: Animal[] = [...ANIMALS_DATA];

  listAnimals(): Animal[] {
    return this.animals.filter(animal => !animal.adopted);
  }

  getAnimalById(id: string): Animal | null {
    const animal = this.animals.find(animal => animal.id === id);
    return animal || null;
  }

  getAnimalByName(name: string): Animal | null {
    const animal = this.animals.find(animal => animal.name.toLowerCase() === name.toLowerCase());
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
