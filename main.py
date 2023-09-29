from GeneticAlgorithm import GeneticAlgorithm
from datetime import timedelta, datetime

durations = [timedelta(seconds=8), timedelta(seconds=1), timedelta(seconds=1), timedelta(seconds=5)]
children = [None, 2, 3, None]
parents = [None, None, 1, 2]
ga = GeneticAlgorithm([None]*4, durations, children, parents)
print(ga.get_best_solution().fitness_score)