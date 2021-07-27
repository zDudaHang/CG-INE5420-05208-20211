from src.util.curves import blending_function, get_GB
from src.util.math import matrix_multiplication
from src.model.enum.graphic_object_enum import GraphicObjectEnum
from typing import Callable, List, Union
from abc import ABC, abstractmethod
from functools import reduce
from PyQt5.QtGui import QBrush, QPainter, QColor, QPainterPath, QPen

from src.util.transform import iterative_viewport_transform, viewport_transform
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
        
        self.center = calculate_center(self.coordinates)

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

class BezierCurve(GraphicObject):
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point2D], color: QColor):
        if len(coordinates) < 4:
            raise ValueError("[ERRO] Uma curva de Bézier deve ter pelo menos 4 pontos!")

        # TOTAL DE PONTOS DE UMA CURVA BEZIER = 4 (minimo) + 3n, sendo n pertencente aos numeros naturais
        n = (len(coordinates) - 4) % 3
        if n != 0:
            raise ValueError("[ERRO] A quantidade de pontos da curva deve estar na imagem da função f(x) = 4 + 3x, sendo x pertencente aos números naturais, para garantir a continuidade G(0). Alguns valores válidos: 4, 7, 10 e 13")
        super().__init__(name, type, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        for i in range(0, len(self.coordinates) - 3, 3):
            gb = get_GB(self.coordinates[i], self.coordinates[i+1], self.coordinates[i+2], self.coordinates[i+3])

            accuracy = 0.001

            t = 0.0

            while t <= 1.0:
                x1 = blending_function(t, gb.x)
                y1 = blending_function(t, gb.y)

                x2 = blending_function(t + accuracy, gb.x)
                y2 = blending_function(t + accuracy, gb.y)

                p1 = viewport_transform(Point2D(x1, y1), viewport_min, viewport_max, viewport_origin)

                p2 = viewport_transform(Point2D(x2, y2), viewport_min, viewport_max, viewport_origin)

                painter.drawLine(p1.to_QPointF(), p2.to_QPointF())

                t += accuracy

def create_graphic_object(type: GraphicObjectEnum, name: str, coordinates: List[Point2D], color: QColor, is_filled: bool = False, onError: Callable = None) -> Union[GraphicObject, None]:

    graphic_obj: GraphicObject = None

    try:
        if type == GraphicObjectEnum.POINT:
            graphic_obj = Point(name, coordinates, color)
        
        if type == GraphicObjectEnum.LINE:
            graphic_obj = Line(name, coordinates, color)
        
        if type == GraphicObjectEnum.WIREFRAME:
            graphic_obj = WireFrame(name, coordinates, color, is_filled)
        
        if type == GraphicObjectEnum.CURVE:
            graphic_obj = BezierCurve(name, type, coordinates, color)
        
    except ValueError as e:
            onError(e.__str__())
    
    return graphic_obj

def calculate_center(coordinates: List[Point2D]) -> Union[Point2D, None]:
    size = len(coordinates)
    
    if size > 0:
        cx = reduce(lambda acc, p: acc + p.x(), coordinates, 0) / size
        cy = reduce(lambda acc, p: acc + p.y(), coordinates, 0) / size
        return Point2D(cx, cy)
    else: 
        return None

def get_rgb(color: QColor) -> list:
    rgb = []
    rgb.append(color.red() / 255)
    rgb.append(color.green() / 255)
    rgb.append(color.blue() / 255)

    return rgb

def apply_matrix_in_object(object: GraphicObject, m: List[List[float]]) -> GraphicObject:
    coords = []
    for point2D in object.coordinates:
        coords.append(apply_matrix_in_point(point2D, m))
    if isinstance(object, WireFrame):
        return create_graphic_object(object.type, object.name, coords, object.color, object.is_filled)
    return create_graphic_object(object.type, object.name, coords, object.color)

def apply_matrix_in_point(point: Point2D, m: List[List[float]]) -> Point2D:
    r = matrix_multiplication(point.coordinates, m)
    return Point2D(r[0][0], r[0][1])
