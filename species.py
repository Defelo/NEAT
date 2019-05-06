from typing import List

from genome import Genome


class Species:
    def __init__(self, genome: Genome = None):
        self.genomes: List[Genome] = []
        if genome is not None:
            self.genomes.append(genome)

    def calculate_genome_adjusted_fitness(self):
        pass

    def get_total_adjusted_fitness(self) -> float:
        pass

    def remove_weak_genomes(self):
        pass

    def get_top_genome(self) -> Genome:
        pass

    def breed_child(self) -> Genome:
        pass
