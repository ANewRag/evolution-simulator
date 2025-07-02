from environment import Environment
from organism import Organism
from population_manager import PopulationManager

if __name__ == "__main__":
    PM = PopulationManager()
    environment = Environment()
    print("Initial Population:")
    environment.display(PM.get_organism_list())