from abc import ABC, abstractmethod
from enum import Enum
import util

from PyQt5.QtGui import QPainter, QColor, QPen
from transform import iterative_viewport_transform, viewport_transform
from point import Point2D
from typing import List

class GraphicObjectEnum(Enum):
    POINT = "Ponto"
    LINE = "Reta"
    WIREFRAME = "Wireframe"

    def valueOf(value: str) :
        if (value == GraphicObjectEnum.POINT.value):
            return GraphicObjectEnum.POINT
        if (value == GraphicObjectEnum.LINE.value):
            return GraphicObjectEnum.LINE
        if (value == GraphicObjectEnum.WIREFRAME.value):
            return GraphicObjectEnum.WIREFRAME
        return None


class GraphicObject(ABC):

    def __init__(self, name: str, type : GraphicObjectEnum, coordinates: List[Point2D], color: QColor):
        self.name = name
        self.type = type
        self.coordinates = coordinates
        if color == None:
            self.color = QColor(0,0,0)
        else:
            self.color = color     
        self.center = util.calculate_center(self.coordinates)

    @abstractmethod
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D):
        ...

    def __str__(self):
        return f'{self.type.value} ({self.name})'

    def drawLines(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D):
        points = iterative_viewport_transform(self.coordinates, viewport_min, viewport_max)
        
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        for i in range(0, len(points) - 1):
            painter.drawLine(points[i].to_QPointF(), points[i+1].to_QPointF())
        
    
class Point(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D], color: QColor):
        if len(coordinates) > 1:
            raise ValueError("[ERRO] Um ponto deve ter apenas um par de coordenadas (x,y)!")
        super().__init__(name, GraphicObjectEnum.POINT, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D):
        p_v = viewport_transform(self.coordinates[0], viewport_min, viewport_max)
        
        pen = QPen()
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
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D):
        self.drawLines(painter, viewport_min, viewport_max)

class WireFrame(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D], color: QColor):
        if len(coordinates) < 3:
            raise ValueError("[ERRO] Um wireframe deve ter no mínimo três pares de coordenadas!")
        super().__init__(name, GraphicObjectEnum.WIREFRAME, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D):
        self.drawLines(painter, viewport_min, viewport_max)

        # Liga a primeira tupla na ultima tupla
        p_v1 = viewport_transform(self.coordinates[0], viewport_min, viewport_max)
        p_v2 = viewport_transform(self.coordinates[-1], viewport_min, viewport_max)
        painter.drawLine(p_v1.to_QPointF(), p_v2.to_QPointF())