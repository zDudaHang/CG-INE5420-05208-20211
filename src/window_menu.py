from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton

class WindowMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Window"))

        # ZOOM:
        self.zoom_box = QHBoxLayout()
        self.zoom_box.addWidget(QLabel("Zoom"))
        
        self.zoom_in_button = QPushButton('+')
        self.zoom_in_button.setFixedSize(QSize(50,20))
        self.zoom_box.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton('-')
        self.zoom_out_button.setFixedSize(QSize(50,20))
        self.zoom_box.addWidget(self.zoom_out_button)

        self.layout.addLayout(self.zoom_box)

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
        
        self.setLayout(self.layout)