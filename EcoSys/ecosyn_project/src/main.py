import pygame
from config import *
from simulation import Simulation
from visualization.plotting import Visualization

def main():
    """主函数，运行整个模拟过程"""
    # 初始化Pygame
    pygame.init()
    
    # 创建可视化对象
    visualization = Visualization(SCREEN_WIDTH, SCREEN_HEIGHT)

    # 设置初始生物数量
    initial_organisms = {
        'Plant': INITIAL_PRODUCER_COUNT,
        'Consumer': INITIAL_CONSUMER_COUNT,
        'Decomposer': INITIAL_DECOMPOSER_COUNT
    }
    
    # 创建模拟对象
    simulation = Simulation(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE, initial_organisms)
    
    running = True
    clock = pygame.time.Clock()
    time_steps = []
    population_counts = {'Plant': [], 'Consumer': [], 'Decomposer': []}
    gene_diversity = []

    # 主循环
    while running and simulation.time < SIMULATION_DURATION:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新模拟
        simulation.step()
        stats = simulation.get_stats()
        
        # 更新显示
        visualization.update_display(simulation.environment.grid, stats)
        
        # 记录数据
        time_steps.append(simulation.time)
        for species in population_counts:
            population_counts[species].append(stats[species.lower() + 's'])
        gene_diversity.append(simulation.calculate_gene_diversity())

        # 控制帧率
        clock.tick(60)

    # 退出Pygame
    pygame.quit()

    # 显示最终的可视化结果
    visualization.show_population_plot(time_steps, population_counts)
    visualization.show_global_distribution(simulation.environment)
    visualization.show_gene_diversity(time_steps, gene_diversity)

if __name__ == "__main__":
    main()