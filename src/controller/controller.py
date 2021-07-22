from src.util.clipping.liang_barksy_clipper import LiagnBarksyClipper
from src.util.clipping.point_clipper import PointClipper
from src.model.enum.graphic_object_form_enum import GraphicObjectFormEnum
from src.model.enum.coords_enum import CoordsEnum
from src.model.enum.display_file_enum import DisplayFileEnum
from typing import Dict, List,  Union
from typing import List, Union
from PyQt5.QtGui import QColor

from src.util.math import matrix_multiplication
from src.gui.main_window import *
from src.util.wavefront import WavefrontOBJ
from src.gui.new_object_dialog import NewObjectDialog, GraphicObjectEnum
from src.model.graphic_object import GraphicObject, Line, Point, apply_matrix_in_object, calculate_center, create_graphic_object
from src.model.point import Point2D
from src.util.transform import generate_rotate_operation_matrix, generate_scale_operation_matrix, generate_scn_matrix, scale_window, translate_matrix_for_rotated_window, translate_window
from src.util.parse import parse
from src.gui.transform_dialog import RotateOptionsEnum, RotateTransformation, ScaleTransformation, TransformDialog, TranslateTransformation
from src.util.clipping.point_clipper import PointClipper

class Controller():

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.set_initial_values()

        self.set_window_values()
        self.set_viewport_values()

        self.main_window = MainWindow(self.step, self.step_angle, self.viewport_coordinates, self.viewport_width, self.viewport_height, self.viewport_origin)
        self.main_window.show()

        self.tranform_dialog = TransformDialog(self.main_window)

        self.new_object_dialog = NewObjectDialog(self.main_window)

        self.display_file : Dict[DisplayFileEnum, List[GraphicObject]] = {
            DisplayFileEnum.WORLD_COORD: [], 
            DisplayFileEnum.SCN_COORD: []
        }

        self.set_handlers()

    def set_initial_values(self):
        # Zoom and move step:
        self.step = 0.1 # 10%

        # Rotation step:
        self.step_angle = 10 # (graus)
        
        # Angle between Y_world and window v_up
        self.angle = 0

    def set_window_values(self):

        self.window_coordinates : List[Point2D] = [None, None, None, None]

        self.window_origin = Point2D(0,0)

        self.window_height = 400
        self.window_width = 600

        self.update_window_coordinates()

        self.center = calculate_center(self.window_coordinates)
    
    def set_viewport_values(self):
        self.viewport_coordinates : List[Point2D] = [None, None, None, None]

        self.viewport_origin = Point2D(10,10)

        self.viewport_width = 400
        self.viewport_height = 400

        self.viewport_coordinates[CoordsEnum.TOP_LEFT] = Point2D(10, 410)
        self.viewport_coordinates[CoordsEnum.TOP_RIGHT] = Point2D(410, 410)

        self.viewport_coordinates[CoordsEnum.BOTTOM_LEFT] = Point2D(10, 10)
        self.viewport_coordinates[CoordsEnum.BOTTOM_RIGHT] = Point2D(410, 10)
        
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

        # STEP ZOOM:
        self.main_window.functions_menu.window_menu.step_plus_button.clicked.connect(lambda: self.on_step_update(0.05))
        self.main_window.functions_menu.window_menu.step_minus_button.clicked.connect(lambda: self.on_step_update(-0.05))

        # ZOOM:
        self.main_window.functions_menu.window_menu.zoom_in_button.clicked.connect(lambda : self.zoom_handler('in'))
        self.main_window.functions_menu.window_menu.zoom_out_button.clicked.connect(lambda : self.zoom_handler('out'))

        # STEP ROTATION:
        self.main_window.functions_menu.window_menu.rotation_step_plus_button.clicked.connect(lambda: self.on_step_rotation_update(5))
        self.main_window.functions_menu.window_menu.rotation_step_minus_button.clicked.connect(lambda: self.on_step_rotation_update(-5))

        # ROTATION:
        self.main_window.functions_menu.window_menu.rotate_left_button.clicked.connect(lambda: self.window_rotate_handler('left'))
        self.main_window.functions_menu.window_menu.rotate_right_button.clicked.connect(lambda: self.window_rotate_handler('right'))

        # DIRECTION:
        self.main_window.functions_menu.window_menu.left_button.clicked.connect(lambda: self.window_move_handler('left'))
        self.main_window.functions_menu.window_menu.right_button.clicked.connect(lambda: self.window_move_handler('right'))
        self.main_window.functions_menu.window_menu.up_button.clicked.connect(lambda: self.window_move_handler('up'))
        self.main_window.functions_menu.window_menu.down_button.clicked.connect(lambda: self.window_move_handler('down'))

        # SCROLL
        self.main_window.viewport.action_scroll_zoom_in.triggered.connect(lambda: self.zoom_handler('in'))
        self.main_window.viewport.action_scroll_zoom_out.triggered.connect(lambda: self.zoom_handler('out'))

        # IMPORT/EXPORT OBJ FILE
        self.main_window.add_new_obj_action.triggered.connect(lambda: self.import_handler())
        self.main_window.export_new_obj_action.triggered.connect(lambda: self.export_handler())

# ====================== HANDLERS:

# ========== IMPORT & EXPORT .OBJ FILES

    def import_handler(self):
        objs : Dict[str, List[Point2D]]= self.main_window.new_objs
        i = 0

        for key, value in objs.objects.items():
            list_points = [Point2D(c[0],c[1]) for c in value]

            usemtl = objs.usemtl[i]
            newmtl = objs.new_mtl.index(usemtl)

            rgb = [round(int(float(i) * 255)) for i in objs.kd_params[newmtl]]  

            if len(list_points) == 1:
                self.add_new_object(key, list_points, GraphicObjectEnum.POINT, QColor(rgb[0],rgb[1],rgb[2]))
            elif len(list_points) == 2:
                self.add_new_object(key, list_points, GraphicObjectEnum.LINE, QColor(rgb[0],rgb[1],rgb[2]))
            else:
                self.add_new_object(key, list_points, GraphicObjectEnum.WIREFRAME, QColor(rgb[0],rgb[1],rgb[2]))
            i += 1
        
        self.update_window_values(objs.window)

        self.calculate_scn_coordinates()

        self.draw_objects()
           
    def export_handler(self):
        WavefrontOBJ.save_obj(self.display_file[DisplayFileEnum.WORLD_COORD], self.center, Point2D(self.window_width, self.window_height))

# ========== UPDATE WINDOW VALUES

    def update_window_coordinates(self):
        self.window_coordinates[CoordsEnum.TOP_LEFT] = self.window_origin + tuple([0, self.window_height])
        self.window_coordinates[CoordsEnum.TOP_RIGHT] = self.window_origin + tuple([self.window_width, self.window_height])

        self.window_coordinates[CoordsEnum.BOTTOM_LEFT] = self.window_origin
        self.window_coordinates[CoordsEnum.BOTTOM_RIGHT] = self.window_origin + tuple([self.window_width, 0])

    def update_window_values(self, window_obj_file: List[List[float]]):
        window_center = window_obj_file[0]
        window_dimensions = window_obj_file[1]

        self.center = Point2D(window_center[0], window_center[1])

        self.window_width = window_dimensions[0]
        self.window_height = window_dimensions[1]

        self.update_window_coordinates()

# ========== NEW OBJECT DIALOG

    def new_object_dialog_submitted_handler(self, type: GraphicObjectEnum):
        values = self.new_object_dialog.get_values(type)
        name = values[GraphicObjectFormEnum.NAME]
        coordinates_str = values[GraphicObjectFormEnum.COORDINATES]
        color = values[GraphicObjectFormEnum.COLOR]

        is_filled = False
        if GraphicObjectFormEnum.FILLED in values:
            is_filled = values[GraphicObjectFormEnum.FILLED]

        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

        if len(name) == 0:
            self.main_window.log.add_item("[ERRO] O nome não pode ser vazio!")
            return
        
        coordinates = self.parse_coordinates(coordinates_str)

        if coordinates == None:
            self.main_window.log.add_item("[ERRO] As coordenadas passadas não respeitam o formato da aplicação. Por favor, utilize o seguinte formato para as coordenadas: (x1,y1),(x2,y2),...")
            return

        self.add_new_object(name, coordinates, type, color, is_filled)

        self.draw_objects()

    def new_object_dialog_cancelled_handler(self, type: GraphicObjectEnum):
        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

    def open_dialog_handler(self):
        self.new_object_dialog.exec()

# ========== TRANSFORM OBJECT DIALOG:

    def on_edit_object(self):
        obj : GraphicObject = self.main_window.functions_menu.object_list.edit_object_state
        self.tranform_dialog.setWindowTitle(f'Aplicando transformações no objeto {obj.name}')
        self.tranform_dialog.exec()

    def on_transform_dialog_submit(self):
        obj = self.main_window.functions_menu.object_list.edit_object_state

        matrix_t = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        for t in self.tranform_dialog.transformations:
            m = []
            
            if isinstance(t, ScaleTransformation):
                m = generate_scale_operation_matrix(obj.center.x(), obj.center.y(), t.sx, t.sy)
            
            elif isinstance(t, TranslateTransformation):
                m = translate_matrix_for_rotated_window(t.dx, t.dy, self.angle, self.center.x(), self.center.y())
            
            elif isinstance(t, RotateTransformation):

                if t.option == RotateOptionsEnum.WORLD:
                    m = generate_rotate_operation_matrix(self.center.x(), self.center.y(), t.angle)
                
                elif t.option == RotateOptionsEnum.OBJECT:
                    m = generate_rotate_operation_matrix(obj.center.x(), obj.center.y(), t.angle)
                
                else: 
                    m = generate_rotate_operation_matrix(t.point.x(), t.point.y(), t.angle)
                
            matrix_t = matrix_multiplication(matrix_t, m)

        for i in range(0, len(obj.coordinates)):
            obj.coordinates[i].coordinates = matrix_multiplication(obj.coordinates[i].coordinates, matrix_t)
        

        index = self.display_file[DisplayFileEnum.WORLD_COORD].index(obj)
        self.display_file[DisplayFileEnum.WORLD_COORD][index] = obj

        self.calculate_scn_coordinates()

        self.tranform_dialog.clear()

    def on_transform_dialog_cancel(self):
        self.tranform_dialog.clear()
        self.tranform_dialog.close()

# ========== WINDOW MENU HANDLERS:

    def zoom_handler(self, direction: str):
        scale = 1.0
        
        if direction == 'in':
            scale = 1 - self.step
        else:
            scale = 1 + self.step
        
        matrix = scale_window(self.window_coordinates, self.center.x(), self.center.y(), scale, scale)

        # The center doesn't change when we scale the window, so we don't need to update it. But, the height and width will change, so we need to update them.
        self.window_height = matrix[CoordsEnum.TOP_RIGHT].y() - matrix[CoordsEnum.BOTTOM_RIGHT].y()
        self.window_width = matrix[CoordsEnum.TOP_RIGHT].x() - matrix[CoordsEnum.TOP_LEFT].x()

        self.main_window.log.add_item(f'[DEBUG] Dando zoom a window em {scale * 100}%. Novas medidas da window: (largura={self.window_width}, altura={self.window_height}')

        self.calculate_scn_coordinates()

    def window_move_handler(self, direction: str):
        dx = 0
        dy = 0

        if direction == 'left':
            dx = -self.step
        elif direction == 'right':
            dx = self.step
        elif direction == 'up':
            dy = self.step
        else:
            dy = -self.step
        
        dx = dx * self.window_width
        dy = dy * self.window_height

        matrix = translate_window(self.window_coordinates, dx, dy, self.angle, self.center.x(), self.center.y())

        # The center changes when we move the window, so we need to update this to reflect in scn transformation
        self.center = calculate_center(matrix)
        self.window_origin = Point2D(self.window_origin.x() + dx, self.window_origin.y() + dy)

        self.main_window.log.add_item(f'[DEBUG] Movimentando a window em {dx * self.window_width} unidades em x e {dy * self.window_height} em y. Novo centro da window: {self.center}')

        self.calculate_scn_coordinates()

    def window_rotate_handler(self, direction: str):
        angle = 0

        if direction == 'left':
            angle = -self.step_angle

        else:
            angle = self.step_angle

        self.angle += angle

        self.main_window.log.add_item(f'[DEBUG] Rotacionando a window em {angle} graus. Ângulo entre v_up e Y_mundo = {self.angle}')

        self.calculate_scn_coordinates()

    def on_step_update(self, value: float):
        self.step += value
        self.main_window.functions_menu.window_menu.update_step_value(self.step)

    # TODO: Se o valor for positivo, usar mod 360 para ficar entre 0 e 360. O mesmo para o negativo
    def on_step_rotation_update(self, value: float):
        self.step_angle += value
        self.main_window.functions_menu.window_menu.update_step_rotation_value(self.step_angle)

# ====================== UTILITIES:

    def draw_objects(self):
        self.main_window.viewport.draw_objects(self.clip())

    def scn_matrix(self) -> List[List[float]]:
        return generate_scn_matrix(self.center.x(), self.center.y(), self.window_height, self.window_width, self.angle)

    def calculate_scn_coordinates(self):

        self.display_file[DisplayFileEnum.SCN_COORD].clear()

        scn = self.scn_matrix()

        for obj in self.display_file[DisplayFileEnum.WORLD_COORD]:
            self.display_file[DisplayFileEnum.SCN_COORD].append(apply_matrix_in_object(obj,scn))
        
        self.draw_objects()

    def clip(self) -> List[GraphicObject]:
        inside_window_objs : List[GraphicObject] = []

        for obj in self.display_file[DisplayFileEnum.SCN_COORD]:
            if isinstance(obj, Point):
                if PointClipper.clip(obj.coordinates[0]): 
                    inside_window_objs.append(obj)
            elif isinstance(obj, Line):
                new_line = LiagnBarksyClipper(obj).clip()

                if new_line != None:
                    inside_window_objs.append(new_line)
                
            else: inside_window_objs.append(obj)

        return inside_window_objs
    
    def parse_coordinates(self, coordinates_expr: str) -> Union[List[Point2D],None]:
        return parse(coordinates_expr)

    def add_new_object(self, name: str, coordinates: list, type: GraphicObjectEnum, color: QColor, is_filled: bool):
        
        graphic_obj : GraphicObject = create_graphic_object(type, name, coordinates, color, is_filled, self.main_window.log.add_item)

        if graphic_obj != None:
            self.add_object_to_display_file(graphic_obj)
            self.main_window.functions_menu.object_list.add_object(graphic_obj)
            self.main_window.log.add_item(f'[INFO] Objeto {graphic_obj.name} do tipo {graphic_obj.type.value}, cujas coordenadas são {[str(c) for c in graphic_obj.coordinates]}, foi criado com sucesso!')
    
    def add_object_to_display_file(self, obj: GraphicObject):
        self.display_file[DisplayFileEnum.WORLD_COORD].append(obj)
        # Nossa window eh egocentrica, quer que todos os objetos girem do jeito que ela estah
        self.display_file[DisplayFileEnum.SCN_COORD].append(apply_matrix_in_object(obj, self.scn_matrix()))

    def start(self):
        self.app.exec()