from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from graphic_object import GraphicObject

class Log(QWidget):
    def __init__(self, actions: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Log"))
        for action in actions:
            self.layout.addWidget(QLabel(f'[LOG] {action}'))
        self.setLayout(self.layout)
        
