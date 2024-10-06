import numpy as np
import noise
from .environment_cell import EnvironmentCell
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_terrain()
        self.organisms = []
        self.time = 0
        self.climate_zones = self.generate_climate_zones()
        self.temperature = self.generate_temperature()

    def generate_terrain(self):
        scale = 0.1
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        terrain = [[EnvironmentCell((x, y)) for y in range(self.height)] for x in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                elevation = noise.pnoise2(nx * scale,
                                          ny * scale,
                                          octaves=octaves,
                                          persistence=persistence,
                                          lacunarity=lacunarity,
                                          repeatx=1024,
                                          repeaty=1024,
                                          base=0)

                terrain[x][y].altitude = (elevation + 1) * 50  # 将噪声值映射到0-100范围

        return terrain

    def generate_climate_zones(self):
        zones = np.zeros((self.height, self.width), dtype=int)
        for y in range(self.height):
            if y < self.height // 3:
                zones[y] = 0  # 热带
            elif y < 2 * self.height // 3:
                zones[y] = 1  # 温带
            else:
                zones[y] = 2  # 寒带
        return zones

    def generate_temperature(self):
        return np.random.normal(20, 5)

    def update(self, time_step):
        self.time += time_step
        self.update_temperature()
        
        for row in self.grid:
            for cell in row:
                cell.update_environment(time_step)

        for organism in self.organisms[:]:
            if organism.update(self):
                action = organism.decide(organism.perceive(self))
                organism.act(action, self)
                if organism.energy > organism.genes['reproduction_threshold']:
                    offspring = organism.reproduce(self)
                    if offspring:
                        self.add_organism(offspring)
            else:
                self.remove_organism(organism)

    def update_temperature(self):
        # 简单的温度变化模拟，可以根据需要进行更复杂的计算
        self.temperature += np.random.normal(0, 0.1)

    def get_temperature(self, location):
        x, y = location
        return self.temperature + self.climate_zones[y, x] * 5  # 简单的温度梯度

    def add_organic_matter(self, position, amount):
        x, y = position
        self.grid[x][y].resource_availability['organic_matter'] += amount

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            self.add_organic_matter(organism.position, organism.energy)

    def add_organism(self, organism):
        self.organisms.append(organism)

    def get_surroundings(self, location, range):
        x, y = location
        surroundings = []
        for dx in range(-range, range+1):
            for dy in range(-range, range+1):
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                surroundings.append(self.grid[ny][nx])
        return surroundings

    def add_organism(self, organism):
        x, y = organism.location
        self.grid[y][x].add_organism(organism)

    def remove_organism(self, organism):
        x, y = organism.location
        self.grid[y][x].remove_organism()

    def get_stats(self):
        # 统计环境中的各种数据
        pass