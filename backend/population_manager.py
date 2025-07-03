from organism import Organism
import random
import config

class PopulationManager:
    def __init__(self, environment):
        assert(config.NUM_ORGANISMS > config.NUM_REPRODUCING)
        self.num_organisms = config.NUM_ORGANISMS
        self.num_reproducing = config.NUM_REPRODUCING
        self.num_generations = config.NUM_GENERATIONS
        self.mutation_strength = config.MUTATION_STRENGTH
        self.environment = environment
        
        self.num_dead = 0
        self.organism_list = []
        self.generation = 1
        
        # Randomly initialize the first generation
        for i in range(self.num_organisms):
            speed = random.randint(1, 10)
            size = random.randint(1, 10)
            x = random.randint(0, config.WORLD_WIDTH - 1)
            y = random.randint(0, config.WORLD_HEIGHT - 1)
            self.organism_list.append(Organism(speed=speed, size=size, x=x, y=y))

        self.history = []  # Store history of generations

    def get_organism_list(self):
        return self.organism_list
        
    def simulateGeneration(self):
        days = 0
        # Still have more living organisms than can reproduce
        while self.num_dead < self.num_organisms - self.num_reproducing:
            for organism in self.organism_list:
                if organism.is_alive:
                    organism.move_randomly(self.environment)

                    if not organism.is_alive: # Died after moving
                        self.num_dead += 1
                if self.num_dead >= self.num_organisms - self.num_reproducing:
                    break

            days += 1
        if __debug__:
            print(f"Genration {self.generation} survived for {days} days")

        # Record generation stats
        avg_energy = sum(org.energy for org in self.organism_list) / len(self.organism_list)
        avg_speed = sum(org.speed for org in self.organism_list) / len(self.organism_list)
        avg_size = sum(org.size for org in self.organism_list) / len(self.organism_list)

        self.history.append({
        "generation": len(self.history),
        "days_survived": days,
        "avg_energy": avg_energy,
        "avg_speed": avg_speed,
        "avg_size": avg_size
        })



    # Creates new list of organisms based on the top survivors from the previous generaiton
    def reproduce(self):
        assert(self.num_organisms - self.num_dead == self.num_reproducing)
        new_organism_list = []

        # Sort organisms by fitness and take the top survivors
        sorted_organisms = sorted(self.organism_list, key=lambda org: org.fitness(), reverse=True)
        parents = sorted_organisms[:self.num_reproducing]
        
        while len(new_organism_list) < self.num_organisms:
            # Create children from parents (asexual reproduction with mutation)
            for parent in parents:
                if len(new_organism_list) >= self.num_organisms: break
                child = parent.mutate(self.mutation_strength)
                new_organism_list.append(child)
        
        assert(len(new_organism_list) == self.num_organisms)
        return new_organism_list



    def simulateEpoch(self):
        while self.generation <= self.num_generations:
            print(f"\nSimulating Generation {self.generation}...")
            # self.environment.display(self.organism_list)

            self.simulateGeneration()

            # self.environment.display(self.organism_list)
            print(f"\nEnd of Generation {self.generation}.")

            self.organism_list = self.reproduce()
            self.environment.populate_food()  # Replenish food after each generation
            self.num_dead = 0  # Reset dead count for the next generation

            
            
            self.generation += 1
