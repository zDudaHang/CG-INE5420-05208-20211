import re
from main_window import *
from new_object_dialog import *
from graphic_object import GraphicObject, Line, Point, WireFrame
from PyQt5.QtCore import *
from point import Point2D
from transform import scale_object, translate_object

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
        # x_window_min and y_window_min
        self.min = Point2D(0, 0)

        # x_window_max and y_window_max
        self.max = Point2D(600, 600)

        self.center = Point2D((self.min.get_x() + self.max.get_x()) / 2, (self.min.get_y() + self.max.get_y()) / 2)
        
    
    def set_handlers(self):

        # NEW OBJECT DIALOG:
        self.main_window.action_open_dialog.triggered.connect(self.open_dialog_handler)
        self.new_object_dialog.buttons_box.accepted.connect(self.new_object_dialog_submitted_handler)
        self.new_object_dialog.buttons_box.rejected.connect(self.new_object_dialog_cancelled_handler)

        # ZOOM:
        self.main_window.functions_menu.window_menu.zoom_in_button.clicked.connect(lambda : self.zoom_handler('in'))
        self.main_window.functions_menu.window_menu.zoom_out_button.clicked.connect(lambda : self.zoom_handler('out'))

        # DIRECTION:
        self.main_window.functions_menu.window_menu.left_button.clicked.connect(lambda: self.window_move_handler('left'))
        self.main_window.functions_menu.window_menu.right_button.clicked.connect(lambda: self.window_move_handler('right'))
        self.main_window.functions_menu.window_menu.up_button.clicked.connect(lambda: self.window_move_handler('up'))
        self.main_window.functions_menu.window_menu.down_button.clicked.connect(lambda: self.window_move_handler('down'))

        # SCROLL
        self.main_window.viewport.action_scroll_zoom_in.triggered.connect(lambda: self.zoom_handler('in'))
        self.main_window.viewport.action_scroll_zoom_out.triggered.connect(lambda: self.zoom_handler('out'))

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

        self.main_window.viewport.draw_objects(self.objects, self.min, self.max)

    def new_object_dialog_cancelled_handler(self):
        self.new_object_dialog.clear_inputs()
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

    def zoom_handler(self, direction: str):
        scale = 1.0
        if direction == 'in':
            scale = 0.5
        else:
            scale = 1.5
        scale_matrix = scale_object([self.min, self.max], self.center.get_x(), self.center.get_y(), scale, scale)
        self.min = scale_matrix[0]
        self.max = scale_matrix[1]
        self.main_window.viewport.draw_objects(self.objects, self.min, self.max)

    def window_move_handler(self, direction : str):
        dx = 0
        dy = 0
        if direction == 'left':
            dx = 0.9
        elif direction == 'right':
            dx = -0.9
        elif direction == 'up':
            dy = -0.9
        else:
            dy = 0.9
        scale_matrix = translate_object([self.min, self.max], dx, dy)
        self.min = scale_matrix[0]
        self.max = scale_matrix[1]
        self.main_window.viewport.draw_objects(self.objects, self.min, self.max)

# ====================== UTILITIES:        

    def parse_coordinates(self, coordinates_expr: str) -> list:
        tuples = re.findall(r"(\d+,\d+)", coordinates_expr)

        coordinates : list[Point2D] = []

        for t in tuples:
            coords = t.split(',')
            coordinates.append(Point2D(float(coords[0]), float(coords[1])))

        return coordinates

    def add_new_object(self, name: str, coordinates: list, type: str):
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
        self.main_window.log.add_log(f'[INFO] Objeto {name} do tipo {type}, cujas coordenadas são {[str(c) for c in coordinates]}, foi criado com sucesso!')

    def start(self):
        self.app.exec()