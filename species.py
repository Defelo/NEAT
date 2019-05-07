import math
import random
from typing import List

from genome import Genome
from neatconfig import *


class Species:
    def __init__(self, genome: Genome = None):
        self.genomes: List[Genome] = []
        self.previous_top_fitness: float = 0
        self.staleness: int = 0
        if genome is not None:
            self.genomes.append(genome)

    def calculate_genome_adjusted_fitness(self):
        for genome in self.genomes:
            genome.adjusted_fitness = genome.fitness / len(self.genomes)

    def get_total_adjusted_fitness(self) -> float:
        return sum(genome.adjusted_fitness for genome in self.genomes)

    def remove_weak_genomes(self):
        self.genomes.sort(key=lambda genome: genome.fitness, reverse=True)
        survive_count: int = math.ceil(len(self.genomes) / 2)
        self.genomes: List[Genome] = self.genomes[:survive_count]

    def get_top_genome(self) -> Genome:
        return max(self.genomes, key=lambda genome: genome.fitness)

    def breed_child(self) -> Genome:
        if random.random() < CROSSOVER_CHANCE:
            parent1: Genome = random.choice(self.genomes)
            parent2: Genome = random.choice(self.genomes)
            child: Genome = Genome.cross_over(parent1, parent2)
        else:
            child: Genome = Genome(random.choice(self.genomes))
        child.mutate()
        return child
