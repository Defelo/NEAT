from typing import List

from evaluator import Evaluator
from genome import Genome
from pool import Pool

evaluator: Evaluator = Evaluator([([i, j], [i ^ j]) for i in range(2) for j in range(2)])
pool: Pool = Pool(300, 2, 1)
generation: int = 1
top_genome: Genome = None
while True:
    pool.evaluate_fitness(evaluator.evaluate)
    top_genome: Genome = pool.get_top_genome()
    print(f"Generation {generation} | Top Fitness: {top_genome.fitness} | Species: {len(pool.species)} | Total Genomes: {sum(len(s.genomes) for s in pool.species)}")
    if top_genome.fitness > 3.9:
        break
    pool.breed_new_generation()
    generation += 1

for network_input, _ in evaluator.test_cases:
    network_output: List[float] = top_genome.evaluate_network(network_input)
    print(network_input, "->", network_output)
