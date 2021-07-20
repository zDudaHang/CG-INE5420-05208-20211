from typing import Callable, List, Union
from functools import reduce
from PyQt5.QtGui import QColor

from src.model.point import Point2D
from src.model.graphic_object import GraphicObject, GraphicObjectEnum, Point, Line, WireFrame
from src.util.math import matrix_multiplication

def create_graphic_object(type: GraphicObjectEnum, name: str, coordinates: List[Point2D], color: QColor, onError: Callable = None) -> Union[GraphicObject, None]:

    graphic_obj: GraphicObject = None

    try:
        if (type == GraphicObjectEnum.POINT):
            graphic_obj = Point(name, coordinates, color)
        if (type == GraphicObjectEnum.LINE):
            graphic_obj = Line(name, coordinates, color)
        if (type == GraphicObjectEnum.WIREFRAME):
            #coordinates = wireframe_points_list(coordinates)
            graphic_obj = WireFrame(name, coordinates, color)
    except ValueError as e:
            onError(e.__str__())
    
    return graphic_obj

def calculate_center(coordinates: List[Point2D]) -> Union[Point2D, None]:
    size = len(coordinates)
    
    if size > 0:
        cx = reduce(lambda acc, p: acc + p.get_x(), coordinates, 0) / size
        cy = reduce(lambda acc, p: acc + p.get_y(), coordinates, 0) / size
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
    return create_graphic_object(object.type, object.name, coords, object.color)

def apply_matrix_in_point(point: Point2D, m: List[List[float]]) -> Point2D:
    r = matrix_multiplication(point.coordinates, m)
    return Point2D(r[0][0], r[0][1])

def wireframe_points_list(coordinates: List[Point2D]):
    coordinates.insert(len(coordinates), coordinates[0])
    return coordinates

def flatten(t):
    return [item for sublist in t for item in sublist]