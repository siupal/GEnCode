import random

class Organism:
    def __init__(self, genes, location):
        self.genes = genes
        self.energy = genes['energy']
        self.metabolism_rate = genes['metabolism_rate']
        self.reproduction_rate = genes['reproduction_rate']
        self.mutation_rate = genes['mutation_rate']
        self.environmental_tolerance = genes['environmental_tolerance']
        self.age = 0
        self.lifespan = genes['lifespan']
        self.size = genes['size']
        self.mobility = int(genes['mobility'])
        self.type = genes['type']
        self.position = location
        self.adaptation_score = 0

    def update(self, environment, time_step):
        self.age += time_step
        self.move(environment)
        self.consume_energy()
        self.eat(environment)
        self.adapt(environment)
        if self.can_reproduce():
            self.reproduce(environment)
        self.die(environment)

    def adapt(self, environment):
        cell = environment.grid[self.position[0]][self.position[1]]
        climate_zone = environment.climate_zones[self.position[1]][self.position[0]]
        self.adaptation_score = (self.environmental_tolerance -
                                 abs(cell.temperature - self.genes['optimal_temperature']))

    def can_reproduce(self):
        return self.energy > self.reproduction_rate and random.random() < 0.1

    def reproduce(self, environment):
        offspring_genes = self.mutate_genes()
        offspring = self.__class__(offspring_genes, self.position)
        environment.add_organism(offspring)
        self.energy //= 2

    def mutate_genes(self):
        offspring_genes = self.genes.copy()
        for gene in offspring_genes:
            if random.random() < self.mutation_rate:
                offspring_genes[gene] = self.mutate(offspring_genes[gene])
        return offspring_genes

    def die(self, environment):
        if self.energy <= 0 or self.age >= self.lifespan or random.random() < 0.01:
            environment.remove_organism(self)

    def move(self, environment):
        if self.mobility > 0:
            dx = random.randint(-self.mobility, self.mobility)
            dy = random.randint(-self.mobility, self.mobility)
            new_x = max(0, min(self.position[0] + dx, environment.width - 1))
            new_y = max(0, min(self.position[1] + dy, environment.height - 1))
            self.position = (new_x, new_y)

    def consume_energy(self):
        self.energy -= self.metabolism_rate

    def eat(self, environment):
        # 由子类实现
        pass

    def mutate(self, gene_value):
        if isinstance(gene_value, (int, float)):
            return gene_value + random.uniform(-0.1 * gene_value, 0.1 * gene_value)
        return gene_value

    def interact(self, other_organisms, environment):
        # 由子类实现
        pass