from GeneticAlgorithm import GeneticAlgorithm
from datetime import timedelta, datetime
from Assignee import Assignee
from Task import Task
from Assignee import Assignee
from datetime import datetime, timedelta
from Node import Node

def run_algorithm(tasks: list[Task], team_memebers: list[Assignee]) -> list[Task]:
    nodes = []
    for i, task in enumerate(tasks):
        nodes.append(Node(task.deadline, task.duration, i, -1))
    for i, node in enumerate(nodes):
        if not tasks[i].parent is None:
            node.child = nodes[tasks[i].parent.id]
        if not tasks[i].depend_on is None:
            node.parent = nodes[tasks[i].depend_on.id]
    ga = GeneticAlgorithm(nodes, team_memebers, iterations=10000, mutation_chance=0.85, crossover_chance=0.85)
    best_chromosome = ga.get_best_solution()
    print(best_chromosome.fitness_score)
    print(str(best_chromosome))
    answer = []
    for node in best_chromosome.nodes:
        answer.append(Task(node.deadline, node.duration, node.child, node.id, node.assignee))
    return answer

tasks = [
    Task(None, timedelta(seconds=5), None, 0, None),
    Task(None, timedelta(seconds=2), None, 1, None),
    Task(None, timedelta(seconds=3), None, 2, None),
    Task(None, timedelta(seconds=7), None, 3, None),
    Task(None, timedelta(seconds=1), None, 4, None),
    Task(None, timedelta(seconds=10), None, 5, None),
    Task(None, timedelta(seconds=2), None, 6, None),
    Task(None, timedelta(seconds=8), None, 7, None),
    Task(None, timedelta(seconds=3), None, 8, None),
    Task(None, timedelta(seconds=4), None, 9, None),
    Task(None, timedelta(seconds=2), None, 10, None),
    Task(None, timedelta(seconds=2), None, 11, None),
    Task(None, timedelta(seconds=2), None, 12, None),
    Task(None, timedelta(seconds=2), None, 13, None),
    Task(None, timedelta(seconds=2), None, 14, None),
]
tasks[2].set_depend_on(tasks[1])
tasks[3].set_depend_on(tasks[2])
tasks[5].set_depend_on(tasks[4])
tasks[8].set_depend_on(tasks[7])
tasks[9].set_depend_on(tasks[8])
tasks[11].set_depend_on(tasks[10])
tasks[12].set_depend_on(tasks[11])
tasks[13].set_depend_on(tasks[12])
tasks[14].set_depend_on(tasks[13])
run_algorithm(tasks, [Assignee(0, None, None), Assignee(1, None, None), Assignee(2, None, None), Assignee(3, None, None)])