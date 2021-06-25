from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialogButtonBox, QGridLayout, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel, QWidget, QPushButton
from h_line import QHLine

class WindowMenu(QWidget):
    def __init__(self, step: int):
        super().__init__()

        self.layout = QVBoxLayout()

        self.layout.setSpacing(15)

        self.layout.addWidget(QLabel("Window"))

        # PASSO:
        self.step_box = QHBoxLayout()
        self.step_box.addWidget(QLabel("Passo:"))
        self.step_label = QLabel('%.2f%%' % (step * 100))
        self.step_box.addWidget(self.step_label)
        
        self.step_plus_button = QPushButton('+')
        self.step_plus_button.setFixedSize(QSize(50,20))
        self.step_box.addWidget(self.step_plus_button)

        self.step_minus_button = QPushButton('-')
        self.step_minus_button.setFixedSize(QSize(50,20))
        self.step_box.addWidget(self.step_minus_button)

        self.layout.addLayout(self.step_box)

        # ZOOM:
        self.zoom_box = QHBoxLayout()
        self.zoom_box.addWidget(QLabel("Zoom:"))
        
        self.zoom_in_button = QPushButton('+')
        self.zoom_in_button.setFixedSize(QSize(50,20))
        self.zoom_box.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton('-')
        self.zoom_out_button.setFixedSize(QSize(50,20))
        self.zoom_box.addWidget(self.zoom_out_button)

        self.layout.addLayout(self.zoom_box)

        self.layout.addWidget(QHLine())

        # Direction:
        self.direction_box = QGridLayout()

        self.direction_box.addWidget(QLabel("Direção"), 0, 0)
        
        self.left_button = QPushButton('◄')
        self.left_button.setFixedSize(QSize(50,20))
        self.direction_box.addWidget(self.left_button, 2, 0)

        self.right_button = QPushButton('►')
        self.right_button.setFixedSize(QSize(50,20))
        self.direction_box.addWidget(self.right_button, 2, 2)

        self.up_button = QPushButton('▲')
        self.up_button.setFixedSize(QSize(50,20))
        self.direction_box.addWidget(self.up_button, 1, 1)

        self.down_button = QPushButton('▼')
        self.down_button.setFixedSize(QSize(50,20))
        self.direction_box.addWidget(self.down_button, 2, 1)

        self.layout.addLayout(self.direction_box)

        self.layout.addWidget(QHLine())
        
        self.setLayout(self.layout)

    def update_step_value(self, value: str):
        self.step_label.setText('%.2f%%' % (value * 100))
