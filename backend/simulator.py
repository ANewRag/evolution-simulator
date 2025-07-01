from environment import Environment
from organism import Organism

if __name__ == "__main__":
    env = Environment(width=10, height=10, food_count=20)
    org = Organism(speed=2, vision_range=3, size=1)
    org.x, org.y = 5, 5

    print("Before movement:")
    env.display()
    print(org)

    for i in range(100): org.move_randomly(env)

    print("\nAfter movement:")
    env.display()
    print(org)