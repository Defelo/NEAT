from typing import List, Callable

from genome import Genome
from neatconfig import *
from species import Species


class Pool:
    def __init__(self):
        self.species: List[Species] = []
        for _ in range(POPULATION):
            self.add_to_species(Genome())

    def add_to_species(self, genome: Genome):
        pass

    def evaluate_fitness(self, d: Callable[[Genome], float]):
        pass

    def get_top_genome(self) -> Genome:
        pass

    def calculate_global_adjusted_fitness(self) -> float:
        pass

    def remove_weak_gnomes_from_species(self):
        pass

    def calculate_gnome_adjusted_fitness(self) -> float:
        pass

    def breed_new_generation(self):
        pass
