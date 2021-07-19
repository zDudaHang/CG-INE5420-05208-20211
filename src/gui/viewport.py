from typing import List
from PyQt5.QtWidgets import  QAction, QLabel
from PyQt5.QtGui import QColor, QPainter, QPen, QWheelEvent

from src.model.graphic_object import GraphicObject
from src.model.point import Point2D

class Viewport(QLabel):
    def __init__(self):
        super().__init__()
        self.top_left = Point2D(0,0)
        self.top_right = Point2D(400,0)

        self.bottom_left = Point2D(0,400)
        self.bottom_right = Point2D(400,400)

        self.objects = []

        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)
        
        self.setMinimumWidth(self.bottom_right.get_x())
        self.setMinimumHeight(self.bottom_right.get_y())

        self.action_scroll_zoom_in = QAction("Zoom In", self)
        self.action_scroll_zoom_out = QAction("Zoom Out", self)
        
        self.addAction(self.action_scroll_zoom_in)
        self.addAction(self.action_scroll_zoom_out)

    def wheelEvent(self, event: QWheelEvent):
        if (event.angleDelta().y() > 0):
            self.action_scroll_zoom_in.trigger()
        else:
            self.action_scroll_zoom_out.trigger()

    def draw_objects(self, objects: List[GraphicObject]):
        self.objects = objects
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()

        for obj in self.objects:
            obj.draw(painter,self.top_left, self.bottom_right)
                    
        # Pintando a borda vermelha da viewport
        
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)
 
        painter.drawLine(10, 10, 390, 10)
        painter.drawLine(10, 10, 10, 390)
        painter.drawLine(10, 390, 390, 390)
        painter.drawLine(390, 10, 390, 390)

        # Coordenadas viewport
        
        pen.setWidth(1)
        pen.setColor(QColor(224,224,224))
        painter.setPen(pen)
 
        painter.drawLine(50, 200, 350, 200)
        painter.drawLine(200, 50, 200, 350)