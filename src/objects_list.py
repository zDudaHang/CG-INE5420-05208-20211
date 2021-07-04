from typing import Callable
from PyQt5.QtWidgets import QAction, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget
from graphic_object import GraphicObject

class ObjectsList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.edit_object_state = None

        self.action_edit_object = QAction("Edit")

        self.addAction(self.action_edit_object)

        self.layout.addWidget(QLabel("Objetos"))

        self.setLayout(self.layout)

    def add_object(self, object: GraphicObject):
        self.layout.addWidget(ObjectView(object, self.handle_edit))

    def handle_edit(self, object: GraphicObject):
        self.edit_object_state = object
        self.action_edit_object.trigger()

class ObjectView(QWidget):

    def __init__(self, object: GraphicObject, handle_edit: Callable):
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

    def on_edit(self):
        self.handle_edit(self.object)