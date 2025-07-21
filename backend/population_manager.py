from organism import Predator, Prey
import random
import config

class PopulationManager:
    def __init__(self, environment):
        self.num_prey = int(config.NUM_ORGANISMS * config.PERCENT_PREY)
        self.num_predators = int(config.NUM_ORGANISMS * (1 - config.PERCENT_PREY))
        self.prey_list = []
        self.predator_list = []

        self.mutation_strength = config.MUTATION_STRENGTH
        self.environment = environment
        
        self.ticks = 0
        
        # Randomly initialize the first generation
        for _ in range(self.num_prey):
            speed = random.randint(1, 10)
            size = random.randint(1, 10)
            x = random.randint(0, config.WORLD_WIDTH - 1)
            y = random.randint(0, config.WORLD_HEIGHT - 1)
            self.prey_list.append(Prey(speed=speed, size=size, x=x, y=y))

        for _ in range(self.num_predators):
            speed = random.randint(1, 10)
            size = random.randint(1, 10)
            x = random.randint(0, config.WORLD_WIDTH - 1)
            y = random.randint(0, config.WORLD_HEIGHT - 1)
            self.predator_list.append(Predator(speed=speed, size=size, x=x, y=y))
        
        self.history = []  # Store history of generations

    def get_organism_list(self):
        return self.prey_list + self.predator_list
    
    def count_alive_prey(self):
        return sum(1 for org in self.prey_list if org.is_alive)
    
    def count_alive_predators(self):
        return sum(1 for org in self.predator_list if org.is_alive)
    
    # Creates new list of organisms based on the top survivors from the previous generaiton
    def reproduce(self):
        new_prey_list = []
        new_predator_list = []
        
        for org in self.prey_list:
            if org.is_alive and org.energy >= org.reproduction_baseline and random.random() < org.reproduction_rate:
                child = org.mutate(self.mutation_strength)
                org.energy -= org.reproduction_cost
                new_prey_list.append(child)

        for org in self.predator_list:
            if org.is_alive and org.energy >= org.reproduction_baseline and random.random() < org.reproduction_rate:
                child = org.mutate(self.mutation_strength)
                org.energy -= org.reproduction_cost
                new_predator_list.append(child)
        
        # Comvine the new organisms with the survivors
        self.prey_list = [org for org in self.prey_list if org.is_alive] + new_prey_list
        self.predator_list = [org for org in self.predator_list if org.is_alive] + new_predator_list

    
    def tick(self):
        self.environment.spawn_food()  # Spawn food at the start of each tick

        for organism in self.prey_list:
            if organism.is_alive:
                organism.move_randomly(self.environment)

        for organism in self.predator_list:
            if organism.is_alive:
                organism.move_randomly(self.prey_list)
        
        self.reproduce()  # Handle reproduction after movement
        self.ticks += 1

    def record_history(self):
        avg_energy_prey = sum(org.energy for org in self.prey_list) / len(self.prey_list) if len(self.prey_list) > 0 else 0
        avg_speed_prey = sum(org.speed for org in self.prey_list) / len(self.prey_list) if len(self.prey_list) > 0 else 0
        avg_size_prey = sum(org.size for org in self.prey_list) / len(self.prey_list) if len(self.prey_list) > 0 else 0

        avg_energy_predator = sum(org.energy for org in self.predator_list) / len(self.predator_list) if len(self.predator_list) > 0 else 0
        avg_speed_predator = sum(org.speed for org in self.predator_list) / len(self.predator_list) if len(self.predator_list) > 0 else 0
        avg_size_predator = sum(org.size for org in self.predator_list) / len(self.predator_list) if len(self.predator_list) > 0 else 0

        self.history.append({
        "ticks": self.ticks,
        "num_prey": self.count_alive_prey(),
        "num_predators": self.count_alive_predators(),
        "avg_energy_prey": avg_energy_prey,
        "avg_speed_prey": avg_speed_prey,
        "avg_size_prey": avg_size_prey,
        "avg_energy_predator": avg_energy_predator,
        "avg_speed_predator": avg_speed_predator,
        "avg_size_predator": avg_size_predator,
        "food_count": self.environment.food_count()
        })

        
    def simulateEpoch(self):
        # Still have more living organisms than can reproduce
        for i in range(config.NUM_TICKS):
            self.tick()
            
            # Record history every 100 ticks
            if i % 10 == 0:
                self.record_history()


"""     def simulateEpoch(self):
        while self.generation <= config.NUM_GENERATIONS:
            print(f"\nSimulating Generation {self.generation}...")
            # self.environment.display(self.organism_list)

            self.simulateGeneration()

            # self.environment.display(self.organism_list)
            print(f"\nEnd of Generation {self.generation}.")

            self.environment.populate_food()  # Replenish food after each generation
            
            self.generation += 1
 """