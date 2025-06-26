class Organism:
    def __init__(self, speed, vision_range, size):
        self.speed = speed
        self.vision_range = vision_range
        self.size = size

    def __repr__(self):
        return f"Organism(speed={self.speed}, vision={self.vision_range}, size={self.size})"

if __name__ == "__main__":
    test = Organism(5, 10, 2)
    print(test)