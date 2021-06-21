import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions_menu import FunctionsMenu
from viewport import *
from graphic_object import Point, Line, WireFrame
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

        self.functions_menu = FunctionsMenu()
        self.generalLayout.addWidget(self.functions_menu, 0, 0)

        self.viewport = Viewport()
        self.generalLayout.addWidget(self.viewport, 0, 1)

        self.log = Log()
        self.generalLayout.addWidget(self.log, 1, 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.action_open_dialog.trigger() 

    def put_actions(self):
        self.action_open_dialog = QAction("Open dialog", self)

