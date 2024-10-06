import matplotlib.pyplot as plt
import pygame
import numpy as np
from mpl_toolkits.basemap import Basemap
from config import *

class Visualization:
    def __init__(self, screen_width, screen_height):
        """
        初始化可视化类
        :param screen_width: 屏幕宽度
        :param screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("EcoSyn Simulation")
        self.font = pygame.font.Font(None, 24)

    def draw_grid(self):
        """绘制网格线"""
        for x in range(0, self.screen_width, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.screen_width, y))

    def draw_environment(self, environment):
        """
        绘制环境和生物
        :param environment: 环境对象
        """
        for y in range(len(environment)):
            for x in range(len(environment[y])):
                cell = environment[y][x]
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                # 绘制背景（土壤）
                pygame.draw.rect(self.screen, BROWN, rect)
                
                # 绘制资源
                if cell.resources > 0:
                    resource_height = int(cell.resources / 10 * GRID_SIZE)
                    resource_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + GRID_SIZE - resource_height, GRID_SIZE, resource_height)
                    pygame.draw.rect(self.screen, GREEN, resource_rect)
                
                # 绘制生物
                if cell.organism:
                    if cell.organism.species == "Plant":
                        color = RED
                    elif cell.organism.species == "Consumer":
                        color = BLUE
                    elif cell.organism.species == "Decomposer":
                        color = YELLOW
                    pygame.draw.circle(self.screen, color, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)

    def draw_stats(self, stats):
        """
        绘制统计信息
        :param stats: 统计数据字典
        """
        y = 10
        for key, value in stats.items():
            text = self.font.render(f"{key}: {value}", True, WHITE)
            self.screen.blit(text, (10, y))
            y += 30

    def update_display(self, environment, stats):
        """
        更新显示
        :param environment: 环境对象
        :param stats: 统计数据
        """
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_environment(environment)
        self.draw_stats(stats)
        pygame.display.flip()

    def show_population_plot(self, time_steps, population_counts):
        """
        显示种群数量变化图表
        :param time_steps: 时间步骤列表
        :param population_counts: 种群数量字典
        """
        plt.figure(figsize=(10, 6))
        for species, counts in population_counts.items():
            plt.plot(time_steps, counts, label=species)
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title('Population Dynamics')
        plt.show()

    def show_global_distribution(self, environment):
        """
        显示全球物种分布图
        :param environment: 环境对象
        """
        # 创建全球地图
        plt.figure(figsize=(12, 8))
        m = Basemap(projection='robin', resolution='c', lon_0=0)
        m.drawcoastlines()
        m.drawcountries()
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color='aqua')

        # 将环境数据映射到全球坐标
        lons = np.linspace(-180, 180, environment.width)
        lats = np.linspace(-90, 90, environment.height)
        x, y = m(*np.meshgrid(lons, lats))

        # 创建物种分布热力图
        species_distribution = np.zeros((environment.height, environment.width))
        for org in environment.organisms:
            species_distribution[org.location[1], org.location[0]] += 1

        # 绘制热力图
        cs = m.pcolormesh(x, y, species_distribution, cmap='YlOrRd', shading='auto')
        plt.colorbar(cs, label='Species Density')
        plt.title('Global Species Distribution')
        plt.show()

    def show_gene_diversity(self, time_steps, gene_diversity):
        """
        显示基因多样性变化图表
        :param time_steps: 时间步骤列表
        :param gene_diversity: 基因多样性列表
        """
        plt.figure(figsize=(10, 6))
        plt.plot(time_steps, gene_diversity)
        plt.xlabel('Time')
        plt.ylabel('Genetic Diversity')
        plt.title('Genetic Diversity Over Time')
        plt.show()

# 其他可视化方法可以根据需要继续添加