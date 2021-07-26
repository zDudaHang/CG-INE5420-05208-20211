from src.model.enum.coords_enum import CoordsEnum
from typing import List
from PyQt5.QtWidgets import  QAction, QLabel
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QWheelEvent

from src.model.graphic_object import GraphicObject
from src.model.point import Point2D

class Viewport(QLabel):
    def __init__(self, viewport_coordinates: List[Point2D], viewport_width: int, viewport_height: int, viewport_origin: Point2D):
        super().__init__()
        
        self.coordinates = viewport_coordinates
        self.width = viewport_width
        self.height = viewport_height
        self.origin = viewport_origin

        self.objects = []

        stylesheet = '''
            QLabel {
                background-color: white;
                border: 1px solid black
            }
        '''
        self.setStyleSheet(stylesheet)

        # 20 => +10 para cada lado para a viewport não ocupar todo o QLabel
        self.setMinimumWidth(self.width + 20)
        self.setMinimumHeight(self.height + 20)
        self.setMaximumHeight(self.height + 20)
        self.setMaximumWidth(self.width + 20)

        self.action_scroll_zoom_in = QAction("Zoom In", self)
        self.action_scroll_zoom_out = QAction("Zoom Out", self)
        
        self.addAction(self.action_scroll_zoom_in)
        self.addAction(self.action_scroll_zoom_out)

# ========== EVENT HANDLERS

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.action_scroll_zoom_in.trigger()
        else:
            self.action_scroll_zoom_out.trigger()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()

        self.draw_axes(pen, painter)

        self.draw_viewport_border(pen, painter)
        
        for obj in self.objects:
            obj.draw(painter, self.coordinates[CoordsEnum.BOTTOM_LEFT], self.coordinates[CoordsEnum.TOP_RIGHT], self.origin)

        
# ========== DRAW FUNCTIONS

    def draw_objects(self, objects: List[GraphicObject]):
        self.objects = objects
        self.update()

    def draw_axes(self, pen: QPen, painter: QPainter):       
        pen.setWidth(1)
        pen.setColor(QColor(224,224,224))
        painter.setPen(pen)

        middle_x = (self.width / 2) + self.origin.x()
        middle_y = (self.height / 2) + self.origin.y()

        # x axis
        painter.drawLine(self.origin.x(), middle_y, self.width + self.origin.x(), middle_y)

        # y axis
        painter.drawLine(middle_x, self.origin.y(), middle_x, self.height + self.origin.y())
    
    def draw_viewport_border(self, pen: QPen, painter: QPainter):
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        top_left = self.coordinates[CoordsEnum.TOP_LEFT].to_QPointF()
        top_right = self.coordinates[CoordsEnum.TOP_RIGHT].to_QPointF()

        bottom_left = self.coordinates[CoordsEnum.BOTTOM_LEFT].to_QPointF()
        bottom_right = self.coordinates[CoordsEnum.BOTTOM_RIGHT].to_QPointF()

        # Bottom Left -> Bottom Right
        painter.drawLine(bottom_left, bottom_right)

        # Top Left -> Top Right
        painter.drawLine(top_left, top_right)

        # Top Left -> Bottom Left
        painter.drawLine(top_left, bottom_left)

        # Top Right -> Bottom Right
        painter.drawLine(top_right, bottom_right)