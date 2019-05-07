from typing import List

from genome import Genome
from pool import Pool


def evaluate(genome: Genome) -> float:
    fitness: float = 0
    for i in range(2):
        for j in range(2):
            fitness += 1 - abs((i ^ j) - genome.evaluate_network([i, j])[0])
    return fitness ** 2


pool: Pool = Pool()
generation: int = 1
while True:
    pool.evaluate_fitness(evaluate)
    top_genome: Genome = pool.get_top_genome()
    print(f"Generation {generation} | Top Fitness: {top_genome.fitness} | Species: {len(pool.species)}")
    if top_genome.fitness > 15:
        break
    pool.breed_new_generation()
    generation += 1

for i in range(2):
    for j in range(2):
        network_input: List[float] = [i, j]
        network_output: List[float] = top_genome.evaluate_network(network_input)
        print(network_input, "->", network_output)
