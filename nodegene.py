from typing import List

from connectiongene import ConnectionGene


class NodeGene:
    def __init__(self, value: float):
        self.value: float = value
        self.incoming: List[ConnectionGene] = []
