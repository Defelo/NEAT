class InnovationCounter:
    innovation: int = 0

    @staticmethod
    def new_innovation():
        InnovationCounter.innovation += 1
        return InnovationCounter.innovation
