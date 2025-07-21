import random
import config

class Organism:
    def __init__(self, speed=1, size=1, x=0, y=0, inital_energy=200, move_cost=10, reproduction_cost=50, reproduction_baseline=75, reproduction_rate=0.1):
        self.speed = speed
        self.size = size
        self.x = x
        self.y = y
        self.energy = inital_energy
        self.move_cost = move_cost
        self.reproduction_cost = reproduction_cost
        self.reproduction_baseline = reproduction_baseline
        self.reproduction_rate = reproduction_rate
        self.is_alive = True

    def __repr__(self):
        return (f"Organism(speed={self.speed}, "
                f"size={self.size}, energy={self.energy}, pos=({self.x},{self.y}))")
    
    def die(self):
        self.is_alive = False
        self.energy = 0 

    def eat(self, energy):
        self.energy = self.energy + energy

    def move(self, dx, dy):
        # Ensure organism stays within bounds
        self.x = max(0, min(self.x + dx, config.WORLD_WIDTH - 1))
        self.y = max(0, min(self.y + dy, config.WORLD_HEIGHT - 1))

        self.energy -= self.move_cost  # Moving costs energy, larger organisms burn more energy
        if self.energy <= 0: self.die() # Die if out of energy

    # Default movement behavior, can be overridden by subclasses
    def move_randomly(self, *args, **kwargs):
        dirX, dirY = random.choice([(1,0), (-1,0), (0,1), (0, -1)]) # North, South, East, West, respectively
        steps = int(round(random.uniform(1, self.speed))) # Move a random number of steps based on speed

        self.move(dirX * steps, dirY * steps) # Move
    
    def fitness(self):
        return self.energy
    
    def mutate(self, mutation_strength):
        # Each trait gets a new value sampled from a normal distribution centered on parent trait
        child_speed = max(1, random.gauss(self.speed, mutation_strength * self.speed))
        child_size = max(1, random.gauss(self.size, mutation_strength * self.size))

        # Prevent exceeding max limits
        child_speed = min(child_speed, config.MAX_SPEED)
        child_size = min(child_size, config.MAX_SIZE)

        # Set random initial position
        child_x = random.randint(0, config.WORLD_WIDTH - 1)
        child_y = random.randint(0, config.WORLD_HEIGHT - 1)

        return Organism(child_speed, child_size, child_x, child_y)



class Prey(Organism):
    def __init__(self, speed=1, size=1, x=0, y=0):
        super().__init__(speed=speed, size=size, x=x, y=y, move_cost=size)
        self.type = "Prey"

    def __repr__(self):
        return f"Prey(speed={self.speed}, size={self.size}, pos=({self.x},{self.y}))"
    
    def move_randomly(self, environment):
        dirX, dirY = random.choice([(1,0), (-1,0), (0,1), (0, -1)]) # North, South, East, West, respectively
        steps = int(round(random.uniform(1, self.speed))) # Move a random number of steps based on speed

        # Eat any food passed along the way
        for i in range(1, steps + 1):
            new_x = max(0, min(self.x + dirX * i, config.WORLD_WIDTH - 1))
            new_y = max(0, min(self.y + dirY * i, config.WORLD_HEIGHT - 1))

            # Eat food
            if environment.has_food(new_x, new_y):
                environment.remove_food(new_x, new_y)
                self.eat(50)

        self.move(dirX * steps, dirY * steps) # Move

    
class Predator(Organism):
    def __init__(self, speed=1, size=1, x=0, y=0):
        super().__init__(speed, size, x, y, move_cost=size)
        self.type = "Predator"

    def __repr__(self):
        return f"Predator(speed={self.speed}, size={self.size}, pos=({self.x},{self.y}))"
    
    def move_randomly(self, prey_list):
        dirX, dirY = random.choice([(1,0), (-1,0), (0,1), (0, -1)]) # North, South, East, West, respectively
        steps = int(round(random.uniform(1, self.speed))) # Move a random number of steps based on speed

        # Eat any oranism passed along the way
        for i in range(1, steps + 1):
            new_x = max(0, min(self.x + dirX * i, config.WORLD_WIDTH - 1))
            new_y = max(0, min(self.y + dirY * i, config.WORLD_HEIGHT - 1))
            # Eat other organisms
            for org in prey_list:
                if (
                    org.is_alive and 
                    self.is_alive and
                    org.x == new_x and 
                    org.y == new_y and 
                    org.size < self.size
                ):
                    # Consume the other organism
                    self.eat(org.size * 20) # Energy gained is proportional to size of prey
                    org.die()

        self.move(dirX * steps, dirY * steps) # Move