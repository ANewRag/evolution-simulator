import random

class Environment:
    def __init__(self, width, height, food_count):
        self.width = width
        self.height = height
        self.food_locations = set()
        self.populate_food(food_count)

    def populate_food(self, food_count):
        while len(self.food_locations) < food_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food_locations.add((x, y))

    def has_food(self, x, y):
        return (x, y) in self.food_locations

    def remove_food(self, x, y):
        if (x, y) in self.food_locations:
            self.food_locations.remove((x, y))

    def display(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in self.food_locations:
                    row += "🍎"
                else:
                    row += "⬜"
            print(row)
