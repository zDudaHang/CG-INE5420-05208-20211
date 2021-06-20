from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton
from graphic_object import GraphicObject
from objects_list import *
from window_menu import *

class FunctionsMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Menu de funções"))

        self.object_list = ObjectsList()
        self.layout.addWidget(self.object_list)

        self.window_menu = WindowMenu()
        self.layout.addWidget(self.window_menu)

        self.setLayout(self.layout)
