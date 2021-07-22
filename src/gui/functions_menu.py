from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QRadioButton, QVBoxLayout, QLabel, QWidget

from src.gui.objects_list import ObjectsList
from src.gui.window_menu import WindowMenu
from src.gui.h_line import QHLine

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

        self.clipping_layout = QVBoxLayout()
        self.radiobuttons_layout = QHBoxLayout()
        self.clipping_layout.addWidget(QLabel('Técnica de clipagem de retas'))

        self.clipping_button_group = QButtonGroup(self)
        self.liangb_radiobutton = QRadioButton("Liang Barksy")
        self.liangb_radiobutton.toggled.connect(self.handle_click)
        self.clipping_button_group.addButton(self.liangb_radiobutton)

        self.radiobuttons_layout.addWidget(self.liangb_radiobutton)

        self.cohens_radiobutton = QRadioButton("Cohen-Sutherland")
        self.cohens_radiobutton.toggled.connect(self.handle_click)
        self.clipping_button_group.addButton(self.cohens_radiobutton)

        self.radiobuttons_layout.addWidget(self.cohens_radiobutton)

        self.clipping_layout.addLayout(self.radiobuttons_layout)
        
        self.layout.addLayout(self.clipping_layout)

        self.setLayout(self.layout)

        self.width = 500
        self.height = 600
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)

    def handle_click(self, value):
        print(value)