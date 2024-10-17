from .base_organism import BaseOrganism
from .plant import Plant
import pygame
from config import GRID_SIZE, CONSUMER_ENERGY_LOSS_RATE

class Consumer(BaseOrganism):
    def __init__(self, environment, position=None, genome=None):
        super().__init__(environment, position, genome)
        self.color = (255, 0, 0)  # 红色
        self.hunger = 0

    def update(self):
        if super().update():
            self.hunt()
            self.energy -= self.energy * CONSUMER_ENERGY_LOSS_RATE
            return True
        return False

    def hunt(self):
        nearby_organisms = self.environment.get_organisms_at(self.position)
        for organism in nearby_organisms:
            if isinstance(organism, Plant) and organism.size > 1:
                energy_gain = organism.energy * self.genome.get_gene('energy_efficiency').value
                self.energy += energy_gain
                organism.size -= 1
                if organism.size <= 1:
                    self.environment.remove_organism(organism)
                break

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (int(self.position[0] * GRID_SIZE), int(self.position[1] * GRID_SIZE)), 
                           int(self.genome.get_gene('size').value * 5))
