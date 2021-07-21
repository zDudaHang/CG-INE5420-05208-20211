from typing import Callable, List, Union
from functools import reduce
from PyQt5.QtGui import QColor

from src.model.point import Point2D
from src.model.graphic_object import GraphicObject, GraphicObjectEnum, Point, Line, WireFrame
from src.util.math import matrix_multiplication

def create_graphic_object(type: GraphicObjectEnum, name: str, coordinates: List[Point2D], color: QColor, is_filled: bool = False, onError: Callable = None) -> Union[GraphicObject, None]:

    graphic_obj: GraphicObject = None

    try:
        if type == GraphicObjectEnum.POINT:
            graphic_obj = Point(name, coordinates, color)
        
        if type == GraphicObjectEnum.LINE:
            graphic_obj = Line(name, coordinates, color)
        
        if type == GraphicObjectEnum.WIREFRAME:
            graphic_obj = WireFrame(name, coordinates, color, is_filled)
        
    except ValueError as e:
            onError(e.__str__())
    
    return graphic_obj

def calculate_center(coordinates: List[Point2D]) -> Union[Point2D, None]:
    size = len(coordinates)
    
    if size > 0:
        cx = reduce(lambda acc, p: acc + p.x(), coordinates, 0) / size
        cy = reduce(lambda acc, p: acc + p.y(), coordinates, 0) / size
        return Point2D(cx, cy )
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