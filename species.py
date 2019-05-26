import random

from neatconfig import *


class Species:
    def __init__(self, p=None):
        self.genomes = []
        self.best_fitness = 0
        self.average_fitness = 0
        self.staleness = 0
        self.rep = None
        self.champ = None
        if p is not None:
            self.genomes.append(p)
            self.best_fitness = p.fitness
            self.rep = p.clone()
            self.champ = p.clone()

    def same_species(self, g):
        excess_and_disjoint = self.get_excess_disjoint(g, self.rep)
        average_weight_diff = self.average_weight_diff(g, self.rep)

        large_genome_normaliser = len(g.genes) - 20
        if large_genome_normaliser < 1:
            large_genome_normaliser = 1

        compatibility = EXCESS_COEFFICIENT * excess_and_disjoint / large_genome_normaliser
        compatibility += WEIGHT_COEFFICIENT * average_weight_diff
        return compatibility < COMPATIBILITY_THRESHOLD

    def add_to_species(self, p):
        self.genomes.append(p)

    def get_excess_disjoint(self, brain1, brain2):
        matching = 0
        for i in range(len(brain1.genes)):
            for j in range(len(brain2.genes)):
                if brain1.genes[i].innovation_no == brain2.genes[j].innovation_no:
                    matching += 1
                    break
        return len(brain1.genes) + len(brain2.genes) - 2 * matching

    def average_weight_diff(self, brain1, brain2):
        if len(brain1.genes) == 0 or len(brain2.genes) == 0:
            return 0

        matching = 0
        total_diff = 0
        for i in range(len(brain1.genes)):
            for j in range(len(brain2.genes)):
                if brain1.genes[i].innovation_no == brain2.genes[j].innovation_no:
                    matching += 1
                    total_diff += abs(brain1.genes[i].weight - brain2.genes[j].weight)
                    break
        if matching == 0:
            return 100
        return total_diff / matching

    def sort_species(self):
        temp = []

        for _ in range(len(self.genomes)):
            mx = 0
            max_index = 0
            for i in range(len(self.genomes)):
                if self.genomes[i].fitness > mx:
                    mx = self.genomes[i].fitness
                    max_index = i
            temp.append(self.genomes[max_index])
            del self.genomes[max_index]

        genomes = temp.copy()
        if len(genomes) == 0:
            self.staleness = 200
            return

        if self.genomes[0].fitness > self.best_fitness:
            self.staleness = 0
            self.best_fitness = self.genomes[0].fitness
            self.rep = self.genomes[0]
            self.champ = self.genomes[0].clone()
        else:
            self.staleness += 1

    def set_average(self):
        s = 0
        for i in range(len(self.genomes)):
            s += self.genomes[i].fitness
        self.average_fitness = s / len(self.genomes)

    def give_me_baby(self, innovation_history):
        if random.random() < 0.25:
            baby = self.select_genome().clone()
        else:
            parent1 = self.select_genome()
            parent2 = self.select_genome()
            if parent1.fitness < parent2.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby = parent1.crossover(parent2)
        baby.mutate(innovation_history)
        return baby

    def select_genome(self):
        fitness_sum = 0
        for i in range(len(self.genomes)):
            fitness_sum += self.genomes[i].fitness

        rand = random.random() * fitness_sum
        running_sum = 0

        for i in range(len(self.genomes)):
            running_sum += self.genomes[i].fitness
            if running_sum > rand:
                return self.genomes[i]
        assert False

    def cull(self):
        if len(self.genomes) > 2:
            self.genomes = self.genomes[:len(self.genomes) // 2]

    def fitness_sharing(self):
        for i in range(len(self.genomes)):
            self.genomes[i].fitness /= len(self.genomes)
