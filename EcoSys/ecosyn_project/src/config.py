# 定义常量

# 屏幕尺寸和网格大小
SCREEN_WIDTH = 800  # 屏幕宽度（像素）
SCREEN_HEIGHT = 600  # 屏幕高度（像素）
GRID_SIZE = 20  # 每个网格单元的大小（像素）

# 颜色定义（RGB格式）
GREEN = (34, 139, 34)    # 资源的森林绿
RED = (178, 34, 34)      # 生产者的砖红色
BLUE = (70, 130, 180)    # 消费者的钢蓝色
WHITE = (245, 245, 245)  # 背景的灰白色
YELLOW = (218, 165, 32)  # 分解者的金菊色

# 其他颜色
LIGHT_GREEN = (144, 238, 144)  # 浅绿色，用于表示新生长的植物
BROWN = (139, 69, 19)    # 棕色，用于表示土壤或枯萎的植物
LIGHT_BLUE = (173, 216, 230)  # 浅蓝色，用于表示水资源
ORANGE = (255, 140, 0)   # 橙色，用于表示能量或阳光

# 环境参数初始值
INITIAL_TEMPERATURE = 25  # 初始温度（摄氏度）
INITIAL_HUMIDITY = 50    # 初始湿度（百分比）
INITIAL_LIGHT_INTENSITY = 100  # 初始光照强度（任意单位）
INITIAL_SOIL_FERTILITY = 5  # 初始土壤肥力（任意单位）

# 生物初始数量
INITIAL_PRODUCER_COUNT = 50  # 初始生产者数量
INITIAL_CONSUMER_COUNT = 20  # 初始消费者数量
INITIAL_DECOMPOSER_COUNT = 10  # 初始分解者数量

# 模拟参数
TIME_STEP = 1  # 每次模拟步骤的时间单位
SIMULATION_DURATION = 1000  # 模拟总时长（时间单位）

# 基因突变参数
MUTATION_RATE = 0.01  # 基因突变率
MUTATION_MAGNITUDE = 0.1  # 突变幅度（相对于原值的比例）

# 能量参数
ENERGY_TRANSFER_EFFICIENCY = 0.1  # 能量传递效率（捕食时）
REPRODUCTION_ENERGY_THRESHOLD = 100  # 繁殖所需的能量阈值