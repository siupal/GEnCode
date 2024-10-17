from .base_organism import BaseOrganism
import pygame
from config import GRID_SIZE, DECOMPOSER_ENERGY_GAIN_RATE

class Decomposer(BaseOrganism):
    def __init__(self, environment, position=None, genome=None):
        super().__init__(environment, position, genome)
        self.color = (128, 128, 128)  # 灰色

    def update(self):
        if super().update():
            self.decompose()
            return True
        return False

    def decompose(self):
        organic_matter = self.environment.soil_fertility[int(self.position[1])][int(self.position[0])]
        energy_gain = organic_matter * self.genome.get_gene('energy_efficiency').value * DECOMPOSER_ENERGY_GAIN_RATE
        self.energy += energy_gain
        self.environment.soil_fertility[int(self.position[1])][int(self.position[0])] -= energy_gain * 0.1
        self.environment.soil_fertility[int(self.position[1])][int(self.position[0])] = max(0, self.environment.soil_fertility[int(self.position[1])][int(self.position[0])])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (int(self.position[0] * GRID_SIZE), int(self.position[1] * GRID_SIZE)), 
                           int(self.genome.get_gene('size').value * 4))
