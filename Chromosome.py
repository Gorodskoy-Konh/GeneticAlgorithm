from datetime import datetime, timedelta
from Node import Node, ORDER_LIMIT
import random
from Assignee import Assignee

class Chromosome:
    def __init__(self, deadlines: list[datetime], durations: list[timedelta], children: list[int], parents: list[int], assignees: list[Assignee]) -> None:
        self.nodes = []
        self.deadlines = deadlines
        self.durations = durations
        self.children = children
        self.parents = parents
        self.assignees = assignees
        for i in range(len(deadlines)):
            assignee_random_idx = int(random.random() * len(assignees))
            self.nodes.append(Node(deadlines[i], durations[i], i, assignees[assignee_random_idx]))
        for i in range(len(deadlines)):
            if children[i] is not None:
                self.nodes[i].child = self.nodes[children[i]]
            if parents[i] is not None:
                self.nodes[i].parent = self.nodes[parents[i]]    
                
    def fitness(self, assignees: list[Assignee]):
        full_duration = timedelta(seconds=0)
        
        self.nodes.sort(key=lambda x: x.order)
        isopen = [False]*len(self.nodes)
        assignments = {assignee.id:[] for assignee in assignees}

        for node in self.nodes:
            assignments[node.assignee.id].append(node)
            if node.child is None:
                isopen[node.id] = True
        # print(assignments)

        while len(assignments) > 0:
            print('\n')
            min_assignee = -1
            min_time = timedelta(days=1e3)
            for assignee in assignments:
                print(assignee, 'value =', assignments[assignee])
                if len(assignments[assignee]) == 0:
                    continue
                task = assignments[assignee][0]
                if isopen[task.id] and task.duration < min_time:
                    min_assignee = assignee
            for assignee in assignments:
                if len(assignments[assignee]) == 0:
                    continue
                task = assignments[assignee][0]
                if isopen[task.id]:
                    task.duration -= min_time
            print(min_assignee)
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
        mutated_node = Chromosome(self.deadlines, self.durations, self.children, self.parents, self.assignees)
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
        mutated_node = Chromosome(self.deadlines, self.durations, self.children, self.parents, self.assignees)
        for i in range(len(self.nodes)):
            if random.random() > change_rate:
                mutated_node.nodes[i] = chromosome.nodes[i].copy()
        mutated_node.__correct_order()
        return mutated_node

    def __correct_order(self):
        pass
