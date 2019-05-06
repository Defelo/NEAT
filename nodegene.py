from typing import List

from connectiongene import ConnectionGene


class NodeGene:
    def __init__(self):
        self.value: float = 0
        self.incoming: List[ConnectionGene] = []
