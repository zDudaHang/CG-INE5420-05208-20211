from typing import Any, Dict
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCheckBox, QColorDialog, QDialog, QFormLayout, QPushButton, QTabWidget, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget

from src.model.graphic_object import GraphicObjectEnum
from src.model.new_widget import NewWidget
from src.model.enum.graphic_object_form_enum import GraphicObjectFormEnum

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

    def get_values(self, name: GraphicObjectEnum) -> Dict[GraphicObjectFormEnum, Any]:
        if name == GraphicObjectEnum.POINT:
            return self.point_tab.get_values()
        elif name == GraphicObjectEnum.LINE:
            return self.line_tab.get_values()
        else: return self.wireframe_tab.get_values()

    def clear_inputs(self, name: GraphicObjectEnum):
        if name == GraphicObjectEnum.POINT:
            return self.point_tab.clear_inputs()
        elif name == GraphicObjectEnum.LINE:
            return self.line_tab.clear_inputs()
        else: return self.wireframe_tab.clear_inputs()

class GraphicObjectForm(QFormLayout):
    def __init__(self, placeholder: str, new_widgets: Dict[GraphicObjectFormEnum, NewWidget] = None):
        super().__init__()

        self.widgets : Dict[GraphicObjectFormEnum,  NewWidget] = {}

        self.color = QColor(0,0,0)

        # NAME INPUT
        name_input_title = GraphicObjectFormEnum.NAME
        name_input = QLineEdit()
        name_input.setPlaceholderText('Digite um nome')
        self.addRow(name_input_title.value, name_input)
        self.widgets[name_input_title] = NewWidget(name_input, name_input.text, name_input.clear)
        
        # COORDINATES INPUT
        coordinates_title = GraphicObjectFormEnum.COORDINATES
        coordinates = QLineEdit()
        coordinates.setPlaceholderText(placeholder)
        self.addRow(coordinates_title.value, coordinates)
        self.widgets[coordinates_title] = NewWidget(coordinates, coordinates.text, coordinates.clear)

        # COLOR BUTTON
        color_title = GraphicObjectFormEnum.COORDINATES
        self.color_button = QPushButton()
        self.set_color()
        self.color_button.clicked.connect(self.open_dialog_color)
        self.addRow(color_title.value, self.color_button)

        # OTHER WIDGETS
        if new_widgets != None:
            for title, widget in new_widgets.items():
                self.addRow(title.value, widget.widget)
                self.widgets[title] = widget

        # FORM BUTTONS
        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttons_box.rejected.connect(self.clear_inputs)
        self.addWidget(self.buttons_box)


    def clear_inputs(self):
        for widget in self.widgets.values():
            widget.clear()

    def get_values(self) -> Dict[GraphicObjectFormEnum, Any]:
        values = {}

        values[GraphicObjectFormEnum.COLOR] = self.color

        for title, value in self.widgets.items():
            values[title] = value.get_value()
        
        return values
    
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
    
    def get_values(self) -> Dict[GraphicObjectFormEnum, Any]:
        return self.formLayout.get_values()

    def clear_inputs(self):
        self.formLayout.clear_inputs()

class LineTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = GraphicObjectForm('Digite as coordenadas: (x1,y1),(x2,y2)')
        self.setLayout(self.formLayout)

    def get_values(self) -> Dict[GraphicObjectFormEnum, Any]:
        return self.formLayout.get_values()
    
    def clear_inputs(self):
        self.formLayout.clear_inputs()

class WireframeTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        fill_check_box = QCheckBox('Preenchido', self)

        self.formLayout = GraphicObjectForm(
            'Digite as coordenadas: (x1,y1),(x2,y2),(x3,y3),...', 
            {
                GraphicObjectFormEnum.FILLED: 
                NewWidget(fill_check_box, fill_check_box.isChecked, lambda: fill_check_box.setChecked(False))
            }
        )

        self.setLayout(self.formLayout)

    def get_values(self) -> Dict[GraphicObjectFormEnum, Any]:
        return self.formLayout.get_values()

    def clear_inputs(self):
        self.formLayout.clear_inputs()