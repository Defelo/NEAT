import math
import random
from typing import List, Dict

from connectiongene import ConnectionGene
from innovationcounter import InnovationCounter
from neatconfig import *
from nodegene import NodeGene


class Genome:
    def __init__(self, genome: 'Genome' = None):
        self.fitness: float = 0
        self.adjusted_fitness: float = 0
        self.connection_gene_list: List[ConnectionGene] = []
        self.nodes: Dict[int, NodeGene] = {}
        if genome is not None:
            self.fitness: float = genome.fitness
            self.adjusted_fitness: float = genome.adjusted_fitness
            for connection in genome.connection_gene_list:
                self.connection_gene_list.append(connection.copy())

    @staticmethod
    def cross_over(parent1: 'Genome', parent2: 'Genome') -> 'Genome':
        if parent1.fitness < parent2.fitness:
            parent1, parent2 = parent2, parent1

        gene_map1: Dict[int, ConnectionGene] = {}
        gene_map2: Dict[int, ConnectionGene] = {}
        for connection in parent1.connection_gene_list:
            gene_map1[connection.innovation] = connection
        for connection in parent2.connection_gene_list:
            gene_map2[connection.innovation] = connection

        child: Genome = Genome()
        for key in {*gene_map1, *gene_map2}:
            if key in gene_map1 and key in gene_map2:
                trait: ConnectionGene = random.choice([gene_map1, gene_map2])[key].copy()
                if (not gene_map1[key].enabled) or (not gene_map2[key].enabled) and random.random() < 0.75:
                    trait.enabled = False
            elif parent1.fitness == parent2.fitness:
                trait: ConnectionGene = random.choice([gene_map1, gene_map2]).get(key, None)
            else:
                trait: ConnectionGene = gene_map1.get(key, None)

            if trait is not None:
                child.connection_gene_list.append(trait.copy())

        return child

    @staticmethod
    def is_same_species(genome1: 'Genome', genome2: 'Genome') -> bool:
        gene_map1: Dict[int, ConnectionGene] = {}
        gene_map2: Dict[int, ConnectionGene] = {}
        for connection in genome1.connection_gene_list:
            gene_map1[connection.innovation] = connection
        for connection in genome2.connection_gene_list:
            gene_map2[connection.innovation] = connection

        matching: int = 0
        disjoint: int = 0
        excess: int = 0

        weight: float = 0
        max_innovation: int = min(max([0, *gene_map1]), max([0, *gene_map2]))

        for key in {*gene_map1, *gene_map2}:
            if key in gene_map1 and key in gene_map2:
                matching += 1
                weight += abs(gene_map1[key].weight - gene_map2[key].weight)
            elif key <= max_innovation:
                disjoint += 1
            else:
                excess += 1
        n: int = max(len(gene_map1), len(gene_map2))
        if n:
            delta: float = EXCESS_COEFFICIENT * excess + DISJOINT_COEFFICIENT * disjoint
            delta /= n
            if matching > 0:
                delta += WEIGHT_COEFFICIENT * weight / matching
            return delta < COMPATIBILITY_THRESHOLD
        return True

    def generate_network(self):
        self.nodes.clear()

        for i in range(INPUTS):
            self.nodes[i] = NodeGene(0)
        self.nodes[INPUTS] = NodeGene(1)

        for i in range(INPUTS + 1, INPUTS + 1 + OUTPUTS):
            self.nodes[i] = NodeGene(0)

        for connection in self.connection_gene_list:
            if connection.into not in self.nodes:
                self.nodes[connection.into] = NodeGene(0)
            if connection.out not in self.nodes:
                self.nodes[connection.out] = NodeGene(0)
            self.nodes[connection.out].incoming.append(connection)

    def evaluate_network(self, inputs: List[float]) -> List[float]:
        self.generate_network()

        for i in range(INPUTS):
            self.nodes[i].value = inputs[i]

        for i in [*filter(lambda i: i >= INPUTS + OUTPUTS + 1, sorted(self.nodes)), *range(INPUTS + 1, INPUTS + 1 + OUTPUTS)]:
            self.nodes[i].value = Genome.sigmoid(
                sum(
                    self.nodes[connection.into].value * connection.weight * connection.enabled
                    for connection in self.nodes[i].incoming
                )
            )
        return [self.nodes[i].value for i in range(INPUTS + 1, INPUTS + 1 + OUTPUTS)]

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-4.9 * x))

    def mutate(self):
        if random.random() < WEIGHT_MUTATION_CHANCE:
            self.mutate_weight()
        if random.random() < CONNECTION_MUTATION_CHANCE:
            self.mutate_add_connection()
        if random.random() < NODE_MUTATION_CHANCE:
            self.mutate_add_node()
        if random.random() < ENABLE_MUTATION_CHANCE:
            self.mutate_enable()
        if random.random() < DISABLE_MUTATION_CHANCE:
            self.mutate_disable()

    def mutate_weight(self):
        for connection in self.connection_gene_list:
            if random.random() < WEIGHT_CHANCE:
                if random.random() < PERTURB_CHANCE:
                    connection.weight += (2 * random.random() - 1) * STEPS
                else:
                    connection.weight = 4 * random.random() - 2

    def mutate_add_connection(self):
        self.generate_network()
        random1: int = random.choice([*filter(lambda i: i < INPUTS + 1 or i >= INPUTS + 1 + OUTPUTS, self.nodes)])
        random2: int = random.choice([*filter(lambda i: i >= INPUTS + 1, self.nodes)])
        if random1 >= random2:
            return
        if any(connection.into == random1 and connection.out == random2 for connection in self.connection_gene_list):
            return
        self.connection_gene_list.append(
            ConnectionGene(random1, random2, InnovationCounter.new_innovation(), 4 * random.random() - 2, True)
        )

    def mutate_add_node(self):
        enabled: List[ConnectionGene] = [*filter(lambda con: con.enabled, self.connection_gene_list)]
        if not enabled:
            return
        self.generate_network()
        connection: ConnectionGene = random.choice(enabled)
        connection.enabled = False
        next_node: int = max(self.nodes) + 1
        self.connection_gene_list.append(
            ConnectionGene(connection.into, next_node, InnovationCounter.new_innovation(), 1, True)
        )
        self.connection_gene_list.append(
            ConnectionGene(next_node, connection.out, InnovationCounter.new_innovation(), connection.weight, True)
        )

    def mutate_enable(self):
        if self.connection_gene_list:
            connection: ConnectionGene = random.choice(self.connection_gene_list)
            connection.enabled = True

    def mutate_disable(self):
        if self.connection_gene_list:
            connection: ConnectionGene = random.choice(self.connection_gene_list)
            connection.enabled = False
