from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from graphic_object import GraphicObject

class ObjectsList(QWidget):
    def __init__(self, ):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Objetos"))
        self.setLayout(self.layout)

    def add_object(self, object: GraphicObject):
        self.layout.addWidget(QLabel(object.__str__()))