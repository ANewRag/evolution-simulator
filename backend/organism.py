import random
from config import WORLD_WIDTH, WORLD_HEIGHT

class Organism:
    def __init__(self, speed, vision_range, size):
        self.speed = speed
        self.vision_range = vision_range
        self.size = size
        self.energy = 100
        self.x = 0
        self.y = 0

    def __repr__(self):
        return (f"Organism(speed={self.speed}, vision={self.vision_range}, "
                f"size={self.size}, energy={self.energy}, pos=({self.x},{self.y}))")
    
    def eat(self):
        self.energy = min(100, self.energy + 10)

    def move(self, dx, dy):
        # Ensure organism stays within bounds
        self.x = max(0, min(self.x + dx, WORLD_WIDTH - 1))
        self.y = max(0, min(self.y + dy, WORLD_HEIGHT - 1))
        self.energy -= 1  # Moving costs energy

    def move_randomly(self, environment):
        dirX, dirY = random.choice([(1,0), (-1,0), (0,1), (0, -1)]) # North, South, East, West, respectively

        # Eat any food passed along the way (will lead to bugs where multiple organisms eat the same food)
        for i in range(1, self.speed + 1):
            new_x = max(0, min(self.x + dirX * i, WORLD_WIDTH - 1))
            new_y = max(0, min(self.y + dirY * i, WORLD_HEIGHT - 1))

            if environment.has_food(new_x, new_y):
                environment.remove_food(new_x, new_y)
                print(f"{self} ate food at ({new_x}, {new_y})")

        self.move(dirX * self.speed, dirY * self.speed) # Move
    

