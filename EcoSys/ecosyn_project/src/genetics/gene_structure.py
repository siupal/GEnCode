import random
from config import MUTATION_RATE, MUTATION_MAGNITUDE

class Gene:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def mutate(self):
        if random.random() < MUTATION_RATE:
            mutation = random.uniform(-MUTATION_MAGNITUDE, MUTATION_MAGNITUDE)
            return Gene(self.name, max(0, self.value + mutation))
        return Gene(self.name, self.value)

class Genome:
    def __init__(self, genes):
        self.genes = {gene.name: gene for gene in genes}

    def get_gene(self, name):
        return self.genes[name]

    def mutate(self):
        return Genome([gene.mutate() for gene in self.genes.values()])

def create_genes():
    return {
        'metabolism_rate': random.uniform(0.5, 1.5),
        'reproduction_rate': random.uniform(0.5, 1.5),
        'movement_speed': random.uniform(0.5, 1.5),
        'perception_range': random.uniform(0.5, 1.5),
        'temperature_tolerance': random.uniform(-20, 40),
        'longevity': random.uniform(0.8, 1.2)
    }

def mutate_genes(genes, mutation_rate=0.01):
    mutated_genes = genes.copy()
    for gene in mutated_genes:
        if random.random() < mutation_rate:
            mutated_genes[gene] *= random.uniform(0.9, 1.1)
    return mutated_genes
