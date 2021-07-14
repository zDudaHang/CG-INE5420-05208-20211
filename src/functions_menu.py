from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from objects_list import *
from window_menu import *
from h_line import QHLine

class FunctionsMenu(QWidget):
    def __init__(self, step: float, angle: float):
        super().__init__()

        self.layout = QVBoxLayout()
  
        self.layout.addWidget(QLabel("Menu de funções"))

        self.layout.addWidget(QHLine())

        self.object_list = ObjectsList()
        self.layout.addWidget(self.object_list)

        self.layout.addWidget(QHLine())

        self.window_menu = WindowMenu(step, angle)
        self.layout.addWidget(self.window_menu)

        self.setLayout(self.layout)

        self.width = 500
        self.height = 500
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)