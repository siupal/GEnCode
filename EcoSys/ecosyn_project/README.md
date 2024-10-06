# EcoSyn: 地球尺度生物演化模拟程序

EcoSyn 是一个基于 Python 的生态系统模拟程序，旨在模拟地球尺度的生物演化过程。该程序利用 GPU 加速计算，在普通个人电脑上实现高效运行。

## 功能特点

- 模拟地球尺度的生物演化过程
- 包含单细胞和多细胞生物，如植物、消费者和分解者
- 实现有性和无性繁殖机制
- 模拟基因突变和自然选择过程
- 实现基本的地理和气候变化模拟
- 生物之间的复杂交互和生态关系
- 直观的可视化界面
- 支持参数调整和情景模拟

## 安装指南

1. 确保您的系统已安装 Python 3.7 或更高版本。

2. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/ecosyn.git
   ```

3. 进入项目目录：
   ```bash
   cd ecosyn
   ```

4. 创建并激活虚拟环境（可选但推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
   ```

5. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 运行模拟：
   ```bash
   python EcoSyn.py
   ```

2. 在图形界面中，您可以观察到生态系统的实时变化。模拟过程中会显示以下信息：
   - 生物分布图
   - 当前时间步
   - 各物种的数量统计

3. 模拟结束后，程序将显示以下可视化结果：
   - 种群动态图表
   - 全球物种分布热力图
   - 基因多样性变化图表

## 项目结构

```
ecosyn_project/
│
├── src/
│   ├── config.py              # 配置文件，包含所有可调参数
│   ├── main.py                # 主程序入口
│   ├── simulation.py          # 模拟核心逻辑
│   ├── environment/
│   │   ├── environment.py     # 环境类，管理整个生态系统
│   │   └── environment_cell.py # 环境单元类，代表单个网格
│   ├── organisms/
│   │   ├── base_organism.py   # 基础生物类
│   │   ├── plant.py           # 植物类
│   │   ├── consumer.py        # 消费者类
│   │   └── decomposer.py      # 分解者类
│   ├── genetics/
│   │   └── gene_structure.py  # 基因结构和突变机制
│   └── visualization/
│       └── plotting.py        # 可视化功能
│
├── README.md                  # 项目说明文档
└── requirements.txt           # 项目依赖列表
```

## 配置说明

您可以在 `src/config.py` 文件中调整以下参数：

- 屏幕尺寸和网格大小
- 颜色设置
- 初始环境参数（温度、湿度、光照等）
- 初始生物数量
- 模拟持续时间
- 基因突变率和其他遗传参数

## 扩展和自定义

1. 添加新的生物类型：
   - 继承 `base_organism.py` 中的基础生物类
   - 实现特定的行为和属性

2. 修改环境参数：
   - 在 `environment/environment.py` 中添加或修改环境参数

3. 调整基因结构：
   - 在 `genetics/gene_structure.py` 中调整基因结构和突变机制

4. 扩展可视化功能：
   - 在 `visualization/plotting.py` 中添加新的可视化方法

## 贡献指南

我们欢迎任何形式的贡献！如果您想为 EcoSyn 项目做出贡献，请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 将您的更改推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请联系项目维护者：

- 邮箱：your.email@example.com
- GitHub：[@yourusername](https://github.com/yourusername)

感谢您对 EcoSyn 项目的关注和支持！