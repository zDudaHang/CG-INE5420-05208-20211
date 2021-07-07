from main_window import *
from new_object_dialog import *
from graphic_object import GraphicObject, Line, Point, WireFrame
from PyQt5.QtCore import *
from point import Point2D
from transform import generate_rotate_operation_matrix, generate_rotation_matrix, generate_scale_operation_matrix, generate_scaling_matrix, generate_translation_matrix, matrix_multiplication, scale_object, translate_object
from util import parse
from transform_dialog import RotateOptionsEnum, RotateTransformation, ScaleTransformation, TransformDialog, TranslateTransformation

class Controller():

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.step = 0.1 # 10%
        self.main_window = MainWindow(self.step)
        self.main_window.show()

        self.tranform_dialog = TransformDialog(self.main_window)

        self.new_object_dialog = NewObjectDialog(self.main_window)

        self.display_file : list[GraphicObject] = []

        self.set_window_values()
        self.set_handlers()

    def set_window_values(self):
        # x_window_min and y_window_min
        self.bottom_left = Point2D(0, 0)

        self.bottom_right = Point2D(600,0)
        self.top_left = Point2D(0,600)

        # x_window_max and y_window_max
        self.top_right = Point2D(600, 600)

        # TODO: Usar um sum para somar isso por iteracao
        cx = self.top_left.get_x() + self.top_right.get_x() + self.bottom_left.get_x() + self.bottom_right.get_x()
        cy = self.top_left.get_y() + self.top_right.get_y() + self.bottom_left.get_y() + self.bottom_right.get_y()

        self.center = Point2D(cx / 4, cy / 4)
        
    
    def set_handlers(self):

        # TRANSFORM DIALOG:
        self.main_window.functions_menu.object_list.action_edit_object.triggered.connect(self.on_edit_object)
        self.tranform_dialog.apply_transformations_button.clicked.connect(self.on_transform_dialog_submit)
        self.tranform_dialog.cancel_button.clicked.connect(self.on_transform_dialog_cancel)

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
        color = values[2]

        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

        if len(name) == 0:
            self.main_window.log.add_item("[ERRO] O nome não pode ser vazio!")
            return
        
        coordinates = self.parse_coordinates(coordinates_str)

        if (coordinates == None):
            self.main_window.log.add_item("[ERRO] As coordenadas passadas não respeitam o formato da aplicação. Por favor, utilize o seguinte formato para as coordenadas: (x1,y1),(x2,y2),...")
            return

        self.add_new_object(name, coordinates, type, color)

        self.main_window.viewport.draw_objects(self.display_file, self.bottom_left, self.top_right)

    def new_object_dialog_cancelled_handler(self, type: GraphicObjectEnum):
        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

    def on_edit_object(self):
        obj : GraphicObject = self.main_window.functions_menu.object_list.edit_object_state
        self.tranform_dialog.setWindowTitle(f'Aplicando transformações no objeto {obj.name}')
        self.tranform_dialog.exec()

    def on_transform_dialog_submit(self):
        print(f'Transformações no objeto: {self.main_window.functions_menu.object_list.edit_object_state.__str__()}')
        obj = self.main_window.functions_menu.object_list.edit_object_state

        matrix_t = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        for t in self.tranform_dialog.transformations:
            m = []
            if isinstance(t, ScaleTransformation):
                m = generate_scale_operation_matrix(obj.center.get_x(), obj.center.get_y(), t.sx, t.sy)
            elif isinstance(t, TranslateTransformation):
                m = generate_translation_matrix(t.dx, t.dy)
            elif isinstance(t, RotateTransformation):
                if (t.option == RotateOptionsEnum.WORLD):
                    m = generate_rotate_operation_matrix(self.center.get_x(), self.center.get_y(), t.angle)
                elif (t.option == RotateOptionsEnum.OBJECT):
                    m = generate_rotate_operation_matrix(obj.center.get_x(), obj.center.get_y(), t.angle)
                else: 
                    m = generate_rotate_operation_matrix(t.point.get_x(), t.point.get_y(), t.angle)
            matrix_t = matrix_multiplication(matrix_t, m)

        for i in range(0, len(obj.coordinates)):
            obj.coordinates[i].coordinates = matrix_multiplication(obj.coordinates[i].coordinates, matrix_t)
        index = self.display_file.index(obj)
        self.display_file[index] = obj
        self.main_window.viewport.draw_objects(self.display_file, self.bottom_left, self.top_right)
        self.tranform_dialog.clear()

    def on_transform_dialog_cancel(self):
        self.tranform_dialog.clear()
        self.tranform_dialog.close()

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

        self.main_window.viewport.draw_objects(self.display_file, self.bottom_left, self.top_right)

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

        self.main_window.viewport.draw_objects(self.display_file, self.bottom_left, self.top_right)

    def on_step_update(self, value: int):
        self.step += value
        self.main_window.functions_menu.window_menu.update_step_value(self.step)


# ====================== UTILITIES:

    def parse_coordinates(self, coordinates_expr: str) -> list:
        values = []
        try:
            values = parse(coordinates_expr)
        except IndexError:
            return None
        
        if values == None:
            return None
        
        coordinates : list[Point2D] = []

        for i in range(0, len(values)-1, 2):
            coordinates.append(Point2D(float(values[i]), float(values[i+1])))

        return coordinates

    def add_new_object(self, name: str, coordinates: list, type: GraphicObjectEnum, color: QColor):
        
        graphic_obj : GraphicObject = None

        try:
            if (type == GraphicObjectEnum.POINT):
                graphic_obj = Point(name, coordinates, color)
            if (type == GraphicObjectEnum.LINE):
                graphic_obj = Line(name, coordinates, color)
            if (type == GraphicObjectEnum.WIREFRAME):
                graphic_obj = WireFrame(name, coordinates, color)
        except ValueError as e:
            self.main_window.log.add_item(e.__str__())

        if graphic_obj != None:
            self.display_file.append(graphic_obj)        
            self.main_window.functions_menu.object_list.add_object(graphic_obj)
            self.main_window.log.add_item(f'[INFO] Objeto {graphic_obj.name} do tipo {graphic_obj.type.value}, cujas coordenadas são {[str(c) for c in graphic_obj.coordinates]}, foi criado com sucesso!')

    def start(self):
        self.app.exec()