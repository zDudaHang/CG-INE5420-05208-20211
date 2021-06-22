import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functions_menu import FunctionsMenu
from viewport import *
from graphic_object import Point, Line, WireFrame
from log import *
from new_object_dialog import *
from text import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.put_actions()
              
    
    def init_gui(self):

        #self.Width = 600
        #self.height = int(0.618 * self.Width)
        #self.resize(self.Width, self.height)

        self.setWindowTitle('Computação gráfica')
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QGridLayout()
        self._centralWidget.setLayout(self.generalLayout)

        self.menuBar = self.menuBar()

        # Menu de opções
        fileMenu = self.menuBar.addMenu('File')
        add_obj = QAction('Adicionar Objeto', self)
        add_obj.setShortcut('Ctrl+A')
        add_obj.triggered.connect(self.input_data)
        fileMenu.addAction(add_obj)
        fileMenu.addSeparator()
        exit_action = QAction('Sair', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(sys.exit)
        fileMenu.addAction(exit_action)

        helpMenu = self.menuBar.addMenu('Help')
        getting_started = QAction('Getting Started', self)
        getting_started.triggered.connect(self.get_started)
        helpMenu.addAction(getting_started)
        helpMenu.addSeparator()
        about = QAction('About', self)
        about.triggered.connect(self.abt)
        helpMenu.addAction(about)        

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

    def input_data(self):
        self.action_open_dialog.trigger()

    def abt(self):
        about = QDialog(self)
        about.resize(250, 150)
        about.setWindowTitle('Computação Gráfica')
        text = QLabel(ABOUT, about)
        text.move(20,20)
        about.exec_()

    def get_started(self):
        gt_started = QDialog(self)
        gt_started.resize(380, 150)
        gt_started.setWindowTitle('Getting Started')
        text = QLabel(GETTING_STARTED, gt_started)
        text2 = QLabel(INSTRUCTIONS, gt_started)        
        text.move(20,20)
        text2.move(20, 80)
        gt_started.exec_()        