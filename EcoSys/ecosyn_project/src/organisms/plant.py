from .base_organism import Organism
import random

class Plant(Organism):
    def __init__(self, location, genes):
        super().__init__('Plant', location, genes)
        self.photosynthesis_efficiency = genes['photosynthesis_efficiency']

    def act(self, action, environment):
        self.photosynthesize(environment)

    def photosynthesize(self, environment):
        light = environment.get_light(self.location)
        energy_produced = light * self.photosynthesis_efficiency
        self.energy += energy_produced
        environment.add_resources(self.location, energy_produced * 0.1)

    def decide(self, surroundings):
        # 植物不移动，只进行光合作用
        return 'photosynthesize'

    def reproduce(self, environment):
        if self.energy > 150 and random.random() < self.genes['reproduction_rate']:
            return super().reproduce()
        return None