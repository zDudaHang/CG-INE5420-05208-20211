from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton
from graphic_object import GraphicObject
from objects_list import *
from window_menu import *

class FunctionsMenu(QWidget):
    def __init__(self, objects: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Menu de funções"))

        self.objectList = ObjectsList(objects)
        self.layout.addWidget(self.objectList)

        self.windowMenu = WindowMenu()
        self.layout.addWidget(self.windowMenu)

        self.setLayout(self.layout)
