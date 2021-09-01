from copy import deepcopy
from math import ceil, floor
from numpy.core.fromnumeric import transpose
from src.model.enum.curve_enum import CurveEnum
from src.util.curves import blending_function, fwd_diff, generate_curve_initial_values, generate_delta_matrix, get_GB_bezier, get_GB_spline
from src.util.bicubic import generate_surface_initial_values, get_bicubic_GB, blending_function_bicubic, get_bicubic_geometry_matrix
from src.model.enum.graphic_object_enum import GraphicObjectEnum
from typing import Callable, List, Union
from abc import ABC, abstractmethod
from functools import reduce
from PyQt5.QtGui import QBrush, QPainter, QColor, QPainterPath, QPen

from src.model.point import Point3D
from src.util.clipping.curve_clipper import curve_clip

from numpy import dot
from collections import defaultdict

class GraphicObject(ABC):

    def __init__(self, name: str, type : GraphicObjectEnum, coordinates: List[Point3D], color: QColor = None):
        self.name = name

        self.type = type

        self.coordinates = coordinates

        if color == None:
            self.color = QColor(0,0,0)       
        else:
            self.color = color
        
        self.center = calculate_center(self.coordinates)

    @abstractmethod
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        ...

    def __str__(self):
        return f'{self.type.value} ({self.name})'

    def draw_lines(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, painter_path : QPainterPath, viewport_origin: Point3D, 
                  is_filled: bool = False, is_clipped: bool = False, is_wireframe: bool = False):

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        if is_wireframe:
            if is_filled:
                self.coordinates = [[item for sublist in self.coordinates for item in sublist]]

            if is_clipped:
                points = []
                try:
                    for c in self.coordinates:
                        points.append(iterative_viewport_transform(c, viewport_min, viewport_max, viewport_origin))

                    for p in points:
                        painter_path.moveTo(p[0].to_QPointF())

                        for i in range(1, len(p)):
                            painter_path.lineTo(p[i].to_QPointF())
                except IndexError:
                    pass
            else:
                try:                   
                    points = iterative_viewport_transform(self.coordinates[0], viewport_min, viewport_max, viewport_origin)

                    painter_path.moveTo(points[0].to_QPointF())
                    
                    for i in range(1, len(points)):
                        painter_path.lineTo(points[i].to_QPointF())
                except IndexError:
                    pass
        else:
            points = iterative_viewport_transform(self.coordinates, viewport_min, viewport_max, viewport_origin)
            painter_path.moveTo(points[0].to_QPointF())

            for i in range(1, len(points)):
                painter_path.lineTo(points[i].to_QPointF())
    
class Point(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point3D], color: QColor):
        if len(coordinates) > 1:
            raise ValueError("[ERRO] Um ponto deve ter apenas um par de coordenadas (x,y)!")
        
        super().__init__(name, GraphicObjectEnum.POINT, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        p_v = viewport_transform(self.coordinates[0], viewport_min, viewport_max, viewport_origin)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(self.color)
        painter.setPen(pen)

        painter.drawPoint(p_v.to_QPointF())
        
class Line(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point3D], color: QColor = None):
        if len(coordinates) > 2:
            raise ValueError("[ERRO] Uma linha deve ter apenas 2 pares de coordenadas (x1,y1) e (x2, y2)!")
        
        if len(coordinates) < 2:
            raise ValueError("[ERRO] Uma linha deve ter pelo menos 2 pares de coordenadas (x1,y1) e (x2, y2)!")
        
        super().__init__(name, GraphicObjectEnum.LINE, coordinates, color)
    
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        painter_path = QPainterPath()
        self.draw_lines(painter, viewport_min, viewport_max, painter_path, viewport_origin)
        painter.drawPath(painter_path)

class WireFrame(GraphicObject):

    def __init__(self, name: str, coordinates: List[Point3D], color: QColor, is_filled: bool, is_clipped: bool):
        if len(coordinates) < 3:
            raise ValueError("[ERRO] Um wireframe deve ter no mínimo três pares de coordenadas!")

        super().__init__(name, GraphicObjectEnum.WIREFRAME, coordinates, color)

        self.is_filled = is_filled
        self.is_clipped = is_clipped
    
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        painter_path = QPainterPath()
        self.draw_lines(painter, viewport_min, viewport_max, painter_path, viewport_origin, self.is_filled, self.is_clipped, is_wireframe=True)

        if not self.is_clipped:
            p_v1 = viewport_transform(self.coordinates[0][0], viewport_min, viewport_max, viewport_origin)        
            p_v2 = viewport_transform(self.coordinates[0][-1], viewport_min, viewport_max, viewport_origin)

            painter_path.lineTo(p_v1.to_QPointF())
            painter_path.lineTo(p_v2.to_QPointF())

        if self.is_filled:
            painter.fillPath(painter_path, QBrush(self.color))
        else:
            painter.drawPath(painter_path)

class Curve(GraphicObject):
    def __init__(self, name: str, coordinates: List[Point3D], color: QColor, curve_type: CurveEnum):
        super().__init__(name, GraphicObjectEnum.CURVE, coordinates, color)

        self.curve_type = curve_type
    
    def draw_line(self, painter: QPainter, x1: float, x2: float, y1: float, y2: float, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D, z1: float = 0, z2: float = 0):
        # 2D Clip
        x1, y1, x2, y2 = curve_clip(x1, y1, x2, y2)

        if x1 != None and x2 != None and y1 != None and y2 != None:
            p1 = viewport_transform(Point3D(x1, y1, z1), viewport_min, viewport_max, viewport_origin)
            p2 = viewport_transform(Point3D(x2, y2, z2), viewport_min, viewport_max, viewport_origin)
            painter.drawLine(p1.to_QPointF(), p2.to_QPointF())
     
class BezierCurve(Curve):
    curve_points = []

    def __init__(self, name: str, coordinates: List[Point3D], color: QColor = None):
        if len(coordinates) < 4:
            raise ValueError("[ERRO] Uma curva de Bézier deve ter pelo menos 4 pontos!")

        # TOTAL DE PONTOS DE UMA CURVA BEZIER = 4 (minimo) + 3n, sendo n pertencente aos numeros naturais
        n = (len(coordinates) - 4) % 3
        if n != 0:
            raise ValueError("[ERRO] A quantidade de pontos da curva deve estar na imagem da função f(x) = 4 + 3x, sendo x pertencente aos números naturais, para garantir a continuidade G(0). Alguns valores válidos: 4, 7, 10 e 13")
        
        super().__init__(name, GraphicObjectEnum.CURVE, coordinates, color, CurveEnum.BEZIER)

        self.curve_points = BezierCurve.curve_points

    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        for i in range(0, len(self.coordinates) - 3, 3):
            gb = get_GB_bezier(self.coordinates[i], self.coordinates[i+1], self.coordinates[i+2], self.coordinates[i+3])

            accuracy = 0.001

            t = 0.0
            while t <= 1.0:
                x1 = blending_function(t, gb.x)
                y1 = blending_function(t, gb.y)

                x2 = blending_function(t + accuracy, gb.x)
                y2 = blending_function(t + accuracy, gb.y)

                self.draw_line(painter, x1, x2, y1, y2, viewport_min, viewport_max, viewport_origin)
                
                t += accuracy

                BezierCurve.curve_points.extend([Point3D(x1,y1), Point3D(x2,y2)])

class BSpline(Curve):
    
    def __init__(self, name: str, coordinates: List[Point3D], color: QColor = None):
        if len(coordinates) < 4:
            raise ValueError("[ERRO] Uma BSpline deve ter pelo menos 4 pontos!")

        super().__init__(name, GraphicObjectEnum.CURVE, coordinates, color, CurveEnum.BSPLINE)
    
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        delta = 0.01
        n = 1 / delta
        delta_matrix = generate_delta_matrix(delta)

        for i in range(len(self.coordinates) - 3):
            gb = get_GB_spline(self.coordinates[i], self.coordinates[i+1], self.coordinates[i+2], self.coordinates[i+3])
            initial_values = generate_curve_initial_values(delta_matrix, gb)
            fwd_diff(n, initial_values, self.draw_line, painter, viewport_min, viewport_max, viewport_origin)

class Object3D(GraphicObject):
    
    def __init__(self, name: str, coordinates: List[Point3D], color: QColor, edges: List[tuple], faces: List[tuple] = None):
        super().__init__(name, GraphicObjectEnum.OBJECT_3D, coordinates, color)

        self.edges = edges
        self.faces = faces

        self.edges_lines : List[Line] = []

        for edge in edges:
            first = edge[0] - 1
            second = edge[1] - 1
            print(f'Edge: {coordinates[first]} -> {coordinates[second]}')
            line = Line('_', [coordinates[first], coordinates[second]])
            self.edges_lines.append(line)

        self.faces_wireframes : List[WireFrame] = []
        
        if faces != None:
            for face in faces:
                coords = []
                for edge in face:
                    coords.extend(self.edges_lines[edge - 1].coordinates)
                self.faces_wireframes.append(WireFrame('_', coords, self.color, False, True))

    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pass

class BicubicSurface(Curve):
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point3D], curve: CurveEnum, color: QColor = None):
        if len(coordinates) < 16:
            raise ValueError("[ERRO] Uma superfície bicúbica deve ter 16 pontos!")

        n = (len(coordinates)) % 16
        if n != 0:
            raise ValueError("[ERRO] Adicionar conjuntos de pontos de controle 16 a 16.")
        
        super().__init__(name, type, coordinates, color, curve)

class BezierBicubicSurface(BicubicSurface):
    
    def __init__(self, name: str, coordinates: List[Point3D], color: QColor = None):
        super().__init__(name, GraphicObjectEnum.BICUBIC_BEZIER, coordinates, CurveEnum.BEZIER, color)

    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        gb = get_bicubic_GB(self.coordinates)
        
        points = defaultdict(list)
        accuracy = 0.111
        s = 0.0
        t = 0.0
        while s <= 1.0:
            t = 0.0
            while t <= 1.0:
                x1 = blending_function_bicubic(s, t, gb.x)
                y1 = blending_function_bicubic(s, t, gb.y)
                z1 = blending_function_bicubic(s, t, gb.z)
                points[s].append(Point3D(x1[0][0], y1[0][0], z1[0][0]))            
                t += accuracy
            s += accuracy    

        # Direção S
        for k, v in points.items():
            for i in range(len(v)-1):
                self.draw_line(painter, v[i].x(), v[i+1].x(), v[i].y(), v[i+1].y(), viewport_min, viewport_max, viewport_origin, v[i].z(), v[i+1].z())

        # Direção T
        for i in range(10):
            t_list = [elem[i] for elem in points.values()]
            for j in range(len(t_list)-1):
                self.draw_line(painter, t_list[j].x(), t_list[j+1].x(), t_list[j].y(), t_list[j+1].y(), viewport_min, viewport_max, viewport_origin, t_list[j].z(), t_list[j+1].z())

class BSplineBicubicSurface(BicubicSurface):
    
    def __init__(self, name: str, coordinates: List[Point3D], color: QColor = None):    
        super().__init__(name, GraphicObjectEnum.BICUBIC_BSPLINE, coordinates, CurveEnum.BSPLINE, color)

    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

        # Mesmo delta para s e t, logo o mesmo n tambem
        delta = 0.01
        n = ceil(1 / delta)

        delta_matrix = generate_delta_matrix(delta)

        # Valores iniciais:
        gb = get_bicubic_geometry_matrix(self.coordinates)

        initial_values = generate_surface_initial_values(delta_matrix, transpose(delta_matrix), gb)
        
        # Cria uma copia para ser usada no lugar da original
        auxiliary = deepcopy(initial_values)

        # t
        for i in range(0, n):
            fwd_diff(n, auxiliary.to_fwd_diff(), self.draw_line, painter, viewport_min, viewport_max, viewport_origin)
            auxiliary.update()
        
        initial_values.transpose()

        # s
        for j in range(0, n):
            fwd_diff(n, initial_values.to_fwd_diff(), self.draw_line, painter, viewport_min, viewport_max, viewport_origin)
            initial_values.update()


def create_graphic_object(type: GraphicObjectEnum, name: str, coordinates: List[Point3D], color: QColor, is_filled: bool = False, is_clipped: bool = False, \
    curve_option: CurveEnum = None, edges: str = None, faces: str = None, onError: Callable = None) -> Union[GraphicObject, None]:
    
    graphic_obj: GraphicObject = None

    try:
        if type == GraphicObjectEnum.POINT:
            graphic_obj = Point(name, coordinates, color)
        
        if type == GraphicObjectEnum.LINE:
            graphic_obj = Line(name, coordinates, color)
        
        if type == GraphicObjectEnum.WIREFRAME:
            graphic_obj = WireFrame(name, coordinates, color, is_filled, is_clipped)
        
        if type == GraphicObjectEnum.CURVE:
            if curve_option == CurveEnum.BEZIER:
                graphic_obj = BezierCurve(name, coordinates, color)
            else:
                graphic_obj = BSpline(name, coordinates, color)
        
        if type == GraphicObjectEnum.OBJECT_3D:
            graphic_obj = Object3D(name, coordinates, color, edges, faces)
        
        if type == GraphicObjectEnum.BICUBIC_BEZIER or type == GraphicObjectEnum.BICUBIC_BSPLINE:
            # graphic_obj = BezierBicubicSurface(name, coordinates, color)
            graphic_obj = BSplineBicubicSurface(name, coordinates, color)

    except ValueError as e:
        onError(e.__str__())
    
    return graphic_obj

def calculate_center(coordinates: List[Point3D]) -> Union[Point3D, None]:
    size = len(coordinates)
    
    if size > 0:
        cx = reduce(lambda acc, p: acc + p.x(), coordinates, 0) / size
        cy = reduce(lambda acc, p: acc + p.y(), coordinates, 0) / size
        cz = reduce(lambda acc, p: acc + p.z(), coordinates, 0) / size
        return Point3D(cx, cy, cz)
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
    for Point3D in object.coordinates:
        coords.append(apply_matrix_in_point(Point3D, m))
    
    if isinstance(object, WireFrame):
        return create_graphic_object(object.type, object.name, coords, object.color, is_filled=object.is_filled)
    
    if isinstance(object, Curve):
        return create_graphic_object(object.type, object.name, coords, object.color, curve_option=object.curve_type)

    if isinstance(object, Object3D):
        return create_graphic_object(object.type, object.name, coords, object.color, edges=object.edges, faces=object.faces)
    return create_graphic_object(object.type, object.name, coords, object.color)

def apply_matrix_in_point(point: Point3D, m: List[List[float]]) -> Point3D:
    r = dot(point.coordinates, m)
    return Point3D(r[0][0], r[0][1], r[0][2])

def iterative_viewport_transform(object_coordinates: List[Point3D], viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D) -> List[Point3D]:
    viewport_coordinates: List[Point3D] = []
    for p in object_coordinates:
        viewport_coordinates.append(viewport_transform(p, viewport_min, viewport_max, viewport_origin))
    return viewport_coordinates

def viewport_transform(point: Point3D, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D) -> Point3D:
 
    window_min = Point3D(-1, -1)
    window_max = Point3D(1, 1)

    # x_div = (x_w - x_w_min) / (x_w_max - x_w_min)
    x_div = (point.x() - window_min.x()) / (window_max.x() - window_min.x())

    # x_v = x_div * (x_v_max - x_v_min)
    x_vp = x_div * (viewport_max.x() - viewport_min.x())

    # y_div = (y_w - y_w_min) / (y_w_max - y_w_min)
    y_div = (point.y() - window_min.y()) / (window_max.y() - window_min.y())

    # y_v = (1 - y_div) * (y_v_max - y_v_min)
    y_vp = (1 - y_div) * (viewport_max.y() - viewport_min.y())

    return Point3D(x_vp + viewport_origin.x(), y_vp + viewport_origin.y())
