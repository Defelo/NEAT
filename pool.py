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
        for species in self.species:
            if Genome.is_same_species(species.genomes[0], genome):
                species.genomes.append(genome)
                return
        self.species.append(Species(genome))

    def evaluate_fitness(self, evaluator: Callable[[Genome], float]):
        for species in self.species:
            for genome in species.genomes:
                genome.fitness = evaluator(genome)

    def get_top_genome(self) -> Genome:
        top_genome: Genome = None
        for species in self.species:
            genome: Genome = species.get_top_genome()
            if top_genome is None or genome.fitness > top_genome.fitness:
                top_genome = genome
        return top_genome

    def calculate_total_adjusted_fitness(self) -> float:
        return sum(species.get_total_adjusted_fitness() for species in self.species)

    def remove_weak_genomes_from_species(self):
        for species in self.species:
            species.remove_weak_genomes()

    def calculate_genome_adjusted_fitness(self):
        for species in self.species:
            species.calculate_genome_adjusted_fitness()

    def breed_new_generation(self):
        self.calculate_genome_adjusted_fitness()
        total_adjusted_fitness: float = self.calculate_total_adjusted_fitness()

        self.remove_weak_genomes_from_species()

        survived_species: List[Species] = []
        children: List[Genome] = []

        carry_over: float = 0
        for species in self.species:
            fchild: float = POPULATION * (species.get_total_adjusted_fitness() / total_adjusted_fitness)
            nchild: int = int(fchild)
            carry_over += fchild - nchild
            if carry_over >= 1:
                carry_over -= 1
                nchild += 1

            if nchild < 1:
                continue

            survived_species.append(Species(species.get_top_genome()))
            for _ in range(1, nchild):
                children.append(species.breed_child())

        self.species: List[Species] = survived_species
        for child in children:
            self.add_to_species(child)
