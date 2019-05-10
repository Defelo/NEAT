from typing import List, Tuple

from genome import Genome
from neatconfig import *

TestCase = Tuple[List[float], List[float]]


class Evaluator:
    def __init__(self, test_cases: List[TestCase]):
        self.test_cases: List[TestCase] = test_cases

    def evaluate(self, genome: Genome) -> float:
        fitness: float = 0
        for network_input, expected_output in self.test_cases:
            network_output: List[float] = genome.evaluate_network(network_input)
            error: float = 0
            for expected, actual in zip(expected_output, network_output):
                error += abs(expected - actual)
            fitness += OUTPUTS - error
        return fitness
