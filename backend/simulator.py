from environment import Environment
from population_manager import PopulationManager
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = Environment()
    PM = PopulationManager(env)

    print("\nSimulating Generations...")
    PM.simulateGeneration()

    # --- PLOTTING RESULTS ---
    # Extract values
    ticks = [h["ticks"] for h in PM.history]
    num_prey = [h["num_prey"] for h in PM.history]
    num_predators = [h["num_predators"] for h in PM.history]

    avg_size_prey = [h["avg_size_prey"] for h in PM.history]
    avg_size_predator = [h["avg_size_predator"] for h in PM.history]

    avg_speed_prey = [h["avg_speed_prey"] for h in PM.history]
    avg_speed_predator = [h["avg_speed_predator"] for h in PM.history]

    # --- Population ---
    plt.figure("Population Over Time", figsize=(8, 4))
    plt.plot(ticks, num_prey, label="Prey")
    plt.plot(ticks, num_predators, label="Predators")
    plt.title("Population Over Time")
    plt.xlabel("Ticks")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)

    # --- Size ---
    """ plt.figure("Average Size", figsize=(8, 4))
    plt.plot(ticks, avg_size_prey, label="Prey")
    plt.plot(ticks, avg_size_predator, label="Predators")
    plt.title("Average Size Over Time")
    plt.xlabel("Generation")
    plt.ylabel("Size")
    plt.legend()
    plt.grid(True) """

    # --- Speed ---
    """ plt.figure("Average Speed", figsize=(8, 4))
    plt.plot(ticks, avg_speed_prey, label="Prey")
    plt.plot(ticks, avg_speed_predator, label="Predators")
    plt.title("Average Speed Over Time")
    plt.xlabel("Generation")
    plt.ylabel("Speed")
    plt.legend()
    plt.grid(True) """

    # Show all at once
    plt.show()
    print([h["food_count"] for h in PM.history])


    """ # Speed
    plt.figure(figsize=(10, 5))
    plt.plot(generations, avg_speed_prey, label="Prey")
    plt.plot(generations, avg_speed_predator, label="Predator")
    plt.xlabel("Generation")
    plt.ylabel("Average Speed")
    plt.title("Average Speed Over Time")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Size
    plt.figure(figsize=(10, 5))
    plt.plot(generations, avg_size_prey, label="Prey")
    plt.plot(generations, avg_size_predator, label="Predator")
    plt.xlabel("Generation")
    plt.ylabel("Average Size")
    plt.title("Average Size Over Time")
    plt.legend()
    plt.tight_layout()
    plt.show() """

