from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout

class Log(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area_content = QWidget()
        self.scroll_area_content.setGeometry( 0, 0, 400, 400 )
        self.scroll_area.setWidget(self.scroll_area_content)

        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area_layout.addWidget(QLabel("Log"))

        self.setLayout(self.layout)
    
    def add_log(self, text: str):
        self.scroll_area_layout.addWidget(QLabel(text))