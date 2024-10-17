import sys
import os
import traceback
import logging

# 设置日志
logging.basicConfig(filename='simulation.log', level=logging.DEBUG)

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QSplitter
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QScreen
from config import *
from simulation import Simulation
from visualization.plotting_qt import VisualizationWidget

print("Starting application...")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing MainWindow...")
        self.setWindowTitle("EcoSyn - Ecosystem Simulator")
        self.setWindowState(Qt.WindowState.WindowMaximized)  # 设置窗口最大化
        self.showFullScreen()  # 显示全屏
        print("Window set to full screen.")

        print("Creating Simulation...")
        self.simulation = Simulation()
        print("Simulation created.")

        print("Creating VisualizationWidget...")
        self.visualization = VisualizationWidget(self.simulation.environment)
        print("VisualizationWidget created.")

        print("Setting up UI...")
        self.setup_ui()
        print("UI setup complete.")

        print("Setting up timer...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(50)  # 每50毫秒更新一次，减少更新频率
        print("Timer setup complete.")
        
        self.frame_count = 0
        print("MainWindow initialization complete.")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # 使用QSplitter来允许用户调整可视化和控制面板的大小
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        splitter.addWidget(self.visualization)

        control_widget = QWidget()
        control_layout = QVBoxLayout()
        control_widget.setLayout(control_layout)
        splitter.addWidget(control_widget)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_simulation)
        control_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)
        control_layout.addWidget(self.reset_button)

        self.exit_fullscreen_button = QPushButton("Exit Fullscreen")
        self.exit_fullscreen_button.clicked.connect(self.exit_fullscreen)
        control_layout.addWidget(self.exit_fullscreen_button)

        self.stats_label = QLabel()
        control_layout.addWidget(self.stats_label)

        # 设置splitter的初始大小
        screen = QApplication.primaryScreen().size()
        splitter.setSizes([int(screen.width() * 0.8), int(screen.width() * 0.2)])

    def start_simulation(self):
        print("Starting simulation...")  # 添加这行来调试
        self.timer.start()

    def pause_simulation(self):
        self.timer.stop()

    def reset_simulation(self):
        self.simulation.reset()
        self.visualization.update_environment(self.simulation.environment)

    def update_simulation(self):
        self.frame_count += 1
        if self.frame_count % 20 == 0:  # 每20帧打印一次
            print(f"Frame: {self.frame_count}")
        try:
            self.simulation.update()
        except Exception as e:
            logging.error(f"Error in update simulation: {str(e)}")
            logging.error(traceback.format_exc())

    def exit_fullscreen(self):
        self.showNormal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    print("Entering main...")
    app = QApplication(sys.argv)
    print("QApplication created.")
    window = MainWindow()
    print("MainWindow created.")
    window.show()
    print("Window shown.")
    sys.exit(app.exec())
