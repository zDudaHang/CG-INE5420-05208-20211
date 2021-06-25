import sys
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions_menu import FunctionsMenu
from viewport import *
from log import *
from new_object_dialog import *

class MainWindow(QMainWindow):
    def __init__(self, step: int):
        super().__init__()
        self.init_gui(step)
        self.put_actions()
        
    
    def init_gui(self, step):
        self.setWindowTitle('Computação gráfica')

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.generalLayout = QGridLayout()
        self._centralWidget.setLayout(self.generalLayout)

        self.functions_menu = FunctionsMenu(step)
        self.generalLayout.addWidget(self.functions_menu, 0, 0)

        self.viewport = Viewport()
        self.generalLayout.addWidget(self.viewport, 0, 1)

        self.log = Log()
        self.generalLayout.addWidget(self.log, 1, 1)

        self.width = 600
        self.height = int(0.618 * self.width)
        self.resize(self.width, self.height)
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.action_open_dialog.trigger() 

    def put_actions(self):
        self.action_open_dialog = QAction("Open dialog", self)


