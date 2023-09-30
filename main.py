from genetic_algorithm.runner import run_algorithm
from genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from datetime import timedelta, datetime
from genetic_algorithm.Assignee import Assignee
from genetic_algorithm.Task import Task
from genetic_algorithm.Assignee import Assignee
from datetime import timedelta
from genetic_algorithm.Node import Node

if __name__ == '__main__':
    tasks = [
        Task(None, timedelta(seconds=5), 0, None),
        Task(None, timedelta(seconds=2), 1, None),
        Task(None, timedelta(seconds=3), 2, None),
        Task(None, timedelta(seconds=7), 3, None),
        Task(None, timedelta(seconds=1), 4, None),
        Task(None, timedelta(seconds=10), 5, None),
        Task(None, timedelta(seconds=2), 6, None),
        Task(None, timedelta(seconds=8), 7, None),
        Task(None, timedelta(seconds=3), 8, None),
        Task(None, timedelta(seconds=4), 9, None),
        Task(None, timedelta(seconds=2), 10, None),
        Task(None, timedelta(seconds=2), 11, None),
        Task(None, timedelta(seconds=2), 12, None),
        Task(None, timedelta(seconds=2), 13, None),
        Task(None, timedelta(seconds=2), 14, None),
    ]
    tasks[2].set_depend_on([tasks[1]])
    tasks[3].set_depend_on([tasks[2]])
    tasks[5].set_depend_on([tasks[4]])
    tasks[8].set_depend_on([tasks[7]])
    tasks[9].set_depend_on([tasks[8]])
    tasks[11].set_depend_on([tasks[10]])
    tasks[12].set_depend_on([tasks[11]])
    tasks[13].set_depend_on([tasks[12]])
    tasks[14].set_depend_on([tasks[13]])
    result = run_algorithm(tasks, [Assignee(0, None), Assignee(1, None), Assignee(2, None), Assignee(3, None)])
