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
            self.nodes.append(Node(deadlines[i], durations[i], i, assignees[assignee_random_idx], order=i*len(deadlines)))
        for i in range(len(deadlines)):
            if children[i] is not None:
                self.nodes[i].child = self.nodes[children[i]]
            if parents[i] is not None:
                self.nodes[i].parent = self.nodes[parents[i]]    
                
    def fitness(self):
        full_duration = timedelta(seconds=0)
        
        self.nodes.sort(key=lambda x: x.order)
        isopen = [False]*len(self.nodes)
        assignments = {assignee.id:[] for assignee in self.assignees}
        
        for node in self.nodes:
            assignments[node.assignee.id].append(node)
            if node.parent is None:
                isopen[node.id] = True
        for assignee in list(assignments.keys()):
            if len(assignments[assignee]) == 0:
                del assignments[assignee]
        # print(assignments)

        while len(assignments) > 0:
            # print('\n')
            min_assignee = -1
            min_time = timedelta(days=1e3)
            # print(isopen)
            for assignee in assignments:
                # print(assignee, 'value =', assignments[assignee])
                # print('ids:', [assignments[assignee][i].id for i in range(len(assignments[assignee]))])
                # print('children:', [assignments[assignee][i].child.id if assignments[assignee][i].child is not None else None for i in range(len(assignments[assignee]))])
                # print('orders:', [assignments[assignee][i].order for i in range(len(assignments[assignee]))])
                
                task = assignments[assignee][0]
                if isopen[task.id] and task.duration < min_time:
                    min_assignee = assignee
            for assignee in assignments:
                task = assignments[assignee][0]
                if isopen[task.id]:
                    task.duration -= min_time
            #print(assignments[min_assignee][0].id)
            min_task = assignments[min_assignee][0]
            # print(f"Zalupa: {min_task.child}, id: {min_task.id}")
            if not min_task.child is None:
                isopen[min_task.child.id] = True
            
            assignments[min_assignee].pop(0)
            if len(assignments[min_assignee]) == 0:
                del assignments[min_assignee]
            
            full_duration += min_time
        
        self.fitness_score = full_duration
        return full_duration


    def mutate(self, assignees, mut_num: int=1):
        mutated_chromosome = Chromosome(self.deadlines, self.durations, self.children, self.parents, self.assignees)
        for i in range(mut_num):
            node_ind = int(random.random() * len(self.nodes))
            assignee_ind = int(random.random() * len(assignees))
            mutated_chromosome.nodes[node_ind].assignee = assignees[assignee_ind]
            mutated_chromosome.nodes[node_ind].order = random.random() * ORDER_LIMIT
        mutated_chromosome.__correct_order()
        return mutated_chromosome

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
        assignments = {assignee.id:[] for assignee in self.assignees}
        # node2assignee = {node.id:node}
        for node in self.nodes:
            assignments[node.assignee.id].append(node)
        
        for a in assignments:
            for i in range(len(assignments[a])):
                for j in range(len(assignments[a])):
                    if assignments[a][i].child is not None and assignments[a][i].child.id == assignments[a][j].id:
                        assignments[a][i].order = assignments[a][j].order - 1
        
        used = [False]*len(self.nodes)
        iter_range = list(range(len(self.nodes)))
        random.shuffle(iter_range)
        for i in iter_range:
            if not used[i] and self.nodes[i].parent == None:
                self.__dfs(self.nodes[i].id, used, i*len(self.nodes), assignments)
        
    def __dfs(self, v, used, order, assignments):
        used[v] = True
        self.nodes[v].order = order
        if self.nodes[v].child is None:
            return
        # self.nodes[v].order = order

        if not used[self.nodes[v].child.id]:
            self.__dfs(self.nodes[v].child.id, used, order + 1, assignments)

        for t in assignments[self.nodes[v].assignee.id]:
            if not used[t.id]:
                order += 1
                self.__dfs(t.id, used, order, assignments)