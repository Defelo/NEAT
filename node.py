import math


class Node:
    def __init__(self, no):
        self.number = no
        self.input_sum = 0
        self.output_value = 0
        self.output_connections = []
        self.layer = 0

    def engage(self):
        if self.layer != 0:
            self.output_value = Node.sigmoid(self.input_sum)

        for i in range(len(self.output_connections)):
            if self.output_connections[i].enabled:
                self.output_connections[i].to_node.input_sum += self.output_connections[i].weight * self.output_value

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-4.9 * x))

    def is_connected_to(self, node):
        if node.layer == self.layer:
            return False

        if node.layer < self.layer:
            for i in range(len(node.output_connections)):
                if node.output_connections[i].to_node == self:
                    return True
        else:
            for i in range(len(self.output_connections)):
                if self.output_connections[i].to_node == node:
                    return True
        return False

    def clone(self):
        clone = Node(self.number)
        clone.layer = self.layer
        return clone
