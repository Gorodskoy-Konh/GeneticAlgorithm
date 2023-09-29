from Assignee import Assignee
from Node import Node

class Chromosome:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes.copy()
    
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
        
        return full_duration


    def mutate(self):
        pass

    def crossover(self, chromosome):
        pass