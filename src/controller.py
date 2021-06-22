import re
from main_window import *
from new_object_dialog import *
from graphic_object import GraphicObject
from PyQt5.QtCore import *

class Controller():

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.main_window.show()
        self.new_object_dialog = NewObjectDialog(self.main_window)
        self.objects : list[GraphicObject] = []
        self.set_window_values()
        self.set_handlers()

    def set_window_values(self):
        self.x_w_min = 0
        self.y_w_min = 0

        self.x_w_max = 600
        self.y_w_max = 600
        
    
    def set_handlers(self):
        self.main_window.action_open_dialog.triggered.connect(self.open_dialog_handler)
        self.new_object_dialog.buttons_box.accepted.connect(self.new_object_dialog_submitted_handler)
        self.new_object_dialog.buttons_box.rejected.connect(self.new_object_dialog_cancelled_handler)

# ====================== HANDLERS:
    
    def new_object_dialog_submitted_handler(self):
        if len(self.new_object_dialog.name_input.text()) == 0:
            self.main_window.log.add_log("[ERRO] O nome não pode ser vazio!")
            return
        type = self.new_object_dialog.combo_box.currentText()
        coordinates = self.parse_coordinates(self.new_object_dialog.coordinates.text())
        name = self.new_object_dialog.name_input.text()
        self.new_object_dialog.clear_inputs()
        self.add_new_object(name, coordinates, type)
        self.main_window.viewport.draw_objects(self.objects, self.x_w_min, self.y_w_min, self.x_w_max, self.y_w_max)

    def new_object_dialog_cancelled_handler(self):
        self.new_object_dialog.clear_inputs()
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

# ====================== UTILITIES:        

    def parse_coordinates(self, coordinates_expr: str) -> list:
        tuples = re.findall(r"(\d+,\d+)", coordinates_expr)

        coordinates = []

        for t in tuples:
            coordinates.extend(t.split(','))

        return list(map(lambda c: float(c), coordinates))

    def add_new_object(self, name: str, coordinates: str, type: str):
        type_enum = GraphicObjectEnum.valueOf(type)
        
        graphic_obj : GraphicObject = None

        try:
            if (type_enum == GraphicObjectEnum.POINT):
                graphic_obj = Point(name, coordinates)
            if (type_enum == GraphicObjectEnum.LINE):
                graphic_obj = Line(name, coordinates)
            if (type_enum == GraphicObjectEnum.WIREFRAME):
                graphic_obj = WireFrame(name, coordinates)
        except ValueError as e:
            self.main_window.log.add_log(e)

        if graphic_obj != None:
            self.objects.append(graphic_obj)
            self.main_window.functions_menu.object_list.add_object(graphic_obj)
        self.main_window.log.add_log(f'[INFO] Objeto {name} do tipo {type}, cujas coordenadas são {coordinates}, foi criado com sucesso!')

    def start(self):
        self.app.exec()