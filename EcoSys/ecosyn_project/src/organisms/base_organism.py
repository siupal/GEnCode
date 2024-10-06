import numpy as np
import random
from ..genetics.gene_structure import mutate_genes

class Organism:
    def __init__(self, species, location, genes):
        self.species = species
        self.location = location
        self.genes = genes
        self.energy = 100  # 初始能量
        self.age = 0
        self.lifespan = self.calculate_lifespan()
        self.alive = True

    def calculate_lifespan(self):
        return int(random.normalvariate(100, 20) * self.genes['longevity'])

    def perceive(self, environment):
        perception_range = int(self.genes['perception_range'] * 5)
        return environment.get_surroundings(self.location, perception_range)

    def decide(self, surroundings):
        # 基础决策逻辑，可被子类重写
        return 'move'

    def act(self, action, environment):
        if action == 'move':
            self.move(environment)

    def move(self, environment):
        new_location = environment.get_nearby_empty_location(self.location)
        if new_location:
            environment.move_organism(self, new_location)
            self.energy -= self.genes['movement_cost']

    def update(self, environment):
        self.age += 1
        self.energy -= self.genes['metabolism_rate']
        if self.energy <= 0 or self.age >= self.lifespan:
            self.alive = False
        return self.alive

    def reproduce(self, mate=None):
        if mate and self.genes['reproductive_strategy'] == 'sexual':
            return self.reproduce_sexually(mate)
        else:
            return self.reproduce_asexually()

    def reproduce_asexually(self):
        offspring = self.__class__(self.species, self.location, self.genes.copy())
        offspring.mutate()
        return offspring

    def reproduce_sexually(self, mate):
        offspring_genes = {}
        for gene in self.genes:
            offspring_genes[gene] = random.choice([self.genes[gene], mate.genes[gene]])
        offspring = self.__class__(self.species, self.location, offspring_genes)
        offspring.mutate()
        return offspring

    def mutate(self):
        self.genes = mutate_genes(self.genes)

    def calculate_fitness(self, environment):
        fitness = 1.0
        temperature_diff = abs(environment.temperature - self.genes['optimal_temperature'])
        fitness -= temperature_diff * 0.01  # TEMPERATURE_PENALTY
        fitness += self.genes['foraging_efficiency'] * 0.1  # FORAGING_BONUS
        fitness -= self.genes['metabolism_rate'] * 0.05  # METABOLISM_COST
        return max(0, fitness)