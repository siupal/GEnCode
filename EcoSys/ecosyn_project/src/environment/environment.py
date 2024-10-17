from config import *
import numpy as np
import torch
import noise
import random
from scipy.ndimage import gaussian_filter

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.temperature = torch.full((height, width), INITIAL_TEMPERATURE, dtype=torch.float32, device=self.device)
        self.humidity = torch.full((height, width), INITIAL_HUMIDITY, dtype=torch.float32, device=self.device)
        self.light_intensity = torch.full((height, width), INITIAL_LIGHT_INTENSITY, dtype=torch.float32, device=self.device)
        self.soil_fertility = torch.full((height, width), INITIAL_SOIL_FERTILITY, dtype=torch.float32, device=self.device)
        
        self.organisms = []
        self.terrain = torch.tensor(self.generate_terrain(), device=self.device)
        self.rivers = torch.tensor(self.generate_rivers(), device=self.device)
        self.water = torch.tensor(self.generate_resource_map(), device=self.device)
        self.minerals = torch.tensor(self.generate_resource_map(), device=self.device)
        self.organic_matter = torch.tensor(self.generate_resource_map(), device=self.device)
        self.current_season = 0  # 0: Spring, 1: Summer, 2: Autumn, 3: Winter
        self.day = 0
        self.year = 0

    def generate_terrain(self):
        print("Starting terrain generation...")
        scale = 0.03  # 进一步减小scale值，使地形变化更加平缓
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        terrain = np.zeros((self.height, self.width))

        for y in range(self.height):
            for x in range(self.width):
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
                terrain[y, x] = (elevation + 1) * 50  # 将噪声值映射到0-100范围

        # 使用高斯滤波平滑地形
        terrain = gaussian_filter(terrain, sigma=3)  # 增加sigma值，使地形更加平滑

        print("Terrain generation complete.")
        return terrain

    def generate_rivers(self):
        print("Starting river generation...")
        rivers = np.zeros((self.height, self.width), dtype=bool)
        num_rivers = int(min(self.width, self.height) / 20)  # 减少河流数量
        max_steps = max(self.width, self.height)  # 限制最大步数
        
        for _ in range(num_rivers):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            steps = 0
            while self.terrain[y, x] > 20 and steps < max_steps:  # 从高处开始，但限制步数
                rivers[y, x] = True
                # 找到最低的相邻点
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < self.width and 0 <= ny < self.height]
                if not valid_neighbors:
                    break
                x, y = min(valid_neighbors, key=lambda pos: self.terrain[pos[1], pos[0]])
                steps += 1
            
            if steps % 100 == 0:
                print(f"Generated {steps} steps for a river")
        
        print("River generation complete.")
        return rivers

    def generate_resource_map(self):
        return np.random.rand(self.height, self.width) * INITIAL_RESOURCE_AMOUNT

    def update(self, time_step):
        self.day += time_step
        if self.day >= 365:
            self.day = 0
            self.year += 1
            self.current_season = (self.current_season + 1) % 4

        self.update_environmental_factors()
        self.update_resources()
        self.handle_natural_disasters()

    def update_environmental_factors(self):
        noise = torch.randn_like(self.temperature, device=self.device)
        
        season_factor = torch.sin(2 * np.pi * (self.day / 365 + self.current_season / 4))
        
        self.temperature += noise * ENVIRONMENTAL_CHANGE_RATE + season_factor * 10
        self.humidity = torch.clamp(self.humidity + noise * ENVIRONMENTAL_CHANGE_RATE + season_factor * 20, 0, 100)
        self.light_intensity = torch.clamp(self.light_intensity + noise * ENVIRONMENTAL_CHANGE_RATE + season_factor * 40, 0, 200)
        self.soil_fertility = torch.clamp(self.soil_fertility + noise * ENVIRONMENTAL_CHANGE_RATE, 0, 10)

        # 添加更强烈的环境变化对生物的影响
        for organism in self.organisms:
            climate = self.get_climate_at(organism.position)
            if climate['temperature'] > 35 or climate['temperature'] < 5:
                organism.energy -= 5  # 增加极端温度造成的能量损失
            if climate['humidity'] < 20:
                organism.energy -= 3  # 增加干旱造成的能量损失
            if isinstance(organism, Plant) and climate['light_intensity'] > 150:
                organism.energy += 3  # 增加强光使植物获得的额外能量

    def update_resources(self):
        # 资源再生
        self.water += torch.rand(self.height, self.width, device=self.device) * WATER_REGEN_RATE
        self.minerals += torch.rand(self.height, self.width, device=self.device) * MINERAL_REGEN_RATE
        self.organic_matter += torch.rand(self.height, self.width, device=self.device) * ORGANIC_MATTER_REGEN_RATE

        # 确保资源不超过最大值
        self.water = torch.clamp(self.water, 0, MAX_RESOURCE_AMOUNT)
        self.minerals = torch.clamp(self.minerals, 0, MAX_RESOURCE_AMOUNT)
        self.organic_matter = torch.clamp(self.organic_matter, 0, MAX_RESOURCE_AMOUNT)

    def handle_natural_disasters(self):
        if random.random() < DISASTER_PROBABILITY:
            disaster_type = random.choice(['drought', 'flood', 'wildfire'])
            affected_area = np.random.rand(self.height, self.width) < DISASTER_AREA
            
            if disaster_type == 'drought':
                self.humidity[affected_area] *= 0.5
                self.water[affected_area] *= 0.7
            elif disaster_type == 'flood':
                self.humidity[affected_area] = 100
                self.water[affected_area] *= 1.5
            elif disaster_type == 'wildfire':
                self.organic_matter[affected_area] *= 0.1
                for organism in self.organisms[:]:
                    if affected_area[int(organism.position[1])][int(organism.position[0])]:
                        self.remove_organism(organism)

    def consume_resource(self, resource_type, amount, position):
        x, y = int(position[0]), int(position[1])
        if resource_type == 'water':
            consumed = min(self.water[y, x].item(), amount)
            self.water[y, x] -= consumed
        elif resource_type == 'minerals':
            consumed = min(self.minerals[y, x].item(), amount)
            self.minerals[y, x] -= consumed
        elif resource_type == 'organic_matter':
            consumed = min(self.organic_matter[y, x].item(), amount)
            self.organic_matter[y, x] -= consumed
        else:
            consumed = 0
        return consumed

    def add_organism(self, organism):
        self.organisms.append(organism)

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            self.add_organic_matter(organism.position, organism.energy)

    def add_organic_matter(self, position, amount):
        x, y = int(position[0]), int(position[1])
        self.organic_matter[y, x] += amount * DECOMPOSITION_RATE

    def get_climate_at(self, position):
        x, y = int(position[0]), int(position[1])
        return {
            'temperature': self.temperature[y, x].item(),
            'humidity': self.humidity[y, x].item(),
            'light_intensity': self.light_intensity[y, x].item(),
            'soil_fertility': self.soil_fertility[y, x].item()
        }

    def get_resources_at(self, position):
        x, y = int(position[0]), int(position[1])
        return {
            'water': self.water[y, x],
            'minerals': self.minerals[y, x],
            'organic_matter': self.organic_matter[y, x]
        }
