class ConnectionHistory:
    def __int__(self, frm, to, inno, innovation_nos):
        self.frm_node = frm
        self.to_node = to
        self.inno = inno
        self.innovation_nos = innovation_nos.copy()

    def matches(self, genome, frm, to):
        if len(genome.genes) == len(self.innovation_nos):
            if frm.number == self.frm_node and to.number == self.to_node:
                for i in range(len(genome.genes)):
                    if genome.genes[i].innovation_no not in self.innovation_nos:
                        return False
                return True
        return False
