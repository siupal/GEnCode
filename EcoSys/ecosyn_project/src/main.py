import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pygame
import pygame_gui
import torch
from config import *
from simulation import Simulation
from visualization.plotting import Visualization

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EcoSyn - Ecosystem Simulator")

simulation = Simulation()
visualization = Visualization(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            visualization.handle_event(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == visualization.start_button:
                    paused = False
                elif event.ui_element == visualization.pause_button:
                    paused = True
                elif event.ui_element == visualization.reset_button:
                    simulation.reset()
                elif event.ui_element == visualization.plot_button:
                    visualization.plot_population_dynamics(simulation.time_steps, simulation.population_history)
                    visualization.plot_gene_distribution(simulation.organisms, 'size')

        visualization.update(time_delta)

        if not paused:
            simulation.update()

        screen.fill(WHITE)
        env_surface = visualization.draw_environment(simulation.environment)
        screen.blit(env_surface, (0, 0))
        visualization.draw_organisms(simulation.organisms, screen)
        
        stats = simulation.get_stats()
        visualization.update_ui(stats)
        visualization.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
