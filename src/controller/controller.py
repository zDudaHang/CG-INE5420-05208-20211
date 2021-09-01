from src.model.enum.projection_enum import ProjectionEnum
from src.model.enum.RotateAxisOptionsEnum import RotateAxisOptionsEnum
import numpy
from src.model.enum.curve_enum import CurveEnum
from src.model.enum.line_clipping_options_enum import LineClippingOptionsEnum
from src.util.clipping.liang_barksy_clipper import LiagnBarksyClipper
from src.util.clipping.cohen_sutherland_clipper import CohenSutherlandLineClipper
from src.util.clipping.sutherland_hodgman import SutherlandHodgman

from src.util.clipping.point_clipper import PointClipper
from src.model.enum.graphic_object_form_enum import GraphicObjectFormEnum
from src.model.enum.coords_enum import CoordsEnum
from src.model.enum.display_file_enum import DisplayFileEnum
from typing import Dict, List,  Union
from typing import List, Union
from PyQt5.QtGui import QColor

from src.util.math import angle_between_vectors
from src.gui.main_window import *
from src.util.wavefront import WavefrontOBJ
from src.gui.new_object_dialog import NewObjectDialog, GraphicObjectEnum
from src.model.graphic_object import GraphicObject, Line, Object3D, Point, WireFrame, apply_matrix_in_object, calculate_center, create_graphic_object
from src.model.point import Point3D
from src.util.transform import generate_rotate_on_axis_matrix, generate_rotate_operation_matrix, generate_scale_operation_matrix, generate_scn_matrix, generate_translation_matrix, parallel_projection, perspective_projection, rotate_window, scale_window, translate_matrix_for_rotated_window, translate_object, translate_window
from src.util.parse import parse
from src.gui.transform_dialog import TransformDialog
from src.util.clipping.point_clipper import PointClipper

from numpy import dot, array
ORIGIN = Point3D(0,0,0)

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
            DisplayFileEnum.SCN_COORD: [],
            DisplayFileEnum.PROJ_COORD: []

        }

        self.add_test_objects()

        self.set_handlers()

    def add_test_objects(self):
        cubo1 : Object3D = Object3D('cubo1', [
            Point3D(0,0,0), Point3D(0,100,0), Point3D(100,100,0), Point3D(100,0,0), Point3D(0,0,100), Point3D(0,100,100), Point3D(100,100,100), Point3D(100,0,100)
            ],
            QColor(0,0,0), [
                (1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(2,6),(5,1),(3,7),(8,4)
            ]
        )

        cubo2 : Object3D = Object3D('cubo2', [
            Point3D(100,100,0), Point3D(200,100,0), Point3D(200,200,0), Point3D(100,200,0), Point3D(100,100,100), Point3D(200,100,100), Point3D(200,200,100), Point3D(100,200,100)
            ],
            QColor(0,0,0), [
                (0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)
            ]
        )

        self.display_file[DisplayFileEnum.WORLD_COORD].append(cubo1)
        self.display_file[DisplayFileEnum.WORLD_COORD].append(cubo2)

        self.calculate_scn_coordinates()
        

    def set_initial_values(self):
        # Zoom and move step:
        self.step = 0.1 # 10%

        # Rotation step:
        self.step_angle = 10 # (graus)

        self.focal_distance = 400

    def set_window_values(self):

        self.window_coordinates : List[Point3D] = [None, None, None, None]

        self.center = Point3D(0,0,0)

        self.window_height = 800
        self.window_width = 800

        self.window : WireFrame = WireFrame('_window_', self.update_window_coordinates(), None, False, False)
    
    def set_viewport_values(self):
        self.viewport_coordinates : List[Point3D] = [None, None, None, None]

        self.viewport_origin = Point3D(10,10)

        self.viewport_height = 400
        self.viewport_width = 400

        self.viewport_coordinates[CoordsEnum.TOP_LEFT] = self.viewport_origin + tuple([0, self.viewport_height])
        self.viewport_coordinates[CoordsEnum.TOP_RIGHT] = self.viewport_origin + tuple([self.viewport_width, self.viewport_height])

        self.viewport_coordinates[CoordsEnum.BOTTOM_LEFT] = self.viewport_origin
        self.viewport_coordinates[CoordsEnum.BOTTOM_RIGHT] = self.viewport_origin + tuple([self.viewport_width, 0])
        
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
        self.new_object_dialog.line_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.LINE))
        
        self.new_object_dialog.wireframe_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.WIREFRAME))
        self.new_object_dialog.wireframe_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.WIREFRAME))

        self.new_object_dialog.curve_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.CURVE))
        self.new_object_dialog.curve_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.CURVE))

        self.new_object_dialog.obj_3d_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.OBJECT_3D))
        self.new_object_dialog.obj_3d_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.OBJECT_3D))

        self.new_object_dialog.bicubic_tab.formLayout.buttons_box.accepted.connect(lambda: self.new_object_dialog_submitted_handler(GraphicObjectEnum.BICUBIC))
        self.new_object_dialog.bicubic_tab.formLayout.buttons_box.rejected.connect(lambda: self.new_object_dialog_cancelled_handler(GraphicObjectEnum.BICUBIC))

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
        self.main_window.functions_menu.window_menu.forward_button.clicked.connect(lambda: self.window_move_handler('forward'))
        self.main_window.functions_menu.window_menu.back_button.clicked.connect(lambda: self.window_move_handler('back'))

        # SCROLL
        self.main_window.viewport.action_scroll_zoom_in.triggered.connect(lambda: self.zoom_handler('in'))
        self.main_window.viewport.action_scroll_zoom_out.triggered.connect(lambda: self.zoom_handler('out'))

        # IMPORT/EXPORT OBJ FILE
        self.main_window.add_new_obj_action.triggered.connect(lambda: self.import_handler())
        self.main_window.export_new_obj_action.triggered.connect(lambda: self.export_handler())

        # LINE CLIPPING
        self.main_window.functions_menu.clipping_updated_action.triggered.connect(self.clip)

        # PROJECTION
        self.main_window.functions_menu.proj_updated_action.triggered.connect(self.calculate_scn_coordinates)

# ====================== HANDLERS:

# ========== IMPORT & EXPORT .OBJ FILES

    def import_handler(self):
        objs : Dict[str, List[Point3D]]= self.main_window.new_objs
        i = 0

        for key, value in objs.objects.items():
            list_points = [Point3D(c[0],c[1]) for c in value]

            usemtl = objs.usemtl[i]
            newmtl = objs.new_mtl.index(usemtl)

            rgb = [round(int(float(i) * 255)) for i in objs.kd_params[newmtl]]  

            if len(list_points) == 1:
                self.add_new_object(key, list_points, GraphicObjectEnum.POINT, QColor(rgb[0],rgb[1],rgb[2]), objs.filled[i])
            elif len(list_points) == 2:
                self.add_new_object(key, list_points, GraphicObjectEnum.LINE, QColor(rgb[0],rgb[1],rgb[2]), objs.filled[i])
            else:
                self.add_new_object(key, list_points, GraphicObjectEnum.WIREFRAME, QColor(rgb[0],rgb[1],rgb[2]), objs.filled[i])
            i += 1
        
        self.update_window_values(objs.window)

        self.calculate_scn_coordinates()

        # self.draw_objects()
           
    def export_handler(self):
        WavefrontOBJ.save_obj(self.display_file[DisplayFileEnum.WORLD_COORD], self.center, Point3D(self.window_width, self.window_height))

# ========== UPDATE WINDOW VALUES

    def update_window_coordinates(self):
        window_coordinates : List[Point3D] = [None, None, None, None]

        window_coordinates[CoordsEnum.TOP_LEFT] = self.center + tuple([-self.window_width, self.window_height])
        window_coordinates[CoordsEnum.TOP_RIGHT] = self.center + tuple([self.window_width, self.window_height])

        window_coordinates[CoordsEnum.BOTTOM_LEFT] = self.center + tuple([-self.window_width, -self.window_height])
        window_coordinates[CoordsEnum.BOTTOM_RIGHT] = self.center + tuple([self.window_width, -self.window_height])

        return window_coordinates

    def update_window_values(self, window_obj_file: List[List[float]]):
        window_center = window_obj_file[0]
        window_dimensions = window_obj_file[1]

        self.center = Point3D(window_center[0], window_center[1])

        self.window_width = window_dimensions[0]
        self.window_height = window_dimensions[1]

        self.update_window_coordinates()

# ========== NEW OBJECT DIALOG

    def new_object_dialog_submitted_handler(self, type: GraphicObjectEnum):
        values = self.new_object_dialog.get_values(type)
        name = values[GraphicObjectFormEnum.NAME]
        coordinates_str = values[GraphicObjectFormEnum.COORDINATES]

        if len(name) == 0:
            self.main_window.log.add_item("[ERRO] O nome não pode ser vazio!")
            return
        
        coordinates = self.parse_coordinates(coordinates_str)

        if coordinates == None:
            self.main_window.log.add_item("[ERRO] As coordenadas passadas não respeitam o formato da aplicação. Por favor, utilize o seguinte formato para as coordenadas: (x1,y1,z1),(x2,y2,z2),...")
            return
        
        color = None
        if GraphicObjectFormEnum.COLOR in values:
            color = values[GraphicObjectFormEnum.COLOR]
        
        is_filled = False

        if GraphicObjectFormEnum.FILLED in values:
            is_filled = values[GraphicObjectFormEnum.FILLED]

        curve_option = None
        if GraphicObjectFormEnum.CURVE_OPTION in values:
            curve_option = values[GraphicObjectFormEnum.CURVE_OPTION]

        edges = None
        if GraphicObjectFormEnum.EDGES in values:
            text = values[GraphicObjectFormEnum.EDGES]
            text += ','
            edges : List[tuple] = list(eval(text))

        faces = None
        if GraphicObjectFormEnum.FACES in values:
            text = values[GraphicObjectFormEnum.FACES]
            if text != '':
                text += ','
                faces : List[tuple] = list(eval(text))
        
        self.new_object_dialog.clear_inputs(type)
        self.new_object_dialog.close()

        self.add_new_object(name, coordinates, type, color, is_filled, False, curve_option, edges, faces)

        self.calculate_scn_coordinates()

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
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        for t in self.tranform_dialog.transformations:               
            matrix_t = dot(matrix_t, t.generate_matrix(obj, self.calculate_angle_vup_y_axis(), self.window.center))

        for i in range(0, len(obj.coordinates)):
            obj.coordinates[i].coordinates = dot(obj.coordinates[i].coordinates, matrix_t)
        
        obj.center = calculate_center(obj.coordinates)
        
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
        
        s = generate_scale_operation_matrix(self.window.center, scale, scale, 1)

        self.window = apply_matrix_in_object(self.window, s)

        # The center doesn't change when we scale the window, so we don't need to update it. But, the height and width will change, so we need to update them.
        self.window_height *= scale
        self.window_width *= scale

        self.main_window.log.add_item(f'[DEBUG] Dando zoom a window em {round(scale * 100, 2)}%. Novas medidas da window: (largura={round(self.window_width, 2)}, altura={round(self.window_height, 2)})')

        self.calculate_scn_coordinates()

    def window_move_handler(self, direction: str):
        dx = 0
        dy = 0
        dz = 0

        if direction == 'left':
            dx = -self.step
        elif direction == 'right':
            dx = self.step
        elif direction == 'up':
            dy = self.step
        elif direction == 'down':
            dy = -self.step
        elif direction == 'forward':
            dz = self.step
        else:
            dz = -self.step
        
        dx = dx * self.window_width
        dy = dy * self.window_height
        dz = dz * 100

        t = translate_matrix_for_rotated_window(Point3D(dx, dy, dz), self.calculate_angle_vup_y_axis(), self.window.center)

        self.window = apply_matrix_in_object(self.window, t)

        self.main_window.log.add_item(f'[DEBUG] Movimentando a window em {round(dx, 2)} unidades em x, {round(dy, 2)} em y e {round(dz, 2)} em z. Novo centro da window: {self.window.center}')

        self.calculate_scn_coordinates()

    def window_rotate_handler(self, direction: str):
        angle = 0
        
        if direction == 'left':
            angle = -self.step_angle

        else:
            angle = self.step_angle

        axis = self.main_window.functions_menu.window_menu.rotation_axis
        
        r = generate_rotate_on_axis_matrix(self.window.center, angle, axis)

        self.window = apply_matrix_in_object(self.window, r)

        self.calculate_scn_coordinates()

    def on_step_update(self, value: float):
        self.step += value
        self.main_window.functions_menu.window_menu.update_step_value(self.step)

    def on_step_rotation_update(self, value: float):
        self.step_angle += value
        self.main_window.functions_menu.window_menu.update_step_rotation_value(self.step_angle)

# ====================== UTILITIES:

    def draw_objects(self):
        self.main_window.viewport.draw_objects(self.clip())

    def scn_matrix(self) -> List[List[float]]:
        return generate_scn_matrix(self.window.center, self.window_height, self.window_width, self.calculate_angle_vup_y_axis())

    def calculate_angle_vup_y_axis(self) -> float:
        translated = False
        distance = self.window.center

        # Primeiro precisamos transladar a window para a origem para o calculo funcionar corretamente
        if self.window.center != ORIGIN:
            translated = True
            t = generate_translation_matrix(-self.window.center.x(), -self.window.center.y())
            self.window = apply_matrix_in_object(self.window, t)
        
        center_TL_TR = calculate_center([self.window.coordinates[CoordsEnum.TOP_LEFT], self.window.coordinates[CoordsEnum.TOP_RIGHT]])

        v_up = array([center_TL_TR.x(), center_TL_TR.y()])
        y = array([0, 1])

        angle = angle_between_vectors(v_up, y)

        # Desloca para onde estava anteriormente antes de criar a matriz SCN
        if translated:
            t = generate_translation_matrix(distance.x(), distance.y())
            self.window = apply_matrix_in_object(self.window, t)

        return angle

    def calculate_scn_coordinates(self):
        
        self.display_file[DisplayFileEnum.SCN_COORD].clear()
        self.display_file[DisplayFileEnum.PROJ_COORD].clear()

        proj = self.main_window.functions_menu.proj_method

        transform = array([])

        if proj == ProjectionEnum.PARALLEL:
            transform = parallel_projection(self.window)
        else:
            transform = perspective_projection(self.window, self.focal_distance)

        for obj in self.display_file[DisplayFileEnum.WORLD_COORD]: 
            if obj.type == GraphicObjectEnum.OBJECT_3D:
                new_obj = apply_matrix_in_object(obj, transform)
                self.display_file[DisplayFileEnum.PROJ_COORD].append(new_obj)
            else:
                self.display_file[DisplayFileEnum.PROJ_COORD].append(obj)

        scn = self.scn_matrix()

        for obj in self.display_file[DisplayFileEnum.PROJ_COORD]:
            self.display_file[DisplayFileEnum.SCN_COORD].append(apply_matrix_in_object(obj,scn))
        
        self.draw_objects()

    def clip(self) -> List[GraphicObject]:
        clipping_line_method = self.main_window.functions_menu.clipping_method

        inside_window_objs : List[GraphicObject] = []

        for obj in self.display_file[DisplayFileEnum.SCN_COORD]:
            if isinstance(obj, Point):
                if PointClipper.clip(obj.coordinates[0]): 
                    inside_window_objs.append(obj)
            elif isinstance(obj, Line):
                new_line = None

                if clipping_line_method == LineClippingOptionsEnum.LIANG_B:
                    new_line = LiagnBarksyClipper(obj).clip()
                else:
                    new_line = CohenSutherlandLineClipper(obj).cohenSutherlandClip()
                
                if new_line != None:
                    inside_window_objs.append(new_line)
            elif isinstance(obj, WireFrame):
                new_wireframe = SutherlandHodgman(obj).sutherland_hodgman_clip()
                
                if new_wireframe != None:
                    inside_window_objs.append(new_wireframe)         
            elif isinstance(obj, Object3D):
                if len(obj.edges_lines) != 0:
                    for line in obj.edges_lines:
                        if clipping_line_method == LineClippingOptionsEnum.LIANG_B:
                            new_line = LiagnBarksyClipper(line).clip()
                        else:
                            new_line = CohenSutherlandLineClipper(line).cohenSutherlandClip()
                        
                        if new_line != None:
                            inside_window_objs.append(new_line)
                else:
                    for wireframe in obj.faces_wireframes:
                        new_wireframe = SutherlandHodgman(wireframe).sutherland_hodgman_clip()
                    
                        if new_wireframe != None:
                            inside_window_objs.append(new_wireframe)
            else: inside_window_objs.append(obj)
        
        return inside_window_objs
    
    def parse_coordinates(self, coordinates_expr: str) -> Union[List[Point3D],None]:
        return parse(coordinates_expr)

    def add_new_object(self, name: str, coordinates: list, type: GraphicObjectEnum, color: QColor, is_filled: bool = False, is_clipped: bool = False, curve_option: CurveEnum = None, edges : List[tuple] = None, faces : List[tuple] = None):
        graphic_obj : GraphicObject = create_graphic_object(type, name, coordinates, color, is_filled, is_clipped, curve_option, edges, faces, self.main_window.log.add_item)

        if graphic_obj != None:
            self.add_object_to_display_file(graphic_obj)
            self.main_window.functions_menu.object_list.add_object(graphic_obj)
            self.main_window.log.add_item(f'[INFO] Objeto {graphic_obj.name} do tipo {graphic_obj.type.value}, cujas coordenadas são {[str(c) for c in graphic_obj.coordinates]}, foi criado com sucesso!')
    
    def add_object_to_display_file(self, obj: GraphicObject):
        self.display_file[DisplayFileEnum.WORLD_COORD].append(obj)
        self.display_file[DisplayFileEnum.SCN_COORD].append(apply_matrix_in_object(obj, self.scn_matrix()))

    def start(self):
        self.app.exec()