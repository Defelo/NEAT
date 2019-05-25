import random


class ConnectionGene:
    def __init__(self, frm, to, w, inno):
        self.frm_node = frm
        self.to_node = to
        self.weight = w
        self.innovation_no = inno
        self.enabled = True

    def mutate_weight(self):
        rand2 = random.random()
        if rand2 < 0.1:
            self.weight = random.random() * 2 - 1
        else:
            self.weight += random.gauss(0, 1) / 2
            self.weight = min(1, self.weight)
            self.weight = max(self.weight, -1)

    def clone(self, frm, to):
        clone = ConnectionGene(frm, to, self.weight, self.innovation_no)
        clone.enabled = self.enabled
        return clone
