from GeneticAlgorithm import GeneticAlgorithm
from datetime import timedelta, datetime
from Assignee import Assignee
from Task import Task
from Assignee import Assignee

durations = [timedelta(seconds=8), timedelta(seconds=1), timedelta(seconds=1), timedelta(seconds=5)]
children = [None, 2, 3, None]
parents = [None, None, 1, 2]
assignees = [Assignee(0), Assignee(1), Assignee(2)]
ga = GeneticAlgorithm([None]*4, durations, children, parents, assignees)
print(ga.get_best_solution().fitness_score)


def run_algorithm(tasks: list[Task], team_memebers: list[Assignee]) -> list[Task]:
    return []