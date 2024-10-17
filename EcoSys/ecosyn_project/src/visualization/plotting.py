import pygame
import pygame_gui
import matplotlib.pyplot as plt
from config import *
import numpy as np
import random
import os
import colorsys
import noise

class Visualization:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.ui_manager = pygame_gui.UIManager((screen_width, screen_height))
        self.setup_ui()
        self.camera_x, self.camera_y = 0, 0
        self.zoom = 1.0

    def setup_ui(self):
        self.info_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.screen_width - 200, 0), (200, self.screen_height)),
            manager=self.ui_manager
        )
        self.population_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 10), (180, 100)),
            html_text="Population: <br>Plants: 0<br>Consumers: 0<br>Decomposers: 0",
            manager=self.ui_manager,
            container=self.info_panel
        )

    def draw_environment(self, environment):
        surface = pygame.Surface((self.screen_width, self.screen_height))
        cell_width = self.screen_width // environment.width
        cell_height = self.screen_height // environment.height

        for y in range(environment.height):
            for x in range(environment.width):
                color = self.get_terrain_color(environment.terrain[y][x])
                rect = pygame.Rect(
                    (x * cell_width - self.camera_x) * self.zoom,
                    (y * cell_height - self.camera_y) * self.zoom,
                    cell_width * self.zoom,
                    cell_height * self.zoom
                )
                pygame.draw.rect(surface, color, rect)

        return surface

    def get_terrain_color(self, elevation):
        if elevation < 20:
            return self.blend_colors((0, 0, 255), (0, 255, 255), elevation / 20)
        elif elevation < 40:
            return self.blend_colors((0, 255, 255), (240, 240, 64), (elevation - 20) / 20)
        elif elevation < 60:
            return self.blend_colors((240, 240, 64), (0, 128, 0), (elevation - 40) / 20)
        elif elevation < 80:
            return self.blend_colors((0, 128, 0), (128, 64, 0), (elevation - 60) / 20)
        else:
            return self.blend_colors((128, 64, 0), (255, 255, 255), (elevation - 80) / 20)

    def blend_colors(self, color1, color2, blend_factor):
        r = int(color1[0] * (1 - blend_factor) + color2[0] * blend_factor)
        g = int(color1[1] * (1 - blend_factor) + color2[1] * blend_factor)
        b = int(color1[2] * (1 - blend_factor) + color2[2] * blend_factor)
        return (r, g, b)

    def draw_organisms(self, organisms, surface):
        cell_width = self.screen_width // organisms[0].environment.width
        cell_height = self.screen_height // organisms[0].environment.height
        for organism in organisms:
            color = self.get_organism_color(organism)
            size = int(organism.size * min(cell_width, cell_height) / 2)
            pos = (
                int((organism.position[0] * cell_width - self.camera_x) * self.zoom),
                int((organism.position[1] * cell_height - self.camera_y) * self.zoom)
            )
            pygame.draw.circle(surface, color, pos, size)

    def get_organism_color(self, organism):
        if isinstance(organism, Plant):
            hue = 0.3  # Green
        elif isinstance(organism, Consumer):
            hue = 0.0  # Red
        else:  # Decomposer
            hue = 0.6  # Blue
        
        saturation = min(1.0, organism.energy / 200)
        value = min(1.0, organism.size / 10)
        
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return tuple(int(x * 255) for x in rgb)

    def update_ui(self, stats):
        population_text = f"Population: <br>Plants: {stats[Plant]}<br>Consumers: {stats[Consumer]}<br>Decomposers: {stats[Decomposer]}"
        self.population_text.html_text = population_text
        self.population_text.rebuild()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.zoom *= 1.1
            elif event.button == 5:  # Scroll down
                self.zoom /= 1.1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.camera_x -= 10 / self.zoom
            elif event.key == pygame.K_RIGHT:
                self.camera_x += 10 / self.zoom
            elif event.key == pygame.K_UP:
                self.camera_y -= 10 / self.zoom
            elif event.key == pygame.K_DOWN:
                self.camera_y += 10 / self.zoom

        self.ui_manager.process_events(event)

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        self.ui_manager.draw_ui(screen)

    def draw_stats(self, screen, stats, font):
        y = 70
        for organism_type, count in stats.items():
            text = font.render(f"{organism_type.__name__}: {count}", True, BLACK)
            screen.blit(text, (10, y))
            y += 40

    def plot_population_dynamics(self, time_steps, population_counts):
        plt.figure(figsize=(10, 6))
        for species, counts in population_counts.items():
            plt.plot(time_steps, counts, label=species.__name__)
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title('Population Dynamics')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_gene_distribution(self, organisms, gene_name):
        gene_values = [org.genome.get_gene(gene_name).value for org in organisms]
        plt.figure(figsize=(10, 6))
        plt.hist(gene_values, bins=20)
        plt.xlabel(f'{gene_name} Value')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {gene_name} Gene')
        plt.show()
