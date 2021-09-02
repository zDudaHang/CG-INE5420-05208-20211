from typing import List
import sys
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QMainWindow, QMessageBox, QWidget, QErrorMessage

from src.model.point import Point3D
from src.util.wavefront import WavefrontOBJ
from src.gui.functions_menu import FunctionsMenu
from src.gui.viewport import Viewport
from src.gui.log import Log
from src.text import *
import os.path

class MainWindow(QMainWindow):
    def __init__(self, step: float, angle: float, viewport_coordinates: List[Point3D], viewport_width: int, viewport_height: int, viewport_origin: Point3D):
        super().__init__()
        self.init_gui(step, angle, viewport_coordinates, viewport_width, viewport_height, viewport_origin)
        self.put_actions()
        self.new_objs = WavefrontOBJ()
        self.error_dialog = QErrorMessage()
        
    
    def init_gui(self, step: float, angle: float, viewport_coordinates: List[Point3D], viewport_width: int, viewport_height: int, viewport_origin: Point3D):
        self.setWindowTitle('Computação gráfica')

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.generalLayout = QGridLayout()
        self._centralWidget.setLayout(self.generalLayout)

        self.functions_menu = FunctionsMenu(step, angle)
        self.generalLayout.addWidget(self.functions_menu, 0, 0, 2, 1)
        
        self.init_menu()   

        self.viewport = Viewport(viewport_coordinates, viewport_width, viewport_height, viewport_origin)
        self.generalLayout.addWidget(self.viewport, 0, 1)

        self.log = Log[str]('=== LOG ===')
        self.generalLayout.addWidget(self.log, 1, 1, 2, 1)

        self.width = 700
        self.height = int(0.618 * self.width)
        self.resize(self.width, self.height)
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)
    

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.action_open_dialog.trigger() 

    def put_actions(self):
        self.action_open_dialog = QAction("Open dialog", self)
        self.add_new_obj_action = QAction('Adicionar novos objetos', self)
        self.export_new_obj_action = QAction('Exportar objetos', self)

    def open_dialog_handler(self):
        self.action_open_dialog.trigger()

# ========== MENU & ABOUT

    def init_menu(self):
        self.menuBar = self.menuBar()

        # Menu de opções
        fileMenu = self.menuBar.addMenu('File')
        add_obj = QAction('Adicionar Objeto', self)
        add_obj.setShortcut('Ctrl+A')
        add_obj.triggered.connect(self.open_dialog_handler)
        fileMenu.addAction(add_obj)
        fileMenu.addSeparator()

        open_file = QAction('Abrir Arquivo', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.open_file_dialog)
        fileMenu.addAction(open_file)

        save_file = QAction('Salvar Arquivo', self)
        save_file.setShortcut('Ctrl+S')
        save_file.triggered.connect(self.save_file_dialog)
        fileMenu.addAction(save_file)
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

    def abt(self):
        QMessageBox.about(
            self,
            self.tr("Computação Gráfica"),
            self.tr(
               "COMPUTAÇÃO GRÁFICA\n\n\nDesenvolvido pelos alunos:\n\n   Maria Eduarda de Melo Hang (17202304)\n   Ricardo Giuliani (17203922)"
            ),
        )
    
    def get_started(self): 
        gt_started = QDialog(self)

        gt_started.setMinimumHeight(200)
        gt_started.setMinimumWidth(800)
        gt_started.setMaximumWidth(800)
        gt_started.setMaximumHeight(600)

        gt_started.setWindowTitle('Getting Started') 

        text = QLabel(GETTING_STARTED, gt_started) 
        text2 = QLabel(GETTING_STARTED_2, gt_started) 
        text3 = QLabel(INSTRUCTIONS, gt_started)       
        text4 = QLabel(ATALHOS, gt_started)
        text5 = QLabel(CHANGE_COLOR, gt_started)   

        text.move(20,20) 
        text2.move(20, 40) 
        text3.move(20, 80) 
        text4.move(20, 110) 
        text5.move(20, 170)

        gt_started.exec_()

# ========== IMPORT & EXPORT .OBJ FILES
 
    def open_file_dialog(self):
        filename = QFileDialog().getOpenFileName()

        if filename[0] == []:
            return

        path_obj = filename[0]
        path_mtl = os.path.dirname(filename[0])

        if path_obj[-3:] != "obj":
            self.error_dialog.showMessage('Você deve selecionar um arquivo no formato .obj')
            return
        
        try:
            self.new_objs.load_obj(path_obj,path_mtl)
            self.add_new_obj_action.trigger()
            
        except FileNotFoundError:
            pass
    
    def save_file_dialog(self):    
        self.export_new_obj_action.trigger()