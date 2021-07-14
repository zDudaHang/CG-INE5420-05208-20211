from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QColorDialog, QDialog, QFormLayout, QPushButton, QTabWidget, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget

from graphic_object import GraphicObjectEnum

class NewObjectDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Criando um novo objeto')
        self.setGeometry(0,0,500,150)

        self.layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.point_tab = PointTabWidget()
        self.tabs.addTab(self.point_tab, GraphicObjectEnum.POINT.value)

        self.line_tab = LineTabWidget()
        self.tabs.addTab(self.line_tab, GraphicObjectEnum.LINE.value)

        self.wireframe_tab = WireframeTabWidget()
        self.tabs.addTab(self.wireframe_tab, GraphicObjectEnum.WIREFRAME.value)

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def get_values(self, name: GraphicObjectEnum):
        if (name == GraphicObjectEnum.POINT):
            return self.point_tab.get_values()
        elif (name == GraphicObjectEnum.LINE):
            return self.line_tab.get_values()
        else: return self.wireframe_tab.get_values()

    def clear_inputs(self, name: GraphicObjectEnum):
        if (name == GraphicObjectEnum.POINT):
            return self.point_tab.clear_inputs()
        elif (name == GraphicObjectEnum.LINE):
            return self.line_tab.clear_inputs()
        else: return self.wireframe_tab.clear_inputs()

class GraphicObjectForm(QFormLayout):
    def __init__(self, placeholder: str):
        super().__init__()

        self.color = QColor(0,0,0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Digite um nome')
        self.addRow('Nome', self.name_input)
        
        self.coordinates = QLineEdit()
        self.coordinates.setPlaceholderText(placeholder)

        self.addRow('Coordenadas', self.coordinates)

        self.color_button = QPushButton()

        self.set_color()

        self.color_button.clicked.connect(self.open_dialog_color)
        self.addRow('Escolha uma cor', self.color_button)

        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.addWidget(self.buttons_box)


    def clear_inputs(self):
        self.name_input.clear()
        self.coordinates.clear()

    def get_values(self) -> list:
        return [self.name_input.text(), self.coordinates.text(), self.color]
    
    def open_dialog_color(self):
        selected_color = QColorDialog.getColor()
        r, g, b, a = selected_color.red(), selected_color.green(), selected_color.blue(), selected_color.alpha()
        self.color = QColor(r, g, b, a)       
        self.set_color()

    def set_color(self):
        palette = self.color_button.palette()
        role = self.color_button.backgroundRole()
        palette.setColor(role, self.color)
        self.color_button.setPalette(palette)
        self.color_button.setAutoFillBackground(True)

class PointTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = GraphicObjectForm('Digite as coordenadas: (x,y)')
        self.setLayout(self.formLayout)
    
    def get_values(self):
        return self.formLayout.get_values()

    def clear_inputs(self):
        self.formLayout.clear_inputs()

class LineTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = GraphicObjectForm('Digite as coordenadas: (x1,y1),(x2,y2)')
        self.setLayout(self.formLayout)

    def get_values(self):
        return self.formLayout.get_values()
    
    def clear_inputs(self):
        self.formLayout.clear_inputs()

class WireframeTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = GraphicObjectForm('Digite as coordenadas: (x1,y1),(x2,y2),(x3,y3),...')
        self.setLayout(self.formLayout)

    def get_values(self):
        return self.formLayout.get_values()

    def clear_inputs(self):
        self.formLayout.clear_inputs()