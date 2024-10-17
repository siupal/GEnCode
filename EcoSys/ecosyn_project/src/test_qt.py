import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.setGeometry(100, 100, 300, 200)
        button = QPushButton("Click me", self)
        button.setGeometry(100, 80, 100, 30)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
