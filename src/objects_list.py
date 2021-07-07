from typing import Callable
from PyQt5.QtWidgets import QAction, QHBoxLayout, QPushButton, QScrollArea, QVBoxLayout, QLabel, QWidget
from graphic_object import GraphicObject

class ObjectsList(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)

        self.scroll_area_content = QWidget()
        self.scroll_area_content.setGeometry( 0, 0, 400, 400 )
        self.scroll_area.setWidget(self.scroll_area_content)

        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)

        self.scroll_area_layout.addWidget(QLabel("Objetos"))

        self.edit_object_state = None

        self.action_edit_object = QAction("Edit")

        self.addAction(self.action_edit_object)

        self.setLayout(self.layout)

    def add_object(self, object: GraphicObject) -> None:
        self.scroll_area_layout.addWidget(ObjectView(object, self.handle_edit))

    def handle_edit(self, object: GraphicObject) -> None:
        self.edit_object_state = object
        self.action_edit_object.trigger()

class ObjectView(QWidget):

    def __init__(self, object: GraphicObject, handle_edit: Callable) -> None:
        super().__init__()

        self.object : GraphicObject = object

        self.handle_edit = handle_edit

        self.layout = QHBoxLayout()

        self.label = QLabel(self.object.__str__())
        self.layout.addWidget(self.label)

        self.edit_button = QPushButton('Editar')
        self.edit_button.clicked.connect(self.on_edit)
        self.layout.addWidget(self.edit_button)
        
        self.setLayout(self.layout)

    def on_edit(self) -> None:
        self.handle_edit(self.object)