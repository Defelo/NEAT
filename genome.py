import math
from typing import List

from connectiongene import ConnectionGene


class Genome:
    def __init__(self, genome: 'Genome' = None):
        self.fitness: float = 0
        self.adjusted_fitness: float = 0
        self.connection_gene_list: List[ConnectionGene] = []
        if genome is not None:
            self.fitness: float = genome.fitness
            self.adjusted_fitness: float = genome.adjusted_fitness
            self.connection_gene_list: List[ConnectionGene] = genome.connection_gene_list

    @staticmethod
    def cross_over(parent1: 'Genome', parent2: 'Genome') -> 'Genome':
        pass

    @staticmethod
    def is_same_species(genome1: 'Genome', genome2: 'Genome') -> bool:
        pass

    def generate_network(self):
        pass

    def evaluate_network(self, inputs: List[float]) -> List[float]:
        pass

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def mutate(self):
        pass

    def mutate_weight(self):
        pass

    def mutate_add_connection(self):
        pass

    def mutate_add_node(self):
        pass

    def mutate_enable(self):
        pass

    def mutate_disable(self):
        pass
