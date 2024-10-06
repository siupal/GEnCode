from .organism import Organism

class Producer(Organism):
    def __init__(self, genes, location):
        super().__init__(genes, location)
        self.photosynthesis_efficiency = genes['photosynthesis_efficiency']

    def eat(self, environment):
        cell = environment.grid[self.position[0]][self.position[1]]
        if cell.resource_availability['water'] > 0:
            energy_gain = self.photosynthesis_efficiency * cell.light_intensity / 100
            self.energy += energy_gain
            cell.resource_availability['water'] -= 0.1 * energy_gain