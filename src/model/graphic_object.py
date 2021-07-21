from src.model.enum.graphic_object_enum import GraphicObjectEnum
from typing import List
from abc import ABC, abstractmethod
from PyQt5.QtGui import QBrush, QPainter, QColor, QPainterPath, QPen

from src.util.transform import iterative_viewport_transform, viewport_transform
import src.util.objects as objects
from src.model.point import Point2D

class GraphicObject(ABC):

    def __init__(self, name: str, type : GraphicObjectEnum, coordinates: List[Point2D], color: QColor):
        self.name = name

        self.type = type

        self.coordinates = coordinates

        if color == None:
            self.color = QColor(0,0,0)
        
        else:
            self.color = color
        
        self.center = objects.calculate_center(self.coordinates)

    @abstractmethod
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D):
        ...

    def __str__(self):
        return f'{self.type.value} ({self.name})'

    def drawLines(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, painter_path : QPainterPath, viewport_origin: Point2D):
        points = iterative_viewport_transform(self.coordinates, viewport_min, viewport_max, viewport_origin)
        
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        painter_path.moveTo(points[0].to_QPointF())

        for i in range(1, len(points)):
            painter_path.lineTo(points[i].to_QPointF())
        
        
    
class Point(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D], color: QColor):
        if len(coordinates) > 1:
            raise ValueError("[ERRO] Um ponto deve ter apenas um par de coordenadas (x,y)!")
        
        super().__init__(name, GraphicObjectEnum.POINT, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D):
        p_v = viewport_transform(self.coordinates[0], viewport_min, viewport_max, viewport_origin)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(self.color)
        painter.setPen(pen)

        painter.drawPoint(p_v.to_QPointF())
        
class Line(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D], color: QColor):
        if len(coordinates) > 2:
            raise ValueError("[ERRO] Uma linha deve ter apenas 2 pares de coordenadas (x1,y1) e (x2, y2)!")
        
        if len(coordinates) < 2:
            raise ValueError("[ERRO] Uma linha deve ter pelo menos 2 pares de coordenadas (x1,y1) e (x2, y2)!")
        
        super().__init__(name, GraphicObjectEnum.LINE, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D):
        painter_path = QPainterPath()

        self.drawLines(painter, viewport_min, viewport_max, painter_path, viewport_origin)

        painter.drawPath(painter_path)

class WireFrame(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D], color: QColor, is_filled: bool):
        if len(coordinates) < 3:
            raise ValueError("[ERRO] Um wireframe deve ter no mínimo três pares de coordenadas!")

        super().__init__(name, GraphicObjectEnum.WIREFRAME, coordinates, color)

        self.is_filled = is_filled
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D):
        painter_path = QPainterPath()

        self.drawLines(painter, viewport_min, viewport_max, painter_path, viewport_origin)

        p_v1 = viewport_transform(self.coordinates[0], viewport_min, viewport_max, viewport_origin)
        
        p_v2 = viewport_transform(self.coordinates[-1], viewport_min, viewport_max, viewport_origin)

        painter_path.lineTo(p_v1.to_QPointF())

        painter_path.lineTo(p_v2.to_QPointF())

        if self.is_filled:
            painter.fillPath(painter_path, QBrush(self.color))
        else:
            painter.drawPath(painter_path)

