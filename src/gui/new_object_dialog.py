from src.model.enum.curve_enum import CurveEnum
from typing import Any, Dict, List
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QButtonGroup, QCheckBox, QColorDialog, QDialog, QFormLayout, QHBoxLayout, QPushButton, QRadioButton, QTabWidget, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget

from src.model.graphic_object import GraphicObjectEnum
from src.model.new_widget import NewWidget
from src.model.enum.graphic_object_form_enum import GraphicObjectFormEnum

class NewObjectDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Criando um novo objeto')
        self.setGeometry(0,0,900,150)

        self.layout = QVBoxLayout()

        self.widget_tabs : Dict[GraphicObjectEnum, GraphicObjectTabWidget] = {}
        
        self.tabs = QTabWidget()
        self.point_tab = PointTabWidget()
        self.widget_tabs[GraphicObjectEnum.POINT] = self.point_tab
        self.tabs.addTab(self.point_tab, GraphicObjectEnum.POINT.value)

        self.line_tab = LineTabWidget()
        self.widget_tabs[GraphicObjectEnum.LINE] = self.line_tab
        self.tabs.addTab(self.line_tab, GraphicObjectEnum.LINE.value)

        self.wireframe_tab = WireframeTabWidget()
        self.widget_tabs[GraphicObjectEnum.WIREFRAME] = self.wireframe_tab
        self.tabs.addTab(self.wireframe_tab, GraphicObjectEnum.WIREFRAME.value)

        self.curve_tab = CurveTabWidget()
        self.widget_tabs[GraphicObjectEnum.CURVE] = self.curve_tab
        self.tabs.addTab(self.curve_tab, GraphicObjectEnum.CURVE.value)

        self.obj_3d_tab = Object3DTab()
        self.widget_tabs[GraphicObjectEnum.OBJECT_3D] = self.obj_3d_tab
        self.tabs.addTab(self.obj_3d_tab, GraphicObjectEnum.OBJECT_3D.value)

        self.bicubic_tab = BicubicTabWidget()
        self.widget_tabs[GraphicObjectEnum.BICUBIC] = self.bicubic_tab
        self.tabs.addTab(self.bicubic_tab, GraphicObjectEnum.BICUBIC.value)

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def get_values(self, name: GraphicObjectEnum) -> Dict[GraphicObjectFormEnum, Any]:
        return self.widget_tabs[name].get_values()

    def clear_inputs(self, name: GraphicObjectEnum):
        self.widget_tabs[name].clear_inputs()

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
        # coordinates.setText('(100,100,0),(200,100,0),(200,200,0),(100,200,0),(100,100,100),(200,100,100),(200,200,100),(100,200,100)')
        coordinates.setPlaceholderText(placeholder)
        self.addRow(coordinates_title.value, coordinates)
        self.widgets[coordinates_title] = NewWidget(coordinates, coordinates.text, coordinates.clear)

        # COLOR BUTTON
        color_title = GraphicObjectFormEnum.COLOR
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

class GraphicObjectTabWidget(QWidget):
    def __init__(self, coord_placeholder: str, new_widgets: Dict[GraphicObjectFormEnum, NewWidget] = None):
        super().__init__()
        self.formLayout = GraphicObjectForm(coord_placeholder, new_widgets)
        self.setLayout(self.formLayout)
    
    def get_values(self) -> Dict[GraphicObjectFormEnum, Any]:
        return self.formLayout.get_values()

    def clear_inputs(self):
        self.formLayout.clear_inputs()

class PointTabWidget(GraphicObjectTabWidget):
    def __init__(self):
        super().__init__('Digite as coordenadas: (x,y,z)')

class LineTabWidget(GraphicObjectTabWidget):
    def __init__(self):
        super().__init__('Digite as coordenadas: (x1,y1,z1),(x2,y2,z2)')

class WireframeTabWidget(GraphicObjectTabWidget):
    def __init__(self):
        fill_check_box = QCheckBox('Preenchido')
        super().__init__('Digite as coordenadas: (x1,y1,z1),(x2,y2,z2),(x3,y3,z3),...', 
            {
                GraphicObjectFormEnum.FILLED: 
                NewWidget(fill_check_box, fill_check_box.isChecked, lambda: fill_check_box.setChecked(False))
            })

class CurveTabWidget(GraphicObjectTabWidget):
    def __init__(self):
        radio_buttons_layout = QHBoxLayout()
        curve_button_group = QButtonGroup()

        bezier_radiobutton = QRadioButton("B??zier")
        bezier_radiobutton.setChecked(True)
        bspline_radiobutton = QRadioButton("B-Spline")

        curve_button_group.addButton(bezier_radiobutton, CurveEnum.BEZIER)
        curve_button_group.addButton(bspline_radiobutton, CurveEnum.BSPLINE)

        radio_buttons_layout.addWidget(bezier_radiobutton)
        radio_buttons_layout.addWidget(bspline_radiobutton)

        super().__init__('Digite as coordenadas: (x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4), ...', 
        {
            GraphicObjectFormEnum.CURVE_OPTION:
            NewWidget(radio_buttons_layout, curve_button_group.checkedId, lambda: bezier_radiobutton.setChecked(True))
        })

class Object3DTab(GraphicObjectTabWidget):
    def __init__(self):
        new_widgets = {}

        edges_input = QLineEdit()
        edges_input.setPlaceholderText('Digite os n??meros dos pontos para criar as arestas: (1,2),(2,3),...')
        # edges_input.setText('(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)')
        new_widgets[GraphicObjectFormEnum.EDGES] = NewWidget(edges_input, edges_input.text, edges_input.clear)

        faces_input = QLineEdit()
        faces_input.setPlaceholderText('Digite os n??meros arestas que devem formar cada face: (1,2,3), (1,2,3,4),...')
        # faces_input.setText('(1,2,3,4),(5,6,7,8),(9,6,11,2),(10,8,12,4),(1,9,5,10),(3,11,7,12)')
        new_widgets[GraphicObjectFormEnum.FACES] = NewWidget(faces_input, faces_input.text, faces_input.clear)

        super().__init__('Digite as coordenadas: (x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4), ...', new_widgets)
        # super().__init__('(0,0,0),(0,100,0),(100,100,0),(100,0,0),(0,0,100),(0,100,100),(100,100,100),(100,0,100)', new_widgets)

class BicubicTabWidget(GraphicObjectTabWidget):
    def __init__(self):
        radio_buttons_layout = QHBoxLayout()
        curve_button_group = QButtonGroup()

        bezier_radiobutton = QRadioButton("B??zier")
        bezier_radiobutton.setChecked(True)
        bspline_radiobutton = QRadioButton("B-Spline")

        curve_button_group.addButton(bezier_radiobutton, CurveEnum.BEZIER)
        curve_button_group.addButton(bspline_radiobutton, CurveEnum.BSPLINE)

        radio_buttons_layout.addWidget(bezier_radiobutton)
        radio_buttons_layout.addWidget(bspline_radiobutton)

        super().__init__('Digite os 16 pontos de controle: (x1,y1,z1),(x2,y2,z2),..., (x16,y16,z16)', 
        {
            GraphicObjectFormEnum.CURVE_OPTION:
            NewWidget(radio_buttons_layout, curve_button_group.checkedId, lambda: bezier_radiobutton.setChecked(True))
        })