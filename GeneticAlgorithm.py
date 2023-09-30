from Chromosome import Chromosome
from datetime import datetime, timedelta
import random
from Assignee import Assignee
from Node import Node

class GeneticAlgorithm():
    def __init__(self, nodes: list[Node], assignees: list[Assignee], iterations: int=100, generation_size: int=100, mutation_chance: float=0.2, crossover_chance:float=0.2) -> None:
        self.generation_size = generation_size
        self.assignees = assignees
        self.nodes = nodes
        self.generation = self.__init_generation()
        for i in range(iterations):
            self.evolve(mutation_chance, crossover_chance, assignees)
    
    def __init_generation(self):
        generation = []
        for i in range(self.generation_size):
            generation.append(Chromosome(self.nodes, self.assignees))
            generation[i].fitness()
        return generation

    def evolve(self, mutation_chance, crossover_chance, assignees):
        for i in range(self.generation_size):
            if random.random() > 1 - mutation_chance:
                self.generation.append(self.generation[i].mutate(assignees))
            if random.random() > 1 - crossover_chance:
                ind = int(random.random() * len(self.generation))
                self.generation.append(self.generation[i].crossover(self.generation[ind]))
        for i in range(self.generation_size, len(self.generation)):
            self.generation[i].fitness()
        self.generation.sort(key=lambda x: x.fitness_score)
        self.generation = self.generation[:self.generation_size]
        #print(f'Best fitness for epoch: {self.get_best_solution().fitness_score}')
        #print(str(self.get_best_solution()))
    
    def get_best_solution(self):
        return self.generation[0]