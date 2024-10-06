from config import INITIAL_TEMPERATURE, INITIAL_HUMIDITY, INITIAL_LIGHT_INTENSITY, INITIAL_SOIL_FERTILITY

class EnvironmentCell:
    def __init__(self):
        self.temperature = INITIAL_TEMPERATURE
        self.humidity = INITIAL_HUMIDITY
        self.light_intensity = INITIAL_LIGHT_INTENSITY
        self.soil_fertility = INITIAL_SOIL_FERTILITY
        self.resources = 0
        self.organism = None

    def update(self):
        # 这里可以添加环境变化的逻辑
        pass

    def add_organism(self, organism):
        self.organism = organism

    def remove_organism(self):
        self.organism = None

    def add_resources(self, amount):
        self.resources += amount

    def remove_resources(self, amount):
        self.resources = max(0, self.resources - amount)