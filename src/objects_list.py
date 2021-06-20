from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from graphic_object import GraphicObject

class ObjectsList(QWidget):
    def __init__(self, objects: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Objetos"))
        for obj in objects:
            self.layout.addWidget(QLabel(obj.__str__()))
        self.setLayout(self.layout)
