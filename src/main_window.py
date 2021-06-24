import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from text import *

from functions_menu import FunctionsMenu
from viewport import *
from log import *
from new_object_dialog import *
from controller import *


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

        # MENU
        # Menu de opções
        
        self.menuBar = self.menuBar()
        
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

        editMenu = self.menuBar.addMenu('Edit')
        zoom_in = QAction('Zoom In', self)
        zoom_in.setShortcut('Ctrl++')
        #zoom_in.triggered.connect()
        editMenu.addAction(zoom_in)
        zoom_out = QAction('Zoom Out', self)
        zoom_out.setShortcut('Ctrl+-')
        #zoom_out.triggered.connect()
        editMenu.addAction(zoom_out)

        helpMenu = self.menuBar.addMenu('Help')
        getting_started = QAction('Getting Started', self)
        getting_started.triggered.connect(self.get_started)
        helpMenu.addAction(getting_started)
        helpMenu.addSeparator()
        about = QAction('About', self)
        about.triggered.connect(self.abt)
        helpMenu.addAction(about)        

        # FIM do MENU

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.action_open_dialog.trigger() 

    def put_actions(self):
        self.action_open_dialog = QAction("Open dialog", self)
    
    def input_data(self):
            self.action_open_dialog.trigger()

    def abt(self):
        QtWidgets.QMessageBox.about(
            self,
            self.tr("Computação Gráfica"),
            self.tr(
               "COMPUTAÇÃO GRÁFICA\n\n\nDesenvolvido pelos alunos:\n\n   Maria Eduarda de Melo Hang (17202304)\n   Ricardo Giuliani (17203922)"
            ),
        )
    def get_started(self):
        gt_started = QDialog(self)
        gt_started.resize(600, 300)
        gt_started.setWindowTitle('Getting Started')
        text = QLabel(GETTING_STARTED, gt_started)
        text2 = QLabel(GETTING_STARTED_2, gt_started)
        text3 = QLabel(INSTRUCTIONS, gt_started)      
        text4 = QLabel(ATALHOS, gt_started)        
        text.move(20,20)
        text2.move(20, 40)
        text3.move(20, 80)
        text4.move(20, 110)
        gt_started.exec_()

