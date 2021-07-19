from PyQt5.QtWidgets import QComboBox, QDialog, QFormLayout, QGridLayout, QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QLineEdit, QWidget
from typing import Callable, Union
from enum import Enum

from src.util.parse import parse
from src.model.point import Point2D
from src.gui.log import Log

class RotateOptionsEnum(Enum):
    WORLD = 'Rotacionar em torno do centro do mundo'
    OBJECT = 'Rotacionar em torno do centro do objeto'
    POINT = 'Rotacionar em torno de um ponto'

    def valueOf(value: str):
        if (value == RotateOptionsEnum.WORLD.value):
            return RotateOptionsEnum.WORLD
        if (value == RotateOptionsEnum.OBJECT.value):
            return RotateOptionsEnum.OBJECT
        if (value == RotateOptionsEnum.POINT.value):
            return RotateOptionsEnum.POINT
        return None

class RotateTransformation():
    def __init__(self, option: RotateOptionsEnum, angle: float, point: Point2D = None):
        self.option = option
        self.angle = angle
        if self.option == RotateOptionsEnum.POINT:
            self.point = point

    def __str__(self) -> str:
        if self.option != RotateOptionsEnum.POINT:
            return f'{self.option.value} em {self.angle} graus'
        return f'Rotacionar em torno do ponto {self.point.__str__()} em {self.angle} graus'

class ScaleTransformation():
    def __init__(self, sx: float, sy: float):
        self.sx = sx
        self.sy = sy
    
    def __str__(self) -> str:
        return f'Escalonar(sx={self.sx}, sy={self.sy})'

class TranslateTransformation():
    def __init__(self, dx: float, dy: float):
        self.dx = dx
        self.dy = dy

    def __str__(self) -> str:
        return f'Transladar(dx={self.dx}, dy={self.dy})'

class TransformDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.transformations = []

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
        self.add_transformation(ScaleTransformation(float(sx), float(sy)))
        self.clear_inputs()

    def clear_inputs(self):
        self.scale_x_input.clear()
        self.scale_y_input.clear()

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
        self.add_transformation(TranslateTransformation(float(dx), float(dy)))
        self.clear_inputs()

    def clear_inputs(self):
        self.move_x_input.clear()
        self.move_y_input.clear()
    
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

        self.layout.addWidget(self.combo_box)

        self.combo_box.currentIndexChanged.connect(self.on_change)

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText('Digite um ângulo para rotacionar')
        self.formLayout.addRow('Ângulo de rotação (em graus)', self.angle_input)

        self.point_input = QLineEdit()
        self.point_input.setDisabled(True)
        self.point_input.setPlaceholderText('Digite as coordenadas de um ponto: (x,y)')
        self.formLayout.addRow('Ponto:', self.point_input)

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
        points = parse(self.point_input.text())
        option = RotateOptionsEnum.valueOf(self.combo_box.currentText())
        if option == RotateOptionsEnum.POINT:
            if points == None:
                self.add_transformation(None, "As coordenadas do ponto não respeitam o formato, por favor respeite.")
                return None
            elif len(points) != 1:
                self.add_transformation(None, "Um ponto deve ter apenas um par de coordenadas.")
                return None
            else:
                self.add_transformation(RotateTransformation(option, float(angle), points[0]))
                return
        self.add_transformation(RotateTransformation(option, float(angle)))
        self.clear_inputs()

    def clear_inputs(self):
        self.angle_input.clear()
        self.point_input.clear()
        self.combo_box.setCurrentIndex(0)
    
    def on_change(self, index: int):
        if self.combo_box.currentText() == RotateOptionsEnum.POINT.value:
            self.point_input.setEnabled(True)
        else:
            self.point_input.setDisabled(True)