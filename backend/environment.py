import random
import config

class Environment:
    def __init__(self):
        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT
        self.food_locations = set()
        self.populate_food()

    def populate_food(self):
        while len(self.food_locations) < config.FOOD_AMOUNT:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food_locations.add((x, y))

    def has_food(self, x, y):
        return (x, y) in self.food_locations

    def remove_food(self, x, y):
        if (x, y) in self.food_locations:
            self.food_locations.remove((x, y))

    def display(self, organism_list):
        org_map = {(org.x, org.y): org for org in organism_list} if organism_list else {}

        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in org_map:
                    org = org_map[(x, y)]
                    if org.is_alive:
                        row += "🟢"
                    else:
                        row += "🔴"
                elif (x, y) in self.food_locations:
                    row += "🍔"
                else:
                    row += "⬜"
            print(row)
