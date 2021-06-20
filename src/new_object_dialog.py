from PyQt5.QtWidgets import QDialog, QFormLayout, QVBoxLayout, QLineEdit, QComboBox, QDialogButtonBox

from graphic_object import GraphicObjectEnum

class NewObjectDialog(QDialog):
    combo_box_default = GraphicObjectEnum.POINT.value

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Criando um novo objeto')

        layout = QVBoxLayout()
        formLayout = QFormLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItems([g.value for g in GraphicObjectEnum])
        formLayout.addRow('Tipo', self.combo_box)

        self.name_input = QLineEdit()
        formLayout.addRow('Nome', self.name_input)
        
        self.coordinates = QLineEdit()
        formLayout.addRow('Coordenadas', self.coordinates )
        layout.addLayout(formLayout)
        
        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(
        QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        layout.addWidget(self.buttons_box)

        self.setLayout(layout)

    def clear_inputs(self):
        self.combo_box.setCurrentText(self.combo_box_default)
        self.name_input.clear()
        self.coordinates.clear()
