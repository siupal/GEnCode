from .base_organism import BaseOrganism
from config import *
import numpy as np

class Plant(BaseOrganism):
    def __init__(self, environment, position=None, genes=None):
        super().__init__(environment, position, genes)
        self.color = (0, 255, 0)  # 绿色
        self.size = PLANT_INITIAL_SIZE
        
        # 如果需要添加植物特有的基因
        if self.genes is None:
            self.genes = self.initialize_genes()
        self.genes.update({
            'photosynthesis_efficiency': np.random.normal(1.0, 0.1),
            # 其他植物特有的基因...
        })

    def update(self, environment):
        if super().update(environment):
            self.photosynthesize(environment)
            self.grow()
            return True
        return False

    def photosynthesize(self, environment):
        light = environment.light_intensity[int(self.position[1])][int(self.position[0])]
        soil_fertility = environment.soil_fertility[int(self.position[1])][int(self.position[0])]
        water = environment.consume_resource('water', self.genes['water_consumption'], self.position)
        minerals = environment.consume_resource('minerals', self.genes['mineral_consumption'], self.position)
        
        energy_gain = (light * soil_fertility * water * minerals) * self.genes['energy_efficiency'] * PHOTOSYNTHESIS_RATE
        self.energy += energy_gain

    def grow(self):
        self.size = min(self.size + PLANT_GROWTH_RATE, self.genes.get_gene('size').value * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (int(self.position[0] * GRID_SIZE), int(self.position[1] * GRID_SIZE)), 
                           int(self.size * 3))
