from abc import ABC, abstractmethod
from enum import Enum

from PyQt5.QtGui import QPainter
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

    def __init__(self, name: str, type : GraphicObjectEnum, coordinates: List[Point2D]):
        self.name = name
        self.type = type
        self.coordinates = coordinates

        cx = sum(c.get_x() for c in self.coordinates) / len(self.coordinates)
        cy = sum(c.get_y() for c in self.coordinates) / len(self.coordinates)
        
        self.center = Point2D(cx, cy)


    @abstractmethod
    def draw(self, painter: QPainter, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D):
        ...

    def __str__(self):
        return f'{self.type.value} ({self.name})'

    def drawLines(self, painter: QPainter, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D):
        points = iterative_viewport_transform(self.coordinates, window_min, window_max, viewport_min, viewport_max)
        for i in range(0, len(points) - 1):
            painter.drawLine(points[i].get_x(), points[i].get_y(), points[i+1].get_x(), points[i+1].get_y())
    
class Point(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D]):
        if len(coordinates) != 1:
            raise ValueError("[ERRO] Um ponto deve ter apenas um par de coordenadas (x,y)!")
        super().__init__(name, GraphicObjectEnum.POINT, coordinates)
    
    def draw(self, painter: QPainter, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D):
        p_v = viewport_transform(self.coordinates[0], window_min, window_max, viewport_min, viewport_max)
        painter.drawPoint(p_v.get_x(), p_v.get_y())
        
class Line(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D]):
        if len(coordinates) != 2:
            raise ValueError("[ERRO] Uma linha deve ter apenas 2 pares de coordenadas (x1,y1) e (x2, y2)!")
        super().__init__(name, GraphicObjectEnum.LINE, coordinates)
    
    def draw(self, painter: QPainter, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D):
        self.drawLines(painter, window_min, window_max, viewport_min, viewport_max)

class WireFrame(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point2D]):
        if len(coordinates) < 3:
            raise ValueError("[ERRO] Um wireframe deve ter no mínimo três pares de coordenadas!")
        super().__init__(name, GraphicObjectEnum.WIREFRAME, coordinates)
    
    def draw(self, painter: QPainter, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D):
        self.drawLines(painter, window_min, window_max, viewport_min, viewport_max)

        # Liga a primeira tupla na ultima tupla
        p_v1 = viewport_transform(self.coordinates[0], window_min, window_max, viewport_min, viewport_max)
        p_v2 = viewport_transform(self.coordinates[-1], window_min, window_max, viewport_min, viewport_max)
        painter.drawLine(p_v1.get_x(), p_v1.get_y(), p_v2.get_x(), p_v2.get_y())