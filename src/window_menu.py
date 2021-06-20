from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton
from graphic_object import GraphicObject

class WindowMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.box = QHBoxLayout()
        self.layout.addWidget(QLabel("Window"))

        # ZOOM:
        self.box.addWidget(QLabel("Zoom"))
        self.box.addWidget(QPushButton('+'))
        self.box.addWidget(QPushButton('-'))

        self.layout.addLayout(self.box)
        self.setLayout(self.layout)
