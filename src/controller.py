import re
from main_window import *
from new_object_dialog import *

from PyQt5.QtCore import *

class Controller():

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.main_window.show()
        self.new_object_dialog = NewObjectDialog(self.main_window)
        self.objects = []

        self.set_handlers()

    
    def set_handlers(self):
        self.main_window.action_open_dialog.triggered.connect(self.open_dialog_handler)
        self.new_object_dialog.buttons_box.accepted.connect(self.new_object_dialog_submitted_handler)
        self.new_object_dialog.buttons_box.rejected.connect(self.new_object_dialog_cancelled_handler)

    
    def new_object_dialog_submitted_handler(self):
        # print(self.new_object_dialog.comboBox.currentText())
        # print(self.new_object_dialog.coordinates.text())
        self.parse_coordinates(self.new_object_dialog.coordinates.text())

    def new_object_dialog_cancelled_handler(self):
        self.new_object_dialog.clear_inputs()
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

    def parse_coordinates(self, coordinates_expr: str) -> list:
        coordinates = []

        value = ''
        for c in coordinates_expr:
            if c == '(':
                while c != ',': value += c
                coordinates.append(value)
                value = ''
                while c != ')': value += c
                coordinates.append(value)
                value = ''
        print(coordinates)

    def start(self):
        self.app.exec()