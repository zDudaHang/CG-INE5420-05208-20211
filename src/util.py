from PyQt5.QtGui import QColor
from point import Point2D
from graphic_object import GraphicObject, GraphicObjectEnum, Point, Line, WireFrame
from typing import Callable, List, Union
from functools import reduce

def matrix_multiplication(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    result = []

    # Populate the result matrix with zeros
    for i in range(0, len(a)):
        result.append([])
        for j in range(0, len(b[0])):
            result[i].append(0)

    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]

    return result

def apply_matrix_in_object(object: GraphicObject, m: List[List[float]]) -> GraphicObject:
    coords = []
    for point2D in object.coordinates:
        coords.append(apply_matrix_in_point(point2D, m))
    return create_graphic_object(object.type, object.name, coords, object.color)

def apply_matrix_in_point(point: Point2D, m: List[List[float]]) -> Point2D:
    r = matrix_multiplication(point.coordinates, m)
    print(r)
    return Point2D(r[0][0], r[0][1])

def create_graphic_object(type: GraphicObjectEnum, name: str, coordinates: List[Point2D], color: QColor, onError: Callable = None) -> Union[GraphicObject, None]:

    graphic_obj: GraphicObject = None

    try:
        if (type == GraphicObjectEnum.POINT):
            graphic_obj = Point(name, coordinates, color)
        if (type == GraphicObjectEnum.LINE):
            graphic_obj = Line(name, coordinates, color)
        if (type == GraphicObjectEnum.WIREFRAME):
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