import random
import config

class Organism:
    def __init__(self, speed=1, size=1, x=0, y=0):
        self.speed = speed
        self.size = size
        self.energy = 100
        self.x = x
        self.y = y
        self.is_alive = True

    def __repr__(self):
        return (f"Organism(speed={self.speed}, "
                f"size={self.size}, energy={self.energy}, pos=({self.x},{self.y}))")
    
    def die(self):
        self.is_alive = False

    def eat(self):
        self.energy = min(100, self.energy + 10)

    def move(self, dx, dy):
        # Ensure organism stays within bounds
        self.x = max(0, min(self.x + dx, config.WORLD_WIDTH - 1))
        self.y = max(0, min(self.y + dy, config.WORLD_HEIGHT - 1))

        self.energy -= self.size  # Moving costs energy, larger organisms burn more energy
        if self.energy <= 0: self.die() # Die if out of energy

    def move_randomly(self, environment):
        dirX, dirY = random.choice([(1,0), (-1,0), (0,1), (0, -1)]) # North, South, East, West, respectively
        steps = int(round(random.uniform(1, self.speed)))

        # Eat any food passed along the way
        for i in range(1, steps + 1):
            new_x = max(0, min(self.x + dirX * i, config.WORLD_WIDTH - 1))
            new_y = max(0, min(self.y + dirY * i, config.WORLD_HEIGHT - 1))

            if environment.has_food(new_x, new_y):
                environment.remove_food(new_x, new_y)
                print(f"{self} ate food at ({new_x}, {new_y})")

        self.move(dirX * steps, dirY * steps) # Move
    
    def fitness(self):
        return self.energy
    
    def mutate(self, mutation_strength):
        # Each trait gets a new value sampled from a normal distribution centered on parent trait
        child_speed = max(0.1, random.gauss(self.speed, mutation_strength * self.speed))
        child_size = max(0.1, random.gauss(self.size, mutation_strength * self.size))

        # Prevent exceeding max limits
        child_speed = min(child_speed, config.MAX_SPEED)
        child_size = min(child_size, config.MAX_SIZE)

        return Organism(child_speed, child_size)

