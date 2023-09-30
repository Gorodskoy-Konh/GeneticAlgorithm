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
        nodes = []
        for node in self.nodes:
            nodes.append(node.copy())
            full_stack_difference += node.stack_difference()
        nodes.sort(key=lambda x: x.order)
        isopen = [False]*len(nodes)
        assignments = {assignee.id:[] for assignee in self.assignees}
        
        for node in nodes:
            assignments[node.assignee.id].append(node)
            if len(node.parents) == 0:
                isopen[node.id] = True
        for assignee in list(assignments.keys()):
            if len(assignments[assignee]) == 0:
                del assignments[assignee]
        #print(assignments)

        while len(assignments) > 0:
            #print('\n')
            min_assignee = -1
            min_time = timedelta(days=1e3)
            #print(isopen)
            for assignee in assignments:
                # print(assignee, 'value =', assignments[assignee])
                # print('ids:', [assignments[assignee][i].id for i in range(len(assignments[assignee]))])
                # print('children:', [assignments[assignee][i].child.id if assignments[assignee][i].child is not None else None for i in range(len(assignments[assignee]))])
                # print('orders:', [assignments[assignee][i].order for i in range(len(assignments[assignee]))])
                
                task = assignments[assignee][0]
                if isopen[task.id] and task.duration < min_time:
                    min_assignee = assignee
                    min_time = task.duration
            if min_assignee == -1:
                self.fitness_score = timedelta(days=1e3).total_seconds()
                return self.fitness_score

            for assignee in assignments:
                task = assignments[assignee][0]
                if isopen[task.id]:
                    task.duration -= min_time
            #print(assignments[min_assignee][0].id)
            min_task = assignments[min_assignee][0]
            #if not min_task.child is None:
                #print(f"Zalupa: {min_task.child}, id: {min_task.id}")
            for child in min_task.children:
                isopen[child.id] = True
            
            assignments[min_assignee].pop(0)
            if len(assignments[min_assignee]) == 0:
                del assignments[min_assignee]
            
            full_duration += min_time
        
        self.fitness_score = full_duration.total_seconds() + full_stack_difference/max(self.maximum_stack_difference, 1)
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

    def __correct_order(self):
        assignments = {assignee.id:[] for assignee in self.assignees}
        for node in self.nodes:
            assignments[node.assignee.id].append(node)
                
        used = [False]*len(self.nodes)
        iter_range = list(range(len(self.nodes)))
        random.shuffle(iter_range)
        for i in iter_range:
            if not used[i] and self.nodes[i].parent == None:
                self.__dfs(self.nodes[i].id, used, i*len(self.nodes), assignments)
        
    def __dfs(self, v, used, order, assignments):
        used[v] = True
        self.nodes[v].order = order
        
        for t in assignments[self.nodes[v].assignee.id]:
            if not used[t.id]:
                order += 1
                self.__dfs(t.id, used, order, assignments)

    def copy(self):
        nodes = []
        for node in self.nodes:
            nodes.append(node.copy())
        return Chromosome(nodes, self.assignees, self.maximum_stack_difference)

    def __str__(self):
        output = ""
        for node in self.nodes:
            output += str(node) + '\n'
        return output
