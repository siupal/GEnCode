from environment.environment import Environment
from organisms.plant import Plant
from organisms.consumer import Consumer
from organisms.decomposer import Decomposer
from genetics.gene_structure import create_genes
import random

class Simulation:
    def __init__(self, width, height, initial_organisms):
        self.environment = Environment(width, height)
        self.time = 0
        self.initialize_organisms(initial_organisms)

    def initialize_organisms(self, initial_organisms):
        for species, count in initial_organisms.items():
            for _ in range(count):
                location = (random.randint(0, self.environment.width-1),
                            random.randint(0, self.environment.height-1))
                genes = create_genes()
                if species == 'Plant':
                    organism = Plant(location, genes)
                elif species == 'Consumer':
                    organism = Consumer(location, genes)
                elif species == 'Decomposer':
                    organism = Decomposer(location, genes)
                self.environment.add_organism(organism)

    def run(self, steps):
        for _ in range(steps):
            self.step()

    def step(self):
        self.time += 1
        self.environment.update(1)  # 更新环境，时间步长为1

    def get_stats(self):
        stats = {
            'time': self.time,
            'temperature': self.environment.temperature,
            'plants': sum(1 for org in self.environment.organisms if isinstance(org, Plant)),
            'consumers': sum(1 for org in self.environment.organisms if isinstance(org, Consumer)),
            'decomposers': sum(1 for org in self.environment.organisms if isinstance(org, Decomposer)),
        }
        return stats

    def calculate_gene_diversity(self):
        all_genes = [org.genes for org in self.environment.organisms]
        gene_diversity = len(set(tuple(sorted(gene.items())) for gene in all_genes))
        return gene_diversity / len(self.environment.organisms) if self.environment.organisms else 0