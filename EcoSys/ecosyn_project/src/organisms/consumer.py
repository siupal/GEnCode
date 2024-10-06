from .base_organism import Organism
import random

class Consumer(Organism):
    def __init__(self, location, genes):
        super().__init__('Consumer', location, genes)
        self.hunting_efficiency = genes['hunting_efficiency']

    def act(self, action, environment):
        if action == 'hunt':
            prey = self.find_prey(environment)
            if prey:
                self.hunt(prey, environment)
        elif action == 'move':
            self.move(environment)

    def find_prey(self, environment):
        surroundings = self.perceive(environment)
        prey = [org for org in surroundings if org.species == 'Producer' or org.species == 'Consumer']
        return random.choice(prey) if prey else None

    def hunt(self, prey, environment):
        if random.random() < self.hunting_efficiency:
            self.energy += prey.energy * 0.5
            environment.remove_organism(prey)

    def move(self, environment):
        new_location = environment.get_nearby_empty_location(self.location)
        if new_location:
            environment.move_organism(self, new_location)
            self.energy -= self.genes['movement_cost']

    def reproduce(self, environment):
        if self.energy > 200 and random.random() < self.genes['reproduction_rate']:
            new_location = environment.get_nearby_empty_location(self.location)
            if new_location:
                new_genes = mutate_genes(self.genes)
                new_consumer = Consumer(new_location, new_genes)
                environment.add_organism(new_consumer)
                self.energy -= 100  # 繁殖消耗能量