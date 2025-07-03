from environment import Environment
from population_manager import PopulationManager
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = Environment()
    PM = PopulationManager(env)

    print("\nSimulating Generations...")
    PM.simulateEpoch()

    # --- PLOTTING RESULTS ---
    # Extract historical values
    generations = [entry["generation"] for entry in PM.history]
    days = [entry["days_survived"] for entry in PM.history]
    speed = [entry["avg_speed"] for entry in PM.history]
    size = [entry["avg_size"] for entry in PM.history]

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(generations, days, label="Days Survived")
    plt.xlabel("Generation")
    plt.ylabel("Days Survived")
    plt.title("Survival Over Time")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(generations, speed, label="Speed")
    plt.plot(generations, size, label="Size")
    plt.xlabel("Generation")
    plt.ylabel("Trait Values")
    plt.title("Trait Evolution")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
