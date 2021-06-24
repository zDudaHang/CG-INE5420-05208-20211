from PyQt5.QtWidgets import  QAction, QLabel
from PyQt5.QtGui import QPainter, QPen, QWheelEvent
from PyQt5.QtCore import Qt
from point import Point2D

class Viewport(QLabel):
    def __init__(self):
        super().__init__()
        self.min = Point2D(0,0)
        self.max = Point2D(400,400)

# TODO: Achar um jeito melhor de definir isso

        self.objects = []
        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)
        
        self.setMinimumWidth(self.max.get_x())
        self.setMinimumHeight(self.max.get_y())

        self.action_scroll_zoom_in = QAction("Zoom In", self)
        self.action_scroll_zoom_out = QAction("Zoom Out", self)

    def wheelEvent(self, event: QWheelEvent):
        if (event.angleDelta().y() > 0):
            self.action_scroll_zoom_in.trigger()
        else:
            self.action_scroll_zoom_out.trigger()

    def draw_objects(self, objects: list, window_min: Point2D, window_max: Point2D):
        self.objects = objects
        self.window_min = window_min
        self.window_max = window_max
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  2))
        for obj in self.objects:
            obj.draw(painter, self.window_min, self.window_max, self.min, self.max)