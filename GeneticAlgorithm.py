from Chromosome import Chromosome
from datetime import datetime, timedelta
import random

class GeneticAlgorithm():
    def __init__(self,deadlines: list[datetime], durations: list[timedelta], children: list[int], parents: list[int],  
                 iterations: int=100, generation_size: int=100, mutation_chance: float=0.2, crossover_chance:float=0.2) -> None:
        self.generation_size = generation_size
        self.generation = self.__init_generation(deadlines, durations, children, parents)
        for i in range(iterations):
            self.evolve(mutation_chance, crossover_chance)
    
    def __init_generation(self, deadlines: list[datetime], durations: list[timedelta], children: list[int], parents: list[int]):
        generation = []
        for i in range(self.generation_size):
            generation.append(Chromosome(deadlines=deadlines, durations=durations, children=children, parents=parents))
        return generation

    def evolve(self, mutation_chance, crossover_chance):
        for i in range(self.generation_size):
            if random.random() > 1 - mutation_chance:
                self.generation.append(self.generation[i].mutate())
            if random.random() > 1 - crossover_chance:
                ind = int(random.random() * len(self.generation))
                self.generation.append(self.generation[i].crossover(self.generation[ind]))
        for i in range(self.generation_size, len(self.nodes)):
            self.generation[i].fitness()
        self.generation.sort(key=lambda x: -x.fitness_score)
        self.generation = self.generation[:self.generation_size]
    
    def get_best_solution(self):
        return self.generation[0]