from src.model.enum.projection_enum import ProjectionEnum
from src.model.enum.line_clipping_options_enum import LineClippingOptionsEnum
from PyQt5.QtWidgets import QAction, QButtonGroup, QHBoxLayout, QRadioButton, QVBoxLayout, QLabel, QWidget

from src.gui.objects_list import ObjectsList
from src.gui.window_menu import WindowMenu
from src.gui.h_line import QHLine

class FunctionsMenu(QWidget):
    def __init__(self, step: float, angle: float):
        super().__init__()

        self.layout = QVBoxLayout()
  
        self.layout.addWidget(QLabel("Menu de funções"))

        self.layout.addWidget(QHLine())

        self.object_list = ObjectsList()
        self.layout.addWidget(self.object_list)

        self.layout.addWidget(QHLine())

        self.window_menu = WindowMenu(step, angle)
        self.layout.addWidget(self.window_menu)

        # ================= CLIPPING

        self.clipping_layout = QVBoxLayout()
        self.radiobuttons_layout = QHBoxLayout()
        self.clipping_layout.addWidget(QLabel('Técnica de clipagem de retas'))

        self.clipping_method : LineClippingOptionsEnum = LineClippingOptionsEnum.LIANG_B

        self.clipping_button_group = QButtonGroup(self)
        self.liangb_radiobutton = QRadioButton(LineClippingOptionsEnum.LIANG_B.value)

        # Making default
        self.liangb_radiobutton.setChecked(True)
        self.liangb_radiobutton.toggled.connect(lambda: self.handle_click(LineClippingOptionsEnum.LIANG_B))
        self.clipping_button_group.addButton(self.liangb_radiobutton)

        self.radiobuttons_layout.addWidget(self.liangb_radiobutton)

        self.cohens_radiobutton = QRadioButton(LineClippingOptionsEnum.COHEN_S.value)
        self.cohens_radiobutton.toggled.connect(lambda: self.handle_click(LineClippingOptionsEnum.COHEN_S))
        self.clipping_button_group.addButton(self.cohens_radiobutton)

        self.clipping_updated_action = QAction('Change clipping method')
        self.addAction(self.clipping_updated_action)

        self.radiobuttons_layout.addWidget(self.cohens_radiobutton)

        self.clipping_layout.addLayout(self.radiobuttons_layout)

        self.layout.addLayout(self.clipping_layout)

        # ================= PROJECTION

        self.proj_layout = QVBoxLayout()
        self.proj_radiobuttons_layout = QHBoxLayout()
        self.proj_layout.addWidget(QLabel('Técnica de projeção'))

        self.proj_method : ProjectionEnum = ProjectionEnum.PARALLEL

        self.proj_button_group = QButtonGroup(self)
        self.parallel_radiobutton = QRadioButton(ProjectionEnum.PARALLEL.value)

        # Making default
        self.parallel_radiobutton.setChecked(True)
        self.parallel_radiobutton.toggled.connect(lambda: self.handle_proj_click(ProjectionEnum.PARALLEL))
        self.proj_button_group.addButton(self.parallel_radiobutton)

        self.proj_radiobuttons_layout.addWidget(self.parallel_radiobutton)

        self.perspective_radiobutton = QRadioButton(ProjectionEnum.PERSPECTIVE.value)
        self.perspective_radiobutton.toggled.connect(lambda: self.handle_proj_click(ProjectionEnum.PERSPECTIVE))
        self.proj_button_group.addButton(self.perspective_radiobutton)

        self.proj_updated_action = QAction('Change projection method')
        self.addAction(self.proj_updated_action)

        self.proj_radiobuttons_layout.addWidget(self.perspective_radiobutton)

        self.proj_layout.addLayout(self.proj_radiobuttons_layout)

        self.layout.addLayout(self.proj_layout)
        
        self.setLayout(self.layout)

        self.width = 500
        self.height = 600
        
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)

    def handle_click(self, option: LineClippingOptionsEnum):
        self.clipping_method = option
        self.clipping_updated_action.trigger()

    def handle_proj_click(self, option: ProjectionEnum):
        self.proj_method = option
        self.proj_updated_action.trigger()