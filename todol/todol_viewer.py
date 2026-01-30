import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QWidget, QVBoxLayout, QLabel, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt

class TodoWindow(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("Todo List")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()

        for task_info in tasks.values():
            task_label = QLabel(task_info['task'])
            font = QFont("Arial", 12)
            task_label.setFont(font)
            if task_info["completed"]:
                task_label.setStyleSheet("color: gray; text-decoration: line-through;")
            else:
                task_label.setStyleSheet("color: white;")
            container_layout.addWidget(task_label)

        container.setLayout(container_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        self.setLayout(layout)

class GuiApp:
    @staticmethod
    def main():
        with open("/home/wattox/.local/share/todol/todoFiles/main.json") as f:
            data = json.load(f)

        app = QApplication(sys.argv)

        trayIcon = QSystemTrayIcon(QIcon("/home/wattox/Documents/github/todol/assets/demo.png"))
        trayIcon.show()

        window = TodoWindow(data["tasks"])

        def show_window(reason):
            if reason == QSystemTrayIcon.Trigger:
                window.show()
                window.activateWindow()

        trayIcon.activated.connect(show_window)

        sys.exit(app.exec_())

if __name__ == "__main__":
    GuiApp.main()
