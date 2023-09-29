from datetime import datetime, timedelta
from Node import Node, ORDER_LIMIT
import random
from Assignee import Assignee

class Chromosome:
    def __init__(self, deadlines: list[datetime], durations: list[timedelta], children: list[int], parents: list[int]) -> None:
        self.nodes = []
        for i in range(len(deadlines)):
            self.nodes.append(Node(deadlines[i], durations[i], child=children[i], parent=parents[i]))
    
    def fitness(self, assignees: list[Assignee]):
        full_duration = 0
        
        self.nodes.sort(key=lambda x: x.order)
        isopen = [False]*len(self.nodes)
        assignments = {assignee.id:[] for assignee in assignees}

        for node in self.nodes:
            assignments[node.assignee].append(node)
            if node.child is None:
                isopen[node.id] == True
        

        while len(assignments) > 0:
            min_assignee = -1
            min_time = 1e10
            for assignee in assignments:
                task = assignments[assignee][0]
                if isopen[task.id] and task.duration < min_time:
                    min_assignee = assignee
            for assignee in assignments:
                task = assignments[assignee][0]
                if isopen[task.id]:
                    task.duration -= min_task
            
            min_task = assignments[min_assignee][0]
            if not min_task.child is None:
                isopen[min_task.id] = True
            
            assignments[min_assignee].pop(0)
            if len(assignments[min_assignee]) == 0:
                del assignments[min_assignee]
            
            full_duration += min_time
        
        self.fitness_score = full_duration
        return full_duration


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