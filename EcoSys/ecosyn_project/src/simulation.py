import numpy as np
import torch
from config import *
from organisms.base_organism import BaseOrganism
from organisms.plant import Plant
from organisms.consumer import Consumer
from organisms.decomposer import Decomposer
from environment.environment import Environment
from PyQt6.QtCore import QObject, pyqtSignal

class Simulation(QObject):
    update_complete = pyqtSignal(dict, dict, dict)

    def __init__(self):
        super().__init__()
        print("Initializing Simulation...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.environment = Environment(GRID_SIZE, GRID_SIZE)
        print("Environment created.")
        self.organisms = []
        self.initialize_organisms()
        print("Organisms initialized.")
        self.time_steps = []
        self.population_history = {Plant: [], Consumer: [], Decomposer: []}
        self.update_count = 0
        print(f"Using device: {self.device}")
        print("Simulation initialization complete.")

    def initialize_organisms(self):
        for _ in range(INITIAL_PRODUCER_COUNT):
            position = torch.rand(2, device=self.device) * torch.tensor([self.environment.width, self.environment.height], device=self.device)
            self.add_organism(Plant(self.environment, position=position))
        for _ in range(INITIAL_CONSUMER_COUNT):
            position = torch.rand(2, device=self.device) * torch.tensor([self.environment.width, self.environment.height], device=self.device)
            self.add_organism(Consumer(self.environment, position=position))
        for _ in range(INITIAL_DECOMPOSER_COUNT):
            position = torch.rand(2, device=self.device) * torch.tensor([self.environment.width, self.environment.height], device=self.device)
            self.add_organism(Decomposer(self.environment, position=position))

    def add_organism(self, organism):
        self.organisms.append(organism)
        self.environment.add_organism(organism)

    def update(self):
        self.update_count += 1
        if self.update_count % 10 == 0:  # 每10次更新才打印
            print(f"Simulation update: {self.update_count}")
        
        self.environment.update(TIME_STEP)
        
        for organism in self.organisms[:]:
            organism.move()  # 确保每个生物体都移动
            if not organism.update(self.environment):
                self.remove_organism(organism)
            else:
                self.organism_behavior(organism)

        self.reproduction()
        self.natural_selection()

        organism_types, species_count, resources = self.get_stats()
        self.update_complete.emit(organism_types, species_count, resources)

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            self.environment.remove_organism(organism)

    def update_organisms_parallel(self, organism_tensors):
        # 这里实现并行的生物体更新逻辑
        # 例如：移动、能量消耗等
        # 使用 PyTorch 操作进行批量计算
        return organism_tensors  # 这里需要实现具体的并行更新逻辑

    def tensor_to_organism(self, tensor):
        # 将张量转换回生物体对象
        # 这里需要实现具体的转换逻辑
        pass

    def draw(self, screen):
        self.environment.draw(screen)
        for organism in self.organisms:
            organism.draw(screen)

    def reset(self):
        self.environment = Environment(GRID_SIZE, GRID_SIZE)
        self.organisms = []
        self.initialize_organisms()
        self.time_steps = []
        self.population_history = {Plant: [], Consumer: [], Decomposer: []}

    def get_stats(self):
        organism_types = {Plant: 0, Consumer: 0, Decomposer: 0}
        species_count = {}
        for organism in self.organisms:
            organism_types[type(organism)] += 1
            if organism.species_id not in species_count:
                species_count[organism.species_id] = 1
            else:
                species_count[organism.species_id] += 1
        
        # 计算平均资源水平
        resources = {
            'Water': np.mean(self.environment.water),
            'Minerals': np.mean(self.environment.minerals),
            'Organic Matter': np.mean(self.environment.organic_matter)
        }
        
        return organism_types, species_count, resources

    def organism_behavior(self, organism):
        organism.move()
        
        if isinstance(organism, Consumer):
            prey = self.find_nearest_prey(organism)
            if prey:
                distance = np.linalg.norm(organism.position - prey.position)
                if distance < organism.genes['size']:
                    organism.eat(prey)
                    if prey.energy <= 0:
                        self.remove_organism(prey)

        elif isinstance(organism, Plant):
            resources = self.environment.get_resources_at(organism.position)
            consumed = min(resources, organism.genes['size'] * 0.1)
            organism.energy += consumed
            self.environment.consume_resources(organism.position, consumed)

    def find_nearest_prey(self, predator):
        min_distance = float('inf')
        nearest_prey = None
        for organism in self.organisms:
            if isinstance(organism, Plant) and isinstance(predator, Consumer):
                distance = np.linalg.norm(predator.position - organism.position)
                if distance < min_distance:
                    min_distance = distance
                    nearest_prey = organism
        return nearest_prey

    def reproduction(self):
        new_organisms = []
        for organism in self.organisms:
            if np.random.random() < REPRODUCTION_RATE:
                offspring = organism.reproduce()
                if offspring:
                    new_organisms.append(offspring)
                    # 添加突变
                    if np.random.random() < MUTATION_RATE:
                        offspring.mutate()
        for new_org in new_organisms:
            self.add_organism(new_org)

    def natural_selection(self):
        if len(self.organisms) > MAX_POPULATION:
            # 保留一定比例的生物，而不是固定数量
            survival_rate = MAX_POPULATION / len(self.organisms)
            survivors = [org for org in self.organisms if np.random.random() < survival_rate]
            for organism in self.organisms:
                if organism not in survivors:
                    self.remove_organism(organism)
            self.organisms = survivors
