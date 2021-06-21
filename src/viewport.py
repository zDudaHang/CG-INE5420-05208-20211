from PyQt5.QtWidgets import  QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class Viewport(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.objects = []
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)

    def draw_objects(self, objects: list):
        self.objects = objects
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  2))
        for obj in self.objects:
            obj.draw(painter)
