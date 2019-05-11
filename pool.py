from typing import List, Callable

from genome import Genome
from species import Species


class Pool:
    def __init__(self, population: int, input_nodes: int, output_nodes: int):
        self.population: int = population
        self.input_nodes: int = input_nodes
        self.output_nodes = output_nodes
        self.species: List[Species] = []
        for _ in range(population):
            self.add_to_species(Genome(input_nodes, output_nodes))

    def add_to_species(self, genome: Genome):
        for species in self.species:
            if Genome.is_same_species(species.genomes[0], genome):
                species.genomes.append(genome)
                species.previous_top_fitness = max(species.previous_top_fitness, genome.fitness)
                return
        self.species.append(Species(genome))

    def evaluate_fitness(self, evaluator: Callable[[Genome], float]):
        for species in self.species:
            for genome in species.genomes:
                genome.fitness = evaluator(genome)

    def get_top_genome(self) -> Genome:
        return max((species.get_top_genome() for species in self.species), key=lambda genome: genome.fitness)

    def calculate_total_adjusted_fitness(self) -> float:
        return sum(species.get_total_adjusted_fitness() for species in self.species)

    def remove_weak_genomes_from_species(self):
        for species in self.species:
            species.remove_weak_genomes()

    def calculate_genome_adjusted_fitness(self):
        for species in self.species:
            species.calculate_genome_adjusted_fitness()

    def remove_stale_species(self):
        top_top_fitness: float = self.get_top_genome().fitness
        for i in range(len(self.species))[::-1]:
            species: Species = self.species[i]
            top_fitness: float = species.get_top_genome().fitness
            if top_fitness <= species.previous_top_fitness:
                species.staleness += 1
            else:
                species.staleness = 0
            species.previous_top_fitness = top_fitness
            if species.staleness >= 15 and top_fitness < top_top_fitness:
                del self.species[i]

    def breed_new_generation(self):
        self.calculate_genome_adjusted_fitness()

        self.remove_weak_genomes_from_species()
        self.remove_stale_species()

        survived_species: List[Species] = []
        children: List[Genome] = []

        total_adjusted_fitness: float = self.calculate_total_adjusted_fitness()

        carry_over: float = 0
        for species in self.species:
            fchild: float = self.population * (species.get_total_adjusted_fitness() / total_adjusted_fitness)
            nchild: int = int(fchild)
            carry_over += fchild - nchild
            if carry_over >= 1:
                carry_over -= 1
                nchild += 1

            if nchild < 1:
                continue

            new_species: Species = Species(species.get_top_genome())
            new_species.previous_top_fitness = species.previous_top_fitness
            new_species.staleness = species.staleness
            survived_species.append(new_species)
            for _ in range(1, nchild):
                children.append(species.breed_child())

        self.species: List[Species] = survived_species
        for child in children:
            self.add_to_species(child)
