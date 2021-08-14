from src.util.math import concat_transformation_matrixes
from src.model.graphic_object import GraphicObject, Line, apply_matrix_in_object, apply_matrix_in_point, calculate_center
from src.util.transform import generate_rotate_operation_matrix, generate_rx_rotation_matrix, generate_ry_rotation_matrix, generate_rz_rotation_matrix, generate_scale_operation_matrix, generate_translation_matrix, translate_matrix_for_rotated_window
from src.model.enum.RotateAxisOptionsEnum import RotateAxisOptionsEnum
from src.model.enum.rotate_options_enum import RotateOptionsEnum
from PyQt5.QtWidgets import QButtonGroup, QComboBox, QDialog, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QTabWidget, QVBoxLayout, QLineEdit, QWidget
from typing import Callable, List, Union

from src.util.parse import parse
from src.model.point import Point3D
from src.gui.log import Log

from abc import ABC, abstractmethod
from numpy import array, degrees, linalg, arctan

class Transformation(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate_matrix(self, obj: GraphicObject, v_up_angle: float, window_center: Point3D) -> array:
        pass

class RotateTransformation(Transformation):
    def __init__(self, option: RotateOptionsEnum, angle: float, point: Point3D = None, axis_option = RotateAxisOptionsEnum, axis : Point3D = None):
        self.option = option
        self.angle = angle
        self.point = point
        self.axis_option = axis_option
        self.axis = axis

    def __str__(self) -> str:
        if self.option == RotateOptionsEnum.POINT:
            return f'Rotacionar em torno do ponto {self.point.__str__()} em {self.angle} graus'
        elif self.option == RotateOptionsEnum.AXIS:
            if self.axis_option == RotateAxisOptionsEnum.ARBITRARY:
                return f'Rotacionar em torno de um eixo arbitrário A= {self.axis.__str__()} com P={self.point.__str__()} em {self.angle} graus'
            else:
                return f'Rotacionar em torno do eixo {RotateAxisOptionsEnum._to_str(self.axis_option)} em {self.angle} graus'
        return f'{self.option.value} em {self.angle} graus'

    def generate_matrix(self, obj: GraphicObject, v_up_angle: float, window_center: Point3D) -> array:
        if self.option == RotateOptionsEnum.WORLD:
            return generate_rotate_operation_matrix(Point3D(0,0,0), self.angle)
        
        elif self.option == RotateOptionsEnum.OBJECT:
            return generate_rotate_operation_matrix(obj.center, self.angle)
        
        elif self.option == RotateOptionsEnum.POINT:
            return generate_rotate_operation_matrix(self.point, self.angle)
        else:
            if self.axis_option == RotateAxisOptionsEnum.X:
                return generate_rx_rotation_matrix(self.angle)
            
            elif self.axis_option == RotateAxisOptionsEnum.Y:
                return generate_ry_rotation_matrix(self.angle)
            
            elif self.axis_option == RotateAxisOptionsEnum.Z:
                return generate_rz_rotation_matrix(self.angle)
            
            else:
                t = generate_translation_matrix(-self.point.x(), -self.point.y(), -self.point.z())
                t_inv = linalg.inv(t)
                self.axis = apply_matrix_in_point(self.axis, t)
                ry = generate_ry_rotation_matrix(self.angle)

                if self.axis.y() == 0:
                    # In Z axis => Just rotate -90 on X axis
                    if self.axis.x() == 0:
                        rx = generate_rx_rotation_matrix(-90)
                        rx_inv = linalg.inv(rx)
                        return concat_transformation_matrixes([
                            t, 
                            rx,
                            ry,
                            rx_inv,
                            t_inv
                        ])
                
                    # In X axis => Just rotate 90 on Z axis
                    elif self.axis.z() == 0:
                        rz = generate_rz_rotation_matrix(90)
                        rz_inv = linalg.inv(rz)
                        return concat_transformation_matrixes([
                            t, 
                            rz,
                            ry,
                            rz_inv,
                            t_inv
                        ])
                    
                    # In XZ plane (worst case) (x != 0, y = 0, z != 0)
                    else:
                        # Rotate -90 on x axis to force the y to be != 0, will make the z to be zero (XY plane)
                        rx = generate_rx_rotation_matrix(-90)
                        rx_inv = linalg.inv(rx)

                        angle_z = degrees(arctan(self.axis.x()/self.axis.y()))
                        rz = generate_rz_rotation_matrix(angle_z)
                        rz_inv = linalg.inv(rz)

                        return concat_transformation_matrixes([
                            t, 
                            rx,
                            rz,
                            ry,
                            rz_inv,
                            rx_inv,
                            t_inv
                        ])
                
                # Already in y axis (x=0 && z=0)
                if (self.axis.x() == 0 and self.axis.z() == 0):
                    return concat_transformation_matrixes([
                        t, 
                        ry,
                        t_inv
                    ])
                
                # Don't need Rx rotation for put in xy plane (z=0)
                elif self.axis.z() == 0:
                    angle_z = degrees(arctan(self.axis.x()/self.axis.y()))
                    rz = generate_rz_rotation_matrix(angle_z)
                    rz_inv = linalg.inv(rz)
                    return concat_transformation_matrixes([
                        t, 
                        rz,
                        ry,
                        rz_inv,
                        t_inv
                    ])
                
                # Don't need Rz rotation to put in y (x=0 and z!=0)
                elif self.axis.x() == 0:
                    angle_x = -degrees(arctan(self.axis.z()/self.axis.y()))
                    rx = generate_rx_rotation_matrix(angle_x)
                    rx_inv = linalg.inv(rx)
                    return concat_transformation_matrixes([
                        t, 
                        rx,
                        ry,
                        rx_inv,
                        t_inv
                    ])
                
                angle_x = -degrees(arctan(self.axis.z()/self.axis.y()))
                rx = generate_rx_rotation_matrix(angle_x)
                rx_inv = linalg.inv(rx)
                self.axis = apply_matrix_in_point(self.axis, rx)

                angle_z = degrees(arctan(self.axis.x()/self.axis.y()))
                rz = generate_rz_rotation_matrix(angle_z)
                rz_inv = linalg.inv(rz)
                return concat_transformation_matrixes([
                    t, 
                    rx,
                    rz,
                    ry,
                    rz_inv,
                    rx_inv,
                    t_inv
                ])

class ScaleTransformation(Transformation):
    def __init__(self, sx: float, sy: float, sz:float):
        self.sx = sx
        self.sy = sy
        self.sz = sz
    
    def __str__(self) -> str:
        return f'Escalonar(sx={self.sx}, sy={self.sy},sz={self.sz})'
    
    def generate_matrix(self, obj: GraphicObject, v_up_angle: float, window_center: Point3D) -> array:
        return generate_scale_operation_matrix(obj.center, self.sx, self.sy, self.sz)

class TranslateTransformation(Transformation):
    def __init__(self, dx: float, dy: float, dz: float):
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def __str__(self) -> str:
        return f'Transladar(dx={self.dx}, dy={self.dy}, dz={self.dz})'

    def generate_matrix(self, obj: GraphicObject, v_up_angle: float, window_center: Point3D) -> array:
        return translate_matrix_for_rotated_window(Point3D(self.dx, self.dy, self.dz), v_up_angle, window_center)

class TransformDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.transformations : List[Transformation]= []

        self.setGeometry(0,0,850,100)

        self.layout = QGridLayout()
        self.vertical_layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.scaling_tab = ScalingTabWidget(self.add_transformation)
        self.tabs.addTab(self.scaling_tab, 'Escalonar')

        self.translating_tab = TranslatingTabWidget(self.add_transformation)
        self.tabs.addTab(self.translating_tab, 'Transladar')

        self.rotating_tab = RotatingTabWidget(self.add_transformation)
        self.tabs.addTab(self.rotating_tab, 'Rotacionar')

        self.vertical_layout.addWidget(self.tabs)

        self.layout.addLayout(self.vertical_layout, 0, 0)

        self.log = Log[Union[TranslateTransformation, ScaleTransformation, RotateTransformation, str]]('=== Transformações ===')
        self.layout.addWidget(self.log, 0, 1, -1, -1)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancelar')
        self.button_layout.addWidget(self.cancel_button)

        self.apply_transformations_button = QPushButton('Aplicar transformações')
        self.button_layout.addWidget(self.apply_transformations_button)

        self.layout.addLayout(self.button_layout, 1, 0)

        self.setLayout(self.layout)

    def add_transformation(self, transformation: Union[TranslateTransformation, ScaleTransformation, RotateTransformation], msg: Union[str, None] = None):
        self.transformations.append(transformation)
        if transformation != None:
            self.log.add_item(transformation)
        elif msg != None:
            self.log.add_item(f'[ERRO] {msg}')

    def clear(self):
        self.transformations = []
        self.scaling_tab.clear_inputs()
        self.rotating_tab.clear_inputs()
        self.translating_tab.clear_inputs()
        self.log.clear()


class ScalingTabWidget(QWidget):
    def __init__(self, add_transformation: Callable):
        super().__init__()

        self.add_transformation = add_transformation
        
        self.layout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.scale_x_input = QLineEdit()
        self.scale_x_input.setPlaceholderText('Digite um valor para crescer em x')
        self.formLayout.addRow('Escala em x (vezes)', self.scale_x_input)

        self.scale_y_input = QLineEdit()
        self.scale_y_input.setPlaceholderText('Digite um valor para crescer em y')
        self.formLayout.addRow('Escala em y (vezes)', self.scale_y_input)

        self.scale_z_input = QLineEdit()
        self.scale_z_input.setPlaceholderText('Digite um valor para crescer em z')
        self.formLayout.addRow('Escala em z (vezes)', self.scale_z_input)

        self.layout.addLayout(self.formLayout)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancelar')
        self.button_layout.addWidget(self.cancel_button)

        self.cancel_button.clicked.connect(self.clear_inputs)

        self.save_button = QPushButton('Salvar')
        self.button_layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.handle_submit)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def handle_submit(self):
        sx = self.scale_x_input.text()
        sy = self.scale_y_input.text()
        sz = self.scale_z_input.text()
        self.add_transformation(ScaleTransformation(float(sx), float(sy), float(sz)))
        self.clear_inputs()

    def clear_inputs(self):
        self.scale_x_input.clear()
        self.scale_y_input.clear()
        self.scale_z_input.clear()

class TranslatingTabWidget(QWidget):
    def __init__(self, add_transformation: Callable):
        super().__init__()

        self.add_transformation = add_transformation
        
        self.layout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.move_x_input = QLineEdit()
        self.move_x_input.setPlaceholderText('Digite um valor para mover em x ')
        self.formLayout.addRow('Mover em x', self.move_x_input)

        self.move_y_input = QLineEdit()
        self.move_y_input.setPlaceholderText('Digite um valor para mover em y')
        self.formLayout.addRow('Mover em y', self.move_y_input)

        self.move_z_input = QLineEdit()
        self.move_z_input.setPlaceholderText('Digite um valor para mover em z')
        self.formLayout.addRow('Mover em z', self.move_z_input)

        self.layout.addLayout(self.formLayout)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancelar')
        self.button_layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.clear_inputs)
        
        self.save_button = QPushButton('Salvar')
        self.button_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.handle_submit)

        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)
    
    
    def handle_submit(self):
        dx = self.move_x_input.text()
        dy = self.move_y_input.text()
        dz = self.move_z_input.text()
        self.add_transformation(TranslateTransformation(float(dx), float(dy), float(dz)))
        self.clear_inputs()

    def clear_inputs(self):
        self.move_x_input.clear()
        self.move_y_input.clear()
        self.move_z_input.clear()
    
class RotatingTabWidget(QWidget):
    def __init__(self, add_transformation: Callable):
        super().__init__()

        self.add_transformation = add_transformation

        self.layout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItem(RotateOptionsEnum.WORLD.value)
        self.combo_box.addItem(RotateOptionsEnum.OBJECT.value)
        self.combo_box.addItem(RotateOptionsEnum.POINT.value)
        self.combo_box.addItem(RotateOptionsEnum.AXIS.value)

        self.layout.addWidget(self.combo_box)

        self.combo_box.currentIndexChanged.connect(self.on_change)

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText('Digite um ângulo')
        self.formLayout.addRow('Ângulo de rotação anti-horária (em graus)', self.angle_input)

        self.point_input = QLineEdit()
        self.point_input.setDisabled(True)
        self.point_input.setPlaceholderText('Digite as coordenadas de um ponto: (x,y,z)')
        self.formLayout.addRow('Ponto:', self.point_input)

        # ====== AXIS 

        self.axis_layout = QVBoxLayout()
        self.radiobuttons_layout = QHBoxLayout()
        self.axis_layout.addWidget(QLabel('Eixo de referência para rotação'))

        self.axis_button_group = QButtonGroup(self)

        # X
        self.x_axis_button = QRadioButton(RotateAxisOptionsEnum._to_str(RotateAxisOptionsEnum.X))
        self.x_axis_button.setChecked(True)
        self.axis_button_group.addButton(self.x_axis_button, RotateAxisOptionsEnum.X)
        self.radiobuttons_layout.addWidget(self.x_axis_button)
        self.x_axis_button.toggled.connect(lambda: self.handle_click(RotateAxisOptionsEnum.X))

        # Y
        self.y_axis_button = QRadioButton(RotateAxisOptionsEnum._to_str(RotateAxisOptionsEnum.Y))
        self.axis_button_group.addButton(self.y_axis_button, RotateAxisOptionsEnum.Y)
        self.radiobuttons_layout.addWidget(self.y_axis_button)
        self.y_axis_button.toggled.connect(lambda: self.handle_click(RotateAxisOptionsEnum.Y))

        # Z
        self.z_axis_button = QRadioButton(RotateAxisOptionsEnum._to_str(RotateAxisOptionsEnum.Z))
        self.axis_button_group.addButton(self.z_axis_button, RotateAxisOptionsEnum.Z)
        self.radiobuttons_layout.addWidget(self.z_axis_button)
        self.z_axis_button.toggled.connect(lambda: self.handle_click(RotateAxisOptionsEnum.Z))

        # ARBITRARY
        self.arbitrary_axis_button = QRadioButton(RotateAxisOptionsEnum._to_str(RotateAxisOptionsEnum.ARBITRARY))
        self.axis_button_group.addButton(self.arbitrary_axis_button, RotateAxisOptionsEnum.ARBITRARY)
        self.radiobuttons_layout.addWidget(self.arbitrary_axis_button)
        self.arbitrary_axis_button.toggled.connect(lambda: self.handle_click(RotateAxisOptionsEnum.ARBITRARY))

        self.arbitrary_axis_input = QLineEdit()
        self.arbitrary_axis_input.setDisabled(True)
        self.arbitrary_axis_input.setPlaceholderText('Digite as coordenadas de um ponto: (x,y,z)')
        self.formLayout.addRow('Eixo arbitrário:', self.arbitrary_axis_input)

        self.axis_layout.addLayout(self.radiobuttons_layout)

        self.layout.addLayout(self.axis_layout)

        self.layout.addLayout(self.formLayout)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancelar')
        self.button_layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.clear_inputs)

        self.save_button = QPushButton('Salvar')
        self.button_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.handle_submit)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def handle_submit(self):
        angle = self.angle_input.text()
        option = RotateOptionsEnum.valueOf(self.combo_box.currentText())
        axis_option = RotateAxisOptionsEnum.valueOf(self.axis_button_group.checkedId())

        if option == RotateOptionsEnum.POINT:
            point = parse(self.point_input.text())
            if point == None:
                self.add_transformation(None, "As coordenadas do ponto não respeitam o formato, por favor respeite.")
            elif len(point) != 1:
                self.add_transformation(None, "Um ponto deve ter apenas um par de coordenadas.")
            else:
                self.add_transformation(RotateTransformation(option, -float(angle), point[0]))
               
        elif option == RotateOptionsEnum.AXIS:
            if axis_option == RotateAxisOptionsEnum.ARBITRARY:
                axis = parse(self.arbitrary_axis_input.text())
                point = parse(self.point_input.text())
                if axis == None:
                    self.add_transformation(None, "As coordenadas do eixo não respeitam o formato, por favor respeite.")
                elif len(axis) != 1:
                    self.add_transformation(None, "Um vetor deve ter apenas um par de coordenadas.")
                else:
                    self.add_transformation(RotateTransformation(option, -float(angle), point[0], axis_option, axis[0]))
            else:
                self.add_transformation(RotateTransformation(option, -float(angle), axis_option=axis_option))
        else:
            self.add_transformation(RotateTransformation(option, -float(angle)))
        
        self.clear_inputs()

    def clear_inputs(self):
        self.angle_input.clear()
        self.point_input.clear()
        self.arbitrary_axis_input.clear()
        self.combo_box.setCurrentIndex(0)
        self.x_axis_button.setChecked(True)
    
    def on_change(self, index: int):
        if self.combo_box.currentText() == RotateOptionsEnum.POINT.value:
            self.point_input.setEnabled(True)
        else:
            self.point_input.setDisabled(True)

    def handle_click(self, option: RotateAxisOptionsEnum):
        if self.combo_box.currentText() == RotateOptionsEnum.AXIS.value and self.axis_button_group.checkedId() == RotateAxisOptionsEnum.ARBITRARY:
            self.arbitrary_axis_input.setEnabled(True)
            self.point_input.setEnabled(True)
        else:
            self.arbitrary_axis_input.setDisabled(True)
            self.point_input.setDisabled(True)