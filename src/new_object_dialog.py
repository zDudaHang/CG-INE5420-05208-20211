from PyQt5.QtWidgets import QDialog, QFormLayout, QTabWidget, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget

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
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Digite um nome')
        self.addRow('Nome', self.name_input)
        
        self.coordinates = QLineEdit()
        self.coordinates.setPlaceholderText(placeholder)

        self.addRow('Coordenadas', self.coordinates)

        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.addWidget(self.buttons_box)
    
    def clear_inputs(self):
        self.name_input.clear()
        self.coordinates.clear()

    def get_values(self) -> list:
        return [self.name_input.text(), self.coordinates.text()]

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
