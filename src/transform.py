from point import Point2D
from typing import List

def iterative_viewport_transform(object_coordinates: List[Point2D], window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D) -> List[Point2D]:
    viewport_coordinates: List[Point2D] = []
    for p in object_coordinates:
        viewport_coordinates.append(viewport_transform(p, window_min, window_max, viewport_min, viewport_max))
    return viewport_coordinates

def viewport_transform(object_coordinates: Point2D, window_min: Point2D, window_max: Point2D, viewport_min: Point2D, viewport_max: Point2D) -> Point2D:
    # x_div = (x_w - x_w_min) / (x_w_max - x_w_min)
    x_div = (object_coordinates.get_x() - window_min.get_x()) / (window_max.get_x() - window_min.get_x())

    # x_v = x_div * (x_v_max - x_v_min)
    x_v = x_div * (viewport_max.get_x() - viewport_min.get_x())

    # y_div = (y_w - y_w_min) / (y_w_max - y_w_min)
    y_div = (object_coordinates.get_y() - window_min.get_y()) / (window_max.get_y() - window_min.get_y())

    # y_v = (1 - y_div) * (y_v_max - y_v_min)
    y_v = (1 - y_div) * (viewport_max.get_y() - viewport_min.get_y())

    return Point2D(x_v, y_v)

def generate_translation_matrix(dx: float, dy: float):
    return [
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]]

def generate_scaling_matrix(sx: float, sy: float):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]]

def matrix_multiplication(a: list, b: list) -> list:
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

def translate_object(object_coordinates: list, dx: float, dy: float) -> list:
    t = generate_translation_matrix(dx, dy)

    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, t)
    return object_coordinates

def scale_object(object_coordinates: list, cx: float, cy: float, sx: float, sy: float) -> list :
    t1 = generate_translation_matrix(-cx, -cy)
    scale = generate_scaling_matrix(sx, sy)
    t2 = generate_translation_matrix(cx, cy)

    r = matrix_multiplication(t1, scale)
    final_operation = matrix_multiplication(r, t2)
    
    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final_operation)
    return object_coordinates