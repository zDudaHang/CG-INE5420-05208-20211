'''from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton
from graphic_object import GraphicObject
from PyQt5.QtCore import *

class WindowMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.box = QHBoxLayout()
        self.layout.addWidget(QLabel("Window"))
        
        # ZOOM:
        self.box.addWidget(QLabel("Zoom"))

        zoom_mais = QPushButton('+')
        #zoom_mais.setFixedSize(QSize(15, 15))
        zoom_mais.resize(15,15)
        self.box.addWidget(zoom_mais)

        zoom_menos = QPushButton('-')
        zoom_menos.setFixedSize(QSize(15, 15))
        self.box.addWidget(zoom_menos)

        self.box.setSpacing(0)
        #self.box.addWidget(QPushButton('+'))
        #self.box.addWidget(QPushButton('-'))

        self.layout.addLayout(self.box)
        self.setLayout(self.layout)'''
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