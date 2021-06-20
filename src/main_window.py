import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions_menu import FunctionsMenu
from viewport import *
from graphic_object import Point, Line, Polygon
from log import *
from new_object_dialog import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.put_actions()
        
    
    def init_gui(self):
        self.setWindowTitle('Computação gráfica')
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QGridLayout()
        self._centralWidget.setLayout(self.generalLayout)

        objects = []

        objects.append(Point('Ponto1', [0,0]))
        objects.append(Line('Linha1', [0,0,1,1]))
        objects.append(Polygon('Polígono1', [0,0,1,1,2,2]))

        self.functionsMenu = FunctionsMenu(objects)
        self.generalLayout.addWidget(self.functionsMenu, 0, 0)

        self.viewport = Viewport()
        self.generalLayout.addWidget(self.viewport, 0, 1)

        self.log = Log(["Added a polygon, Added a line"])
        self.generalLayout.addWidget(self.log, 1, 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.action_open_dialog.trigger() 

    def put_actions(self):
        self.action_open_dialog = QAction("Open dialog", self)

