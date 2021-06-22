from PyQt5.QtWidgets import  QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class Viewport(QLabel):
    def __init__(self):
        super().__init__()
        self.x_v_min = 0
        self.y_v_min = 0
        self.x_v_max = 400
        self.y_v_max = 400

# TODO: Achar um jeito melhor de definir isso

        self.objects = []
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

    def draw_objects(self, objects: list, x_w_min: int, y_w_min: int, x_w_max: int, y_w_max: int):
        self.objects = objects
        self.x_w_min = x_w_min
        self.y_w_min = y_w_min
        self.x_w_max = x_w_max
        self.y_w_max = y_w_max
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  2))
        for obj in self.objects:
            obj.draw(painter, self.x_w_min,  self.y_w_min, self.x_w_max, self.y_w_max, self.x_v_min, self.y_v_min, self.x_v_max, self.y_v_max)
