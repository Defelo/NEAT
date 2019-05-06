class ConnectionGene:
    def __init__(self, into: int, out: int, innovation: int, weight: float, enabled: bool):
        self.into: int = into
        self.out: int = out
        self.innovation: int = innovation
        self.weight: float = weight
        self.enabled: bool = enabled

    def copy(self) -> 'ConnectionGene':
        return ConnectionGene(self.into, self.out, self.innovation, self.weight, self.enabled)
