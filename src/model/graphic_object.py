from src.model.enum.curve_enum import CurveEnum
from src.util.curves import blending_function, get_GB, get_GB_Spline, forward_differences
from src.model.enum.graphic_object_enum import GraphicObjectEnum
from typing import Callable, List, Union
from abc import ABC, abstractmethod
from functools import reduce
from PyQt5.QtGui import QBrush, QPainter, QColor, QPainterPath, QPen

from src.model.point import Point3D
from src.util.clipping.curve_clipper import curve_clip

from numpy import dot

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

    def drawLines(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, painter_path : QPainterPath, viewport_origin: Point3D, 
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

        self.drawLines(painter, viewport_min, viewport_max, painter_path, viewport_origin)

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
        self.drawLines(painter, viewport_min, viewport_max, painter_path, viewport_origin, self.is_filled, self.is_clipped, is_wireframe=True)

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
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point3D], color: QColor, curve_type: CurveEnum):
        super().__init__(name, type, coordinates, color)

        self.curve_type = curve_type
     
class BezierCurve(Curve):
    curve_points = []
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point3D], color: QColor = None):
        if len(coordinates) < 4:
            raise ValueError("[ERRO] Uma curva de Bézier deve ter pelo menos 4 pontos!")

        # TOTAL DE PONTOS DE UMA CURVA BEZIER = 4 (minimo) + 3n, sendo n pertencente aos numeros naturais
        n = (len(coordinates) - 4) % 3
        if n != 0:
            raise ValueError("[ERRO] A quantidade de pontos da curva deve estar na imagem da função f(x) = 4 + 3x, sendo x pertencente aos números naturais, para garantir a continuidade G(0). Alguns valores válidos: 4, 7, 10 e 13")
        
        super().__init__(name, type, coordinates, color, CurveEnum.BEZIER)

        self.curve_points = BezierCurve.curve_points

    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
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


                x1, y1, x2, y2 = curve_clip(x1, y1, x2, y2)
                try:
                    p1 = viewport_transform(Point3D(x1, y1), viewport_min, viewport_max, viewport_origin)

                    p2 = viewport_transform(Point3D(x2, y2), viewport_min, viewport_max, viewport_origin)

                    painter.drawLine(p1.to_QPointF(), p2.to_QPointF())
                except TypeError:
                    pass
                
                t += accuracy

                BezierCurve.curve_points.extend([Point3D(x1,y1), Point3D(x2,y2)])

class BSpline(Curve):
    
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point3D], color: QColor = None):
        if len(coordinates) < 4:
            raise ValueError("[ERRO] Uma BSpline deve ter pelo menos 4 pontos!")

        n = (len(coordinates) - 4) % 3
        if n != 0:
            raise ValueError("[ERRO] A quantidade de pontos da curva deve estar na imagem da função f(x) = 4 + 3x, sendo x pertencente aos números naturais, para garantir a continuidade G(0). Alguns valores válidos: 4, 7, 10 e 13")
        
        super().__init__(name, type, coordinates, color, CurveEnum.BSPLINE)
        

    #drawCurveFwdDiff
    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.color)
        painter.setPen(pen)

      
        for i in range(len(self.coordinates) - 3):
            gb = get_GB_Spline(self.coordinates[i], self.coordinates[i+1], self.coordinates[i+2], self.coordinates[i+3])
            
            d = 0.01
            n = 1 / d

            x, y = forward_differences(d, gb)
            
            x_old = x[0][0]
            y_old = y[0][0]

            j = 1
            
            while j < n:
                j += 1
                

                x[0][0] += x[1][0]
                x[1][0] += x[2][0]
                x[2][0] += x[3][0]

                y[0][0] += y[1][0]
                y[1][0] += y[2][0]
                y[2][0] += y[3][0]

                x1, y1, x2, y2 = curve_clip(x_old, y_old, x[0][0], y[0][0])
                try:
                    p1 = viewport_transform(Point3D(x1, y1), viewport_min, viewport_max, viewport_origin)

                    p2 = viewport_transform(Point3D(x2, y2), viewport_min, viewport_max, viewport_origin)

                    painter.drawLine(p1.to_QPointF(), p2.to_QPointF())

                except TypeError:
                    pass
                
                x_old = x[0][0]
                y_old = y[0][0]

class Object3D(GraphicObject):
    
    def __init__(self, name: str, type: GraphicObjectEnum, coordinates: List[Point3D], color: QColor, edges: List[tuple], faces: List[tuple]):
        super().__init__(name, type, coordinates, color)

        self.edges = edges
        self.faces = faces

        self.edges_lines : List[Line] = []

        for edge in edges:
            first = edge[0] - 1
            second = edge[1] - 1
            line = Line('_', [coordinates[first], coordinates[second]])
            self.edges_lines.append(line)

        self.faces_wireframes : List[WireFrame] = []
        
        for face in faces:
            coords = []
            for edge in face:
                coords.extend(self.edges_lines[edge - 1].coordinates)
            self.faces_wireframes.append(WireFrame('_', coords, self.color, False, True))


    def draw(self, painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
        pass



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
                graphic_obj = BezierCurve(name, type, coordinates, color)
            else:
                graphic_obj = BSpline(name, type, coordinates, color)
        
        if type == GraphicObjectEnum.OBJECT_3D:

            # transform_matrix = parallel_projection(window_coordinates)
            # coords = []
            # for c in coordinates:
            #     m = dot(c.coordinates,transform_matrix)
            #     coords.append(Point3D(m[0][0], m[0][1]))

            graphic_obj = Object3D(name, type, coordinates, color, edges, faces)
        
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
        # return create_graphic_object(object.type, object.name, coords, object.color, edges=object.edges, faces=object.faces, window_coordinates=window_coordinates)
        return create_graphic_object(object.type, object.name, coords, object.color, edges=object.edges, faces=object.faces)
    return create_graphic_object(object.type, object.name, coords, object.color)

def apply_matrix_in_point(point: Point3D, m: List[List[float]]) -> Point3D:
    r = dot(point.coordinates, m)

    return Point3D(r[0][0], r[0][1])

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
