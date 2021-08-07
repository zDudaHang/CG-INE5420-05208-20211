from typing import List
from math import sin, cos, radians

from src.model.point import Point2D
from src.util.math import matrix_multiplication

def iterative_viewport_transform(object_coordinates: List[Point2D], viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D) -> List[Point2D]:
    viewport_coordinates: List[Point2D] = []
    for p in object_coordinates:
        
        viewport_coordinates.append(viewport_transform(p, viewport_min, viewport_max, viewport_origin))
    return viewport_coordinates

def viewport_transform(point: Point2D, viewport_min: Point2D, viewport_max: Point2D, viewport_origin: Point2D) -> Point2D:
 
    window_min = Point2D(-1, -1)
    window_max = Point2D(1, 1)

    # x_div = (x_w - x_w_min) / (x_w_max - x_w_min)
    x_div = (point.x() - window_min.x()) / (window_max.x() - window_min.x())

    # x_v = x_div * (x_v_max - x_v_min)
    x_vp = x_div * (viewport_max.x() - viewport_min.x())

    # y_div = (y_w - y_w_min) / (y_w_max - y_w_min)
    y_div = (point.y() - window_min.y()) / (window_max.y() - window_min.y())

    # y_v = (1 - y_div) * (y_v_max - y_v_min)
    y_vp = (1 - y_div) * (viewport_max.y() - viewport_min.y())

    return Point2D(x_vp + viewport_origin.x(), y_vp + viewport_origin.y())

def generate_translation_matrix(dx: float, dy: float) -> List[List[float]]:
    return [
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]]

def generate_scaling_matrix(sx: float, sy: float) -> List[List[float]]:
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]]

def generate_rotation_matrix(angleGraus: float) -> List[List[float]]:
    angle = radians(angleGraus)
    return [
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ]

def translate_object(object_coordinates: List[Point2D], dx: float, dy: float) -> List[Point2D]:
    t = generate_translation_matrix(dx, dy)

    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, t)
    return object_coordinates

def translate_matrix_for_rotated_window(dx: float, dy: float, angle: float, cx: float, cy: float) -> List[Point2D]:
    # First, align the window with the world (-angle)
    r_align_with_world = generate_rotate_operation_matrix(cx, cy, -angle)

    # Move the window
    t = generate_translation_matrix(dx, dy)

    # Then rotate the window back (angle)
    r_rotate_back = generate_rotate_operation_matrix(cx, cy, angle)

    r = matrix_multiplication(r_align_with_world, t)
    return matrix_multiplication(r, r_rotate_back)

def translate_window(object_coordinates: List[Point2D], dx: float, dy: float, angle: float, cx: float, cy: float) -> List[Point2D]:
    final = translate_matrix_for_rotated_window(dx, dy, angle, cx, cy)
    
    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final)
    return object_coordinates

def rotate_window(object_coordinates: List[Point2D], angle: float, cx: float, cy: float) -> List[Point2D]:
    final = generate_rotate_operation_matrix(cx, cy, angle)
    
    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final)
    return object_coordinates

def scale_window(object_coordinates: List[Point2D], cx: float, cy: float, sx: float, sy: float) -> List[Point2D]:
    final = generate_scale_operation_matrix(cx, cy, sx, sy)

    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final)
    return object_coordinates

def generate_scale_operation_matrix(cx: float, cy: float, sx: float, sy: float) -> List[List[float]]:
    t1 = generate_translation_matrix(-cx, -cy)
    scale = generate_scaling_matrix(sx, sy)
    t2 = generate_translation_matrix(cx, cy)

    r = matrix_multiplication(t1, scale)
    return matrix_multiplication(r, t2)

def generate_rotate_operation_matrix(dx: float, dy: float, angle: float) -> List[List[float]]:
    t1 = generate_translation_matrix(-dx, -dy)
    rot = generate_rotation_matrix(angle)
    t2 = generate_translation_matrix(dx, dy)

    r = matrix_multiplication(t1, rot)
    return matrix_multiplication(r, t2)

def generate_scn_matrix(cx_w: float, cy_w: float, height_w: float, width_w: float, angle: float) -> List[List[float]]:
    t = generate_translation_matrix(-cx_w, -cy_w)
    r = generate_rotation_matrix(-angle)
    s = generate_scaling_matrix(1/(width_w/2), 1/(height_w/2))

    temp = matrix_multiplication(t, r)
    return matrix_multiplication(temp, s)