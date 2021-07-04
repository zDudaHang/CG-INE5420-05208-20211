from PyQt5.QtWidgets import QComboBox, QDialog, QFormLayout, QTabWidget, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget

from enum import Enum

class RotateOptionsEnum(Enum):
    WORLD = 'Rotacionar em torno do centro do mundo'
    OBJECT = 'Rotacionar em torno do centro do objeto'
    POINT = 'Rotacionar em torno de um ponto'

    def valueOf(value: str) :
        if (value == RotateOptionsEnum.WORLD.value):
            return RotateOptionsEnum.WORLD
        if (value == RotateOptionsEnum.OBJECT.value):
            return RotateOptionsEnum.OBJECT
        if (value == RotateOptionsEnum.POINT.value):
            return RotateOptionsEnum.POINT
        return None


class TransformDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setGeometry(0,0,500,150)

        self.layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.scaling_tab = ScalingTabWidget()
        self.tabs.addTab(self.scaling_tab, 'Escalonar')

        self.translating_tab = TranslatingTabWidget()
        self.tabs.addTab(self.translating_tab, 'Transladar')

        self.rotating_tab = RotatingTabWidget()
        self.tabs.addTab(self.rotating_tab, 'Rotacionar')

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

class ScalingTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = QFormLayout()

        self.scale_x_input = QLineEdit()
        self.scale_x_input.setPlaceholderText('Digite um valor para crescer em x')
        self.formLayout.addRow('Escala em x (vezes)', self.scale_x_input)

        self.scale_y_input = QLineEdit()
        self.scale_y_input.setPlaceholderText('Digite um valor para crescer em y')
        self.formLayout.addRow('Escala em y (vezes)', self.scale_y_input)

        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.formLayout.addWidget(self.buttons_box)

        self.setLayout(self.formLayout)

class TranslatingTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = QFormLayout()

        self.move_x_input = QLineEdit()
        self.move_x_input.setPlaceholderText('Digite um valor para mover em x ')
        self.formLayout.addRow('Mover em x', self.move_x_input)

        self.move_y_input = QLineEdit()
        self.move_y_input.setPlaceholderText('Digite um valor para mover em y')
        self.formLayout.addRow('Mover em y', self.move_y_input)

        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.formLayout.addWidget(self.buttons_box)
        
        self.setLayout(self.formLayout)
    
class RotatingTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItem(RotateOptionsEnum.WORLD.value)
        self.combo_box.addItem(RotateOptionsEnum.OBJECT.value)
        self.combo_box.addItem(RotateOptionsEnum.POINT.value)
        self.layout.addWidget(self.combo_box)

        self.combo_box.currentIndexChanged.connect(self.on_change)

        self.angulo_input = QLineEdit()
        self.angulo_input.setPlaceholderText('Digite um ângulo para rotacionar')
        self.formLayout.addRow('Ângulo de rotação (em graus)', self.angulo_input)

        self.point_input = QLineEdit()
        self.point_input.setDisabled(True)
        self.point_input.setPlaceholderText('Digite as coordenadas de um ponto: (x,y)')
        self.formLayout.addRow('Ponto:', self.point_input)

        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.formLayout.addWidget(self.buttons_box)

        self.layout.addLayout(self.formLayout)
        self.setLayout(self.layout)
    
    def on_change(self, index: int):
        if self.combo_box.currentText() == RotateOptionsEnum.POINT.value:
            self.point_input.setEnabled(True)
        else:
            self.point_input.setDisabled(True)