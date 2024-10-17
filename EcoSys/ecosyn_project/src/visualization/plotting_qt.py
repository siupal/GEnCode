from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem, 
                             QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSlider)
from PyQt6.QtGui import QColor, QBrush, QPen, QPainter, QPixmap, QImage, QFont, QPolygonF, QTransform
from PyQt6.QtCore import Qt, QRectF, QTimer, QPointF
from config import *
import numpy as np
from organisms.plant import Plant
from organisms.consumer import Consumer
from organisms.decomposer import Decomposer
import pyqtgraph as pg
import torch

class EnvironmentItem(QGraphicsPixmapItem):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.pixmap = QPixmap(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.update_pixmap()

    def update_pixmap(self):
        image = QImage(SCREEN_WIDTH, SCREEN_HEIGHT, QImage.Format.Format_RGB32)
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                color = self.get_terrain_color(x, y)
                image.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(image))

    def get_terrain_color(self, x, y):
        elevation = self.environment.terrain[y, x].item()
        temperature = self.environment.temperature[y, x].item()
        humidity = self.environment.humidity[y, x].item()
        
        if self.environment.rivers[y, x]:
            return QColor(0, 0, 255)  # 蓝色表示河流
        elif elevation < 20:
            return QColor(0, 0, 150)  # 深蓝色表示水
        elif elevation < 40:
            return QColor(240, 240, 64)  # 沙滩
        elif elevation < 60:
            green = min(255, max(0, int(100 + humidity)))
            return QColor(0, green, 0)  # 绿色，湿度影响深浅
        elif elevation < 80:
            green = min(255, max(0, int(50 + humidity / 2)))
            return QColor(0, green, 0)  # 深绿色森林
        else:
            snow_factor = max(0, min(255, int((elevation - 80) * 12.75)))
            return QColor(snow_factor, snow_factor, snow_factor)  # 白色山顶

class OrganismItem(QGraphicsItem):
    def __init__(self, organism):
        super().__init__()
        self.organism = organism
        self.setPos(organism.position[0], organism.position[1])

    def boundingRect(self):
        size = max(5, min(20, self.organism.genes['size'] * 5))  # 增加生物体的大小
        return QRectF(-size/2, -size/2, size, size)

    def paint(self, painter, option, widget):
        if isinstance(self.organism, Plant):
            base_color = QColor(0, 255, 0)
            shape = 'circle'
        elif isinstance(self.organism, Consumer):
            base_color = QColor(255, 0, 0)
            shape = 'triangle'
        elif isinstance(self.organism, Decomposer):
            base_color = QColor(128, 128, 128)
            shape = 'square'
        else:
            base_color = QColor(0, 0, 0)
            shape = 'circle'

        # 使用物种ID来调整颜色，创造物种间的视觉差异
        hue = (self.organism.species_id * 137) % 360  # 使用黄金角来创造均匀分布的色相
        color = QColor.fromHsv(hue, base_color.saturation(), base_color.value())

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))

        rect = self.boundingRect()
        if shape == 'circle':
            painter.drawEllipse(rect)
        elif shape == 'triangle':
            points = [
                rect.bottomLeft(),
                rect.bottomRight(),
                QPointF(rect.center().x(), rect.top())
            ]
            painter.drawPolygon(QPolygonF(points))
        elif shape == 'square':
            painter.drawRect(rect)

        # 添加能量指示器
        energy_percentage = self.organism.energy / INITIAL_ENERGY
        energy_bar_height = rect.height() * energy_percentage
        energy_bar_rect = QRectF(rect.left(), rect.bottom() - energy_bar_height, 2, energy_bar_height)
        painter.fillRect(energy_bar_rect, Qt.GlobalColor.yellow)

class VisualizationWidget(QWidget):
    def __init__(self, environment):
        super().__init__()
        print("Initializing VisualizationWidget...")
        
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 左侧布局：环境视图和缩放滑块
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 2)  # 增加左侧布局的比例

        # 环境视图
        self.env_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.env_view.setScene(self.scene)
        self.env_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.env_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.env_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        left_layout.addWidget(self.env_view)

        print("Creating EnvironmentItem...")
        self.environment_item = EnvironmentItem(environment)
        self.scene.addItem(self.environment_item)
        print("EnvironmentItem created and added to scene.")

        self.organism_items = {}
        self.update_organisms(environment.organisms)
        print("Organisms updated.")

        # 添加缩放滑块
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.zoom)
        left_layout.addWidget(self.zoom_slider)

        # 右侧布局：图表和信息
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 1)

        # 种群数量图表
        self.population_plot = pg.PlotWidget(title="Population Over Time")
        right_layout.addWidget(self.population_plot)
        self.population_curves = {
            Plant: self.population_plot.plot(pen='g', name='Plants'),
            Consumer: self.population_plot.plot(pen='r', name='Consumers'),
            Decomposer: self.population_plot.plot(pen='gray', name='Decomposers')
        }
        self.population_plot.setLabel('left', 'Population')
        self.population_plot.setLabel('bottom', 'Time')
        self.population_plot.addLegend()

        # 物种多样性图表
        self.diversity_plot = pg.PlotWidget(title="Species Diversity Over Time")
        right_layout.addWidget(self.diversity_plot)
        self.diversity_curve = self.diversity_plot.plot(pen='b', name='Species Diversity')
        self.diversity_plot.setLabel('left', 'Diversity Index')
        self.diversity_plot.setLabel('bottom', 'Time')

        # 资源图表
        self.resource_plot = pg.PlotWidget(title="Resource Levels Over Time")
        right_layout.addWidget(self.resource_plot)
        self.resource_curves = {
            'Water': self.resource_plot.plot(pen='c', name='Water'),
            'Minerals': self.resource_plot.plot(pen='y', name='Minerals'),
            'Organic Matter': self.resource_plot.plot(pen='m', name='Organic Matter')
        }
        self.resource_plot.setLabel('left', 'Resource Level')
        self.resource_plot.setLabel('bottom', 'Time')
        self.resource_plot.addLegend()

        # 添加信息标签
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.info_label)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_visualization)
        self.update_timer.start(100)  # 每100毫秒更新一次，减少更新频率

        self.redraw_counter = 0

        self.time_steps = []
        self.population_history = {Plant: [], Consumer: [], Decomposer: []}
        self.diversity_history = []
        self.resource_history = {'Water': [], 'Minerals': [], 'Organic Matter': []}
        self.update_counter = 0  # 添加更新计数器
        print("VisualizationWidget initialization complete.")

        self.scale = 1.0
        self.offset = QPointF(0, 0)
        self.last_pan_pos = None

    def wheelEvent(self, event):
        zoom_factor = 1.2
        if event.angleDelta().y() < 0:
            zoom_factor = 1 / zoom_factor

        self.env_view.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.env_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.last_pan_pos:
            delta = event.pos() - self.last_pan_pos
            self.env_view.horizontalScrollBar().setValue(self.env_view.horizontalScrollBar().value() - delta.x())
            self.env_view.verticalScrollBar().setValue(self.env_view.verticalScrollBar().value() - delta.y())
            self.last_pan_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.env_view.setDragMode(QGraphicsView.DragMode.NoDrag)
        super().mouseReleaseEvent(event)

    def zoom(self, value):
        scale = value / 100.0
        self.env_view.setTransform(QTransform().scale(scale, scale))

    def update_visualization(self):
        self.redraw_counter += 1
        if self.redraw_counter % 2 == 0:  # 每2次更新才重绘，提高更新频率
            self.environment_item.update_pixmap()
            self.update_organisms(self.environment_item.environment.organisms)
            self.scene.update()

        # 调整视图以适应所有内容
        self.env_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def update_organisms(self, organisms):
        # 使用批量操作更新生物体位置
        positions = torch.stack([org.position for org in organisms])
        scale_x = SCREEN_WIDTH / self.environment_item.environment.width
        scale_y = SCREEN_HEIGHT / self.environment_item.environment.height
        screen_positions = positions * torch.tensor([scale_x, scale_y], device=positions.device)

        for org, pos in zip(organisms, screen_positions):
            org_id = id(org)
            if org_id in self.organism_items:
                self.organism_items[org_id].setPos(pos[0].item(), pos[1].item())
            else:
                item = OrganismItem(org)
                item.setPos(pos[0].item(), pos[1].item())
                self.scene.addItem(item)
                self.organism_items[org_id] = item

        # 移除不再存在的生物体
        for org_id in list(self.organism_items.keys()):
            if org_id not in [id(org) for org in organisms]:
                self.scene.removeItem(self.organism_items[org_id])
                del self.organism_items[org_id]

        self.scene.update()

    def update_stats(self, organism_types, species_count, resources):
        self.update_counter += 1
        if self.update_counter % 5 == 0:  # 每5次更新才添加新的数据点
            self.time_steps.append(len(self.time_steps))
            
            print(f"Updating stats: {organism_types}")  # 添加这行来调试
            
            # 更新种群数量图表
            for org_type, count in organism_types.items():
                self.population_history[org_type].append(count)
                self.population_curves[org_type].setData(self.time_steps, self.population_history[org_type])

            # 计算并更新物种多样性指数
            total_organisms = sum(species_count.values())
            if total_organisms > 0:
                diversity_index = -sum((count / total_organisms) * np.log(count / total_organisms) for count in species_count.values() if count > 0)
            else:
                diversity_index = 0
            self.diversity_history.append(diversity_index)
            self.diversity_curve.setData(self.time_steps, self.diversity_history)

            # 更新资源图表
            for resource_type, level in resources.items():
                self.resource_history[resource_type].append(level)
                self.resource_curves[resource_type].setData(self.time_steps, self.resource_history[resource_type])

        # 更新信息标签
        stats_text = f"Plants: {organism_types[Plant]}\n"
        stats_text += f"Consumers: {organism_types[Consumer]}\n"
        stats_text += f"Decomposers: {organism_types[Decomposer]}\n"
        stats_text += f"Number of species: {len(species_count)}\n"
        stats_text += f"Diversity Index: {diversity_index:.2f}\n"
        stats_text += f"Water: {resources['Water']:.2f}\n"
        stats_text += f"Minerals: {resources['Minerals']:.2f}\n"
        stats_text += f"Organic Matter: {resources['Organic Matter']:.2f}"
        
        self.info_label.setText(stats_text)

        # 减少图表更新频率
        if self.update_counter % 10 == 0:  # 每10次更新才更新图表
            for plot in [self.population_plot, self.diversity_plot, self.resource_plot]:
                plot.enableAutoRange()

        return stats_text
