from .GeneticAlgorithm import GeneticAlgorithm
from datetime import timedelta, datetime
from .Assignee import Assignee
from .Task import Task
from .Assignee import Assignee
from datetime import timedelta
from .Node import Node

def run_algorithm(tasks: list[Task], team_memebers: list[Assignee], start_sprint: datetime, end_sprint: datetime) -> list[Task]:
    for i, assignee in enumerate(team_memebers):
        assignee.set_id(i)
    nodes = []
    for i, task in enumerate(tasks):
        nodes.append(Node(task.deadline, task.duration, i, -1, project=task.project))
        task.set_id(i)
    for i, node in enumerate(nodes):
        node.children = [nodes[j.id] for j in tasks[i].parents]
        node.parents = [nodes[j.id] for j in tasks[i].depend_on]
    ga = GeneticAlgorithm(nodes, team_memebers, iterations=1000, mutation_chance=0.85, crossover_chance=0.85)
    best_chromosome = ga.get_best_solution()
    print(best_chromosome.fitness_score)
    best_chromosome.calcate_start_times()
    new_tasks = []
    
    sprint_duration = end_sprint - start_sprint
    
    for node in best_chromosome.nodes:
        tasks[node.id].write_answer(node.assignee, node.start)
        if tasks[node.id].duration + tasks[node.id].start <= sprint_duration:
            new_tasks.append(tasks[node.id])
    print(str(best_chromosome))
    return new_tasks

# if __name__ == '__main__':
#     tasks = [
#         Task(None, timedelta(seconds=5), 0, None),
#         Task(None, timedelta(seconds=2), 1, None),
#         Task(None, timedelta(seconds=3), 2, None),
#         Task(None, timedelta(seconds=7), 3, None),
#         Task(None, timedelta(seconds=1), 4, None),
#         Task(None, timedelta(seconds=10), 5, None),
#         Task(None, timedelta(seconds=2), 6, None),
#         Task(None, timedelta(seconds=8), 7, None),
#         Task(None, timedelta(seconds=3), 8, None),
#         Task(None, timedelta(seconds=4), 9, None),
#         Task(None, timedelta(seconds=2), 10, None),
#         Task(None, timedelta(seconds=2), 11, None),
#         Task(None, timedelta(seconds=2), 12, None),
#         Task(None, timedelta(seconds=2), 13, None),
#         Task(None, timedelta(seconds=2), 14, None),
#     ]
#     tasks[2].set_depend_on([tasks[1]])
#     tasks[3].set_depend_on([tasks[2]])
#     tasks[5].set_depend_on([tasks[4]])
#     tasks[8].set_depend_on([tasks[7]])
#     tasks[9].set_depend_on([tasks[8]])
#     tasks[11].set_depend_on([tasks[10]])
#     tasks[12].set_depend_on([tasks[11]])
#     tasks[13].set_depend_on([tasks[12]])
#     tasks[14].set_depend_on([tasks[13]])
#     run_algorithm(tasks, [Assignee(0, None), Assignee(1, None), Assignee(2, None), Assignee(3, None)])
