import torch
import numpy as np
from config import *

class BaseOrganism:
    species_counter = 0

    def __init__(self, environment, position=None, genes=None, species_id=None):
        self.environment = environment
        self.device = environment.device
        if position is None:
            self.position = torch.tensor([np.random.randint(0, environment.width),
                                          np.random.randint(0, environment.height)], device=self.device)
        else:
            self.position = torch.tensor(position, device=self.device)
        self.energy = INITIAL_ENERGY
        self.age = 0
        self.genes = genes if genes is not None else self.initialize_genes()
        if species_id is None:
            BaseOrganism.species_counter += 1
            self.species_id = BaseOrganism.species_counter
        else:
            self.species_id = species_id

    def initialize_genes(self):
        return {
            'size': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
            'speed': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
            'metabolism': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
            'reproduction_threshold': torch.normal(torch.tensor([float(REPRODUCTION_THRESHOLD)], device=self.device), 
                                                   torch.tensor([float(REPRODUCTION_THRESHOLD) * 0.1], device=self.device)).item(),
            'mutation_rate': (torch.rand(1, device=self.device) * 0.09 + 0.01).item(),
            'species_identifier': torch.rand(10, device=self.device),
            'water_consumption': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
            'mineral_consumption': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
            'organic_matter_consumption': torch.normal(torch.tensor([1.0], device=self.device), torch.tensor([0.1], device=self.device)).item(),
        }

    def update(self, environment):
        self.age += 1
        self.energy -= self.genes['metabolism'] * 1.5  # 增加能量消耗
        
        # 消耗资源
        water_consumed = environment.consume_resource('water', self.genes['water_consumption'] * 1.2, self.position)
        minerals_consumed = environment.consume_resource('minerals', self.genes['mineral_consumption'] * 1.2, self.position)
        organic_matter_consumed = environment.consume_resource('organic_matter', self.genes['organic_matter_consumption'] * 1.2, self.position)

        # 根据消耗的资源增加能量
        self.energy += (water_consumed * WATER_ENERGY_CONVERSION 
                        + minerals_consumed * MINERAL_ENERGY_CONVERSION 
                        + organic_matter_consumed * ORGANIC_MATTER_ENERGY_CONVERSION) * 1.2

        if self.energy <= 0 or self.age > MAX_AGE:
            return False
        return True

    def reproduce(self, partner):
        if self.energy > self.genes['reproduction_threshold'] and partner.energy > partner.genes['reproduction_threshold']:
            if self.can_reproduce_with(partner):
                offspring_genes = self.combine_genes(partner)
                offspring = type(self)(self.environment, position=self.position, genes=offspring_genes, species_id=self.species_id)
                self.energy /= 2
                partner.energy /= 2
                offspring.energy = (self.energy + partner.energy) / 2
                return offspring
        return None

    def can_reproduce_with(self, partner):
        gene_difference = torch.norm(self.genes['species_identifier'] - partner.genes['species_identifier'])
        return gene_difference < SPECIES_DIFFERENCE_THRESHOLD

    def combine_genes(self, partner):
        combined_genes = {}
        for gene in self.genes:
            if gene == 'species_identifier':
                combined_genes[gene] = (self.genes[gene] + partner.genes[gene]) / 2
            else:
                combined_genes[gene] = (self.genes[gene] + partner.genes[gene]) / 2 + torch.normal(0, 0.1, device=self.device)
        return self.mutate_genes(combined_genes)

    def mutate_genes(self, genes):
        mutated_genes = genes.copy()
        for gene in mutated_genes:
            if torch.rand(1, device=self.device) < self.genes['mutation_rate']:
                if gene == 'species_identifier':
                    mutated_genes[gene] += torch.normal(0, 0.1, 10, device=self.device)
                else:
                    mutated_genes[gene] *= torch.normal(1, 0.1, device=self.device)
        return mutated_genes

    def move(self):
        direction = torch.randn(2, device=self.device)
        direction /= direction.norm()  # 归一化方向向量
        speed = self.genes['speed'] * MOVEMENT_SPEED
        new_position = self.position + direction * speed
        new_position = torch.clamp(new_position, torch.tensor([0, 0], device=self.device), 
                                   torch.tensor([self.environment.width - 1, self.environment.height - 1], device=self.device))
        self.position = new_position
        print(f"Organism moved to {self.position}")  # 添加这行来调试

    def draw(self, screen):
        # 这个方法现在应该是空的或者被完全移除，因为我们使用PyQt6进行绘制
        pass

    def mutate(self):
        for gene in self.genes:
            if torch.rand(1, device=self.device) < self.genes['mutation_rate']:
                self.genes[gene] *= torch.normal(1, 0.2, device=self.device)  # 增加突变幅度
        # 可能产生新的特征
        if torch.rand(1, device=self.device) < 0.01:
            new_gene = f'new_trait_{torch.randint(1000, device=self.device)}'
            self.genes[new_gene] = torch.normal(1, 0.5, device=self.device)

    def to_tensor(self):
        # 将生物体的属性转换为张量
        return torch.tensor([self.position[0], self.position[1], self.energy, self.age] + 
                            [self.genes[key] for key in sorted(self.genes.keys())], 
                            device=self.device)
