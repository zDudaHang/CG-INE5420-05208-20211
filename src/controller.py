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
        self.step = 0.1 # 10%
        self.main_window = MainWindow(self.step)
        self.main_window.show()

        self.new_object_dialog = NewObjectDialog(self.main_window)
        self.display_file : list[GraphicObject] = []

        self.set_window_values()
        self.set_handlers()

    def set_window_values(self):
        # x_window_min and y_window_min
        self.top_left = Point2D(0, 0)

        self.top_right = Point2D(600,0)
        self.bottom_left = Point2D(0,600)

        # x_window_max and y_window_max
        self.bottom_right = Point2D(600, 600)

        cx = self.top_left.get_x() + self.top_right.get_x() + self.bottom_left.get_x() + self.bottom_right.get_x()
        cy = self.top_left.get_y() + self.top_right.get_y() + self.bottom_left.get_y() + self.bottom_right.get_y()

        self.center = Point2D(cx / 4, cy / 4)
        
    
    def set_handlers(self):

        # NEW OBJECT DIALOG:
        self.main_window.action_open_dialog.triggered.connect(self.open_dialog_handler)
        self.new_object_dialog.point_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.POINT))
        self.new_object_dialog.point_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.POINT))

        self.new_object_dialog.line_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.LINE))
        self.new_object_dialog.point_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.LINE))
        
        self.new_object_dialog.wireframe_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.WIREFRAME))
        self.new_object_dialog.point_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.WIREFRAME))

        # STEP:
        self.main_window.functions_menu.window_menu.step_plus_button.clicked.connect(lambda: self.on_step_update(0.05))
        self.main_window.functions_menu.window_menu.step_minus_button.clicked.connect(lambda: self.on_step_update(-0.05))

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
    
    def new_object_dialog_submitted_handler(self, type: GraphicObjectEnum):
        values = self.new_object_dialog.get_values(type)
        name = values[0]
        coordinates_str = values[1]

        if len(name) == 0:
            self.main_window.log.add_log("[ERRO] O nome não pode ser vazio!")
            return
        
        coordinates = self.parse_coordinates(coordinates_str)

        if (coordinates == None):
            self.main_window.log.add_log("[ERRO] O nome não pode ser vazio!")
            return

        self.add_new_object(name, coordinates, type)

        self.main_window.viewport.draw_objects(self.display_file, self.top_left, self.bottom_right)

    def new_object_dialog_cancelled_handler(self, type: GraphicObjectEnum):
        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

    def zoom_handler(self, direction: str):
        scale = 1.0
        if direction == 'in':
            scale = 1 - self.step
        else:
            scale = 1 + self.step
        matrix = scale_object([self.top_left, self.top_right, self.bottom_left, self.bottom_right], self.center.get_x(), self.center.get_y(), scale, scale)
        
        self.top_left = matrix[0]
        self.top_right = matrix[1]
        self.bottom_left = matrix[2]
        self.bottom_right = matrix[3]

        self.main_window.viewport.draw_objects(self.display_file, self.top_left, self.bottom_right)

    def window_move_handler(self, direction : str):
        dx = 0
        dy = 0
        if direction == 'left':
            dx = 5 + self.step
        elif direction == 'right':
            dx = -(5 + self.step)
        elif direction == 'up':
            dy = - (5 + self.step)
        else:
            dy = 5 + self.step
        matrix = translate_object([self.top_left, self.top_right, self.bottom_left, self.bottom_right], dx, dy)
        
        self.top_left = matrix[0]
        self.top_right = matrix[1]
        self.bottom_left = matrix[2]
        self.bottom_right = matrix[3]

        self.main_window.viewport.draw_objects(self.display_file, self.top_left, self.bottom_right)

    def on_step_update(self, value: int):
        self.step += value
        self.main_window.functions_menu.window_menu.update_step_value(self.step)


# ====================== UTILITIES:        

    def parse_coordinates(self, coordinates_expr: str) -> list:
        values = []
        number = ''
        i = 0
        while i < len(coordinates_expr) - 1:
            if coordinates_expr[i] == '(':
                i += 1
                if (coordinates_expr[i] == '-'):
                    number += coordinates_expr[i]
                    i += 1
                while (coordinates_expr[i] != ','):
                    if (coordinates_expr[i].isnumeric() or coordinates_expr[i] == '.'):
                        number += coordinates_expr[i]
                        i += 1
                        if (coordinates_expr[i] == ','): 
                            continue
                    else: 
                        return None

                i += 1
                values.append(number)
                number = ''

                if (coordinates_expr[i] == '-'):
                    number += coordinates_expr[i]
                    i += 1
                while (coordinates_expr[i] != ')'):
                    if (coordinates_expr[i].isnumeric() or coordinates_expr[i] == '.'):
                        number += coordinates_expr[i]
                        i += 1
                        if (coordinates_expr[i] == ')'): 
                            continue
                    else: 
                        return None
                
                values.append(number)
                number = ''

                if (i == len(coordinates_expr) - 1):
                    break
                i += 1
                if (coordinates_expr[i] == ','):
                    i += 1
                    continue
            else: 
                return None

        coordinates : list[Point2D] = []

        for i in range(0, len(values)-1, 2):
            coordinates.append(Point2D(float(values[i]), float(values[i+1])))

        return coordinates

    def add_new_object(self, name: str, coordinates: list, type: GraphicObjectEnum):
        
        graphic_obj : GraphicObject = None

        try:
            if (type == GraphicObjectEnum.POINT):
                graphic_obj = Point(name, coordinates)
            if (type == GraphicObjectEnum.LINE):
                graphic_obj = Line(name, coordinates)
            if (type == GraphicObjectEnum.WIREFRAME):
                graphic_obj = WireFrame(name, coordinates)
        except ValueError as e:
            self.main_window.log.add_log(e.__str__())

        if graphic_obj != None:
            self.display_file.append(graphic_obj)
            self.main_window.functions_menu.object_list.add_object(graphic_obj)
        self.main_window.log.add_log(f'[INFO] Objeto {name} do tipo {type.value}, cujas coordenadas são {[str(c) for c in coordinates]}, foi criado com sucesso!')

    def start(self):
        self.app.exec()