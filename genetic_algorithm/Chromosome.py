from datetime import datetime, timedelta
from .Node import Node, ORDER_LIMIT
import random
from .Assignee import Assignee

class Chromosome:
    def __init__(self, nodes: list[Node], assignees: list[Assignee], maximum_stack_difference: int) -> None:
        self.nodes = []
        self.assignees = assignees
        self.maximum_stack_difference = maximum_stack_difference
        for node in nodes:
            self.nodes.append(node.copy())
            if node.fixed_assignee:
                continue
            assignee_random_idx = int(random.random() * len(assignees))
            self.nodes[-1].assignee = assignees[assignee_random_idx]
        for i in range(len(nodes)):
            self.nodes[i].children = [self.nodes[node.id] for node in nodes[i].children]
            self.nodes[i].parents = [self.nodes[node.id] for node in self.nodes[i].parents]
        #self.__correct_order()

    def fitness(self):
        full_duration = timedelta(seconds=0)
        full_stack_difference = 0

        assignments = {assignee.id:[] for assignee in self.assignees}
        for node in self.nodes:
            assignments[node.assignee.id].append(node)
        
        total_similarity = 0
        for assignee in assignments:
            similarity = 0
            for i in range(len(assignments[assignee])-1):
                if not assignments[assignee][i].project is None and not assignments[assignee][i+1].project is None:
                    similarity += (assignments[assignee][i].project == assignments[assignee][i+1].project)
            if len(assignments[assignee]) == 0:
                similarity = 0
            else:
                similarity = similarity/len(assignments[assignee])
            total_similarity += similarity
        try:
            self.calcate_start_times()
        except:
            self.fitness_score = timedelta(days=1e3).total_seconds()
            return self.fitness_score

        for node in self.nodes:
            full_duration = max(full_duration, node.start + node.duration)

        self.fitness_score = full_duration.total_seconds() * (1 + full_stack_difference/max(self.maximum_stack_difference, 1) - total_similarity/len(self.assignees))
        return self.fitness_score


    def mutate(self, assignees, mut_chance: float=0.2):
        mutated_chromosome = self.copy()
        for i in range(len(self.nodes)):
            if self.nodes[i].fixed_assignee:
                continue
            if random.random() < mut_chance:
                assignee_ind = int(random.random() * len(assignees))
                mutated_chromosome.nodes[i].assignee = assignees[assignee_ind]
                mutated_chromosome.nodes[i].order = random.random() * ORDER_LIMIT
        #mutated_chromosome.__correct_order()
        return mutated_chromosome

    def crossover(self, chromosome, change_rate: float=0.5):
        if change_rate >= 1 or change_rate <= 0:
            change_rate = 0.5
        mutated_node = self.copy()
        for i in range(len(self.nodes)):
            if self.nodes[i].fixed_assignee:
                continue
            if random.random() > change_rate:
                mutated_node.nodes[i] = chromosome.nodes[i].copy()
        #mutated_node.__correct_order()
        return mutated_node

    def copy(self):
        nodes = []
        for node in self.nodes:
            nodes.append(node.copy())
        return Chromosome(nodes, self.assignees, self.maximum_stack_difference)
    
    def calcate_start_times(self):
        nodes = []
        for node in self.nodes:
            node_copy = node.copy()
            node_copy.start = None
            nodes.append(node_copy)
        nodes.sort(key=lambda x: x.order)
        assignments = {assignee.id:[] for assignee in self.assignees}
        assignees_time = {assignee.id:timedelta(seconds=0) for assignee in self.assignees}
        isopen = [False]*len(nodes)
        for node in nodes:
            assignments[node.assignee.id].append(node)
            if len(node.parents) == 0:
                isopen[node.id] = True
        
        to_delete = [assignee for assignee in assignments if len(assignments[assignee]) == 0]
        for assignee in to_delete:
            del assignments[assignee]

        while(len(assignments) > 0):
            changed = False
            #print(isopen)
            for assignee in assignments:
                
                #print('ids:', [assignments[assignee][i].id for i in range(len(assignments[assignee]))])
                #print('orders:', [assignments[assignee][i].order for i in range(len(assignments[assignee]))])
                
                task = assignments[assignee][0]
                if isopen[task.id]:
                    for child in task.children:
                        opening = 1
                        for parent in child.parents:
                            opening *= isopen[parent.id]
                        isopen[child.id] = (opening == 1)
                    for parent in task.parents:
                        assignees_time[assignee] = max(parent.start + parent.duration, assignees_time[assignee])
                    task.set_start_time(assignees_time[assignee])
                    self.nodes[task.id].set_start_time(assignees_time[assignee])
                    assignees_time[assignee] += task.duration
                    assignments[assignee].pop(0)
                    changed = True
            to_delete = [assignee for assignee in assignments if len(assignments[assignee]) == 0]
            for assignee in to_delete:
                del assignments[assignee]
            if changed == False:
                raise Exception("infinity")
            
    def __str__(self):
        output = ""
        for node in self.nodes:
            output += str(node) + '\n'
        return output
