from datetime import datetime, timedelta
from Node import Node, ORDER_LIMIT
import random

class Chromosome:
    def __init__(self, deadlines: list[datetime], durations: list[timedelta], children: list[int], parents: list[int]) -> None:
        self.nodes = []
        for i in range(len(deadlines)):
            self.nodes.append(Node(deadlines[i], durations[i]))
        for i in range(len(deadlines)):
            if children[i] is not None:
                self.nodes[i].child = self.nodes[children[i]]
            if parents[i] is not None:
                self.nodes[i].parent = self.nodes[parents[i]]
    
    def fitness(self):
        pass

    def mutate(self, assignees, mut_num: int=1):
        mutated_node = Chromosome(self.nodes)
        for i in range(mut_num):
            node_ind = int(random.random() * len(self.nodes))
            assignee_ind = int(random.random() * len(assignees))
            mutated_node.nodes[node_ind].assignee = assignees[assignee_ind]
            mutated_node.nodes[node_ind].order = random.random() * ORDER_LIMIT
        mutated_node.__correct_order()
        return mutated_node

    def crossover(self, chromosome, change_rate: float=0.5):
        if change_rate >= 1 or change_rate <= 0:
            change_rate = 0.5
        mutated_node = Chromosome(self.nodes)
        for i in range(len(self.nodes)):
            if random.random() > change_rate:
                mutated_node.nodes[i] = chromosome.nodes[i].copy()
        mutated_node.__correct_order()
        return mutated_node

    def __correct_order(self):
        pass