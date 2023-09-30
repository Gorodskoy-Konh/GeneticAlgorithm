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
        nodes.append(Node(task.deadline, task.duration, i, child=task.depend_on, parent=task.parent))
    ga = GeneticAlgorithm(nodes, team_memebers)
    best_chromosome = ga.get_best_solution()
    answer = []
    for node in best_chromosome.nodes:
        answer.append(Task(node.deadline, node.duration, node.child, node.id, node.assignee))
    return answer

tasks = [
    Task(None, timedelta(seconds=8), None, 0, None),
    Task(None, timedelta(seconds=1), None, 1, None),
    Task(None, timedelta(seconds=1), None, 2, None),
    Task(None, timedelta(seconds=5), None, 3, None),
]
tasks[2].depend_on = tasks[1]
tasks[3].depend_on = tasks[2]
run_algorithm(tasks, [Assignee(0, None, None), Assignee(1, None, None), Assignee(2, None, None)])