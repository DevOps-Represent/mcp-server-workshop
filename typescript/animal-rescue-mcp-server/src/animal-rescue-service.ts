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

export const adoptionCertificateSchema = z.object({
  animalId: z.string(),
  timestamp: z.string(),
  pickupLocation: z.string(),
});

export type Animal = z.infer<typeof animalSchema>;

export type AdoptionCertificate = z.infer<typeof adoptionCertificateSchema>;

// This is running in memory, ideally this would a deployed REST API that your MCP server communicates with, with a database.
export class AnimalRescueService {
  private animals: Animal[] = [...ANIMALS_DATA];

  async listAnimals(): Promise<Animal[]> {
    return this.animals.filter(animal => !animal.adopted);
  }

  async getAnimalById(id: string): Promise<Animal | null> {
    const animal = this.animals.find(animal => animal.id === id);
    return animal || null;
  }

  async getAnimalByName(name: string): Promise<Animal | null> {
    console.log("getAnimalByName", name);


    const animal = this.animals.find(animal => animal.name.toLowerCase() === name.toLowerCase());
    console.log("animal", animal);

    
    return animal || null;
  }

  async adoptAnimal(id: string): Promise<AdoptionCertificate | null> {
    const animal = this.animals.find(animal => animal.id === id);
    // return a new adoption certificate with a fake pickup location and curent time
    const pickupLocation = "123 Main St, Anytown, USA";
    const timestamp = new Date().toISOString();
    const adoptionCertificate: AdoptionCertificate = {
      animalId: id,
      timestamp,
      pickupLocation
    };
    if (animal && !animal.adopted) {
      animal.adopted = true;
      return adoptionCertificate;
    }
    return null;
  }
}
