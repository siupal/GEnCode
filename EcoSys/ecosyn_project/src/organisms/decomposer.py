from .base_organism import Organism
import random

class Decomposer(Organism):
    def __init__(self, location, genes):
        super().__init__('Decomposer', location, genes)
        self.decomposition_efficiency = genes['decomposition_efficiency']

    def act(self, action, environment):
        if action == 'decompose':
            self.decompose(environment)
        elif action == 'move':
            self.move(environment)

    def decompose(self, environment):
        cell = environment.grid[self.location[1]][self.location[0]]
        decomposed_matter = cell.organic_matter * self.decomposition_efficiency
        self.energy += decomposed_matter
        cell.organic_matter -= decomposed_matter
        cell.nutrients += decomposed_matter * 0.5  # 一半的分解物质转化为养分

    def move(self, environment):
        new_location = environment.get_nearby_empty_location(self.location)
        if new_location:
            environment.move_organism(self, new_location)
            self.energy -= self.genes['movement_cost']

    def reproduce(self, environment):
        if self.energy > 150 and random.random() < self.genes['reproduction_rate']:
            new_location = environment.get_nearby_empty_location(self.location)
            if new_location:
                new_genes = mutate_genes(self.genes)
                new_decomposer = Decomposer(new_location, new_genes)
                environment.add_organism(new_decomposer)
                self.energy -= 75  # 繁殖消耗能量