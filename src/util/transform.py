from typing import List
from math import sin, cos, radians, degrees, atan

from src.model.point import Point3D
from src.util.math import matrix_multiplication, matrix_subtraction

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

def generate_translation_matrix(dx: float, dy: float, dz: float = 0) -> List[List[float]]:
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]]

def generate_scaling_matrix(sx: float, sy: float, sz: float = 1) -> List[List[float]]:
    return [
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]]

def generate_rz_rotation_matrix(angleGraus: float) -> List[List[float]]:
    angle = radians(angleGraus)
    return [
            [cos(angle), sin(angle), 0, 0],
            [-sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]
    


def generate_ry_rotation_matrix(angleGraus: float) -> List[List[float]]:
    angle = radians(angleGraus)
    return[
            [cos(angle), 0, -sin(angle), 0],
            [0, 1, 0, 0],
            [sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]]
    


def generate_rx_rotation_matrix(angleGraus: float) -> List[List[float]]:
    angle = radians(angleGraus)
    return [
            [1, 0, 0, 0],
            [0, cos(angle), sin(angle), 0],
            [0, -sin(angle), cos(angle), 0],
            [0, 0, 0, 1]]

def translate_object(object_coordinates: List[Point3D], dx: float, dy: float) -> List[Point3D]:
    t = generate_translation_matrix(dx, dy)

    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, t)
    return object_coordinates

def translate_matrix_for_rotated_window(dx: float, dy: float, angle: float, cx: float, cy: float) -> List[Point3D]:
    # First, align the window with the world (-angle)
    r_align_with_world = generate_rotate_operation_matrix(cx, cy, -angle)

    # Move the window
    t = generate_translation_matrix(dx, dy)

    # Then rotate the window back (angle)
    r_rotate_back = generate_rotate_operation_matrix(cx, cy, angle)

    r = matrix_multiplication(r_align_with_world, t)
    return matrix_multiplication(r, r_rotate_back)

def translate_window(object_coordinates: List[Point3D], dx: float, dy: float, angle: float, cx: float, cy: float) -> List[Point3D]:
    final = translate_matrix_for_rotated_window(dx, dy, angle, cx, cy)
    
    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final)
    return object_coordinates

def rotate_window(object_coordinates: List[Point3D], angle: float, cx: float, cy: float) -> List[Point3D]:
    final = generate_rotate_operation_matrix(cx, cy, angle)
    
    for coord in object_coordinates:
        coord.coordinates = matrix_multiplication(coord.coordinates, final)
    return object_coordinates

def scale_window(object_coordinates: List[Point3D], cx: float, cy: float, sx: float, sy: float) -> List[Point3D]:
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
    rot = generate_rz_rotation_matrix(angle)
    t2 = generate_translation_matrix(dx, dy)

    r = matrix_multiplication(t1, rot)
    return matrix_multiplication(r, t2)

def generate_scn_matrix(cx_w: float, cy_w: float, height_w: float, width_w: float, angle: float) -> List[List[float]]:
    t = generate_translation_matrix(-cx_w, -cy_w)
    r = generate_rz_rotation_matrix(-angle)
    s = generate_scaling_matrix(1/(width_w/2), 1/(height_w/2))

    temp = matrix_multiplication(t, r)
    return matrix_multiplication(temp, s)


def get_w_homogen(window_coordinates : Point3D) -> List[List[float]]:
    return [[window_coordinates.x(), window_coordinates.y(), window_coordinates.z(), 1]]


def get_vpr(window_coordinates : List[Point3D]) -> List[float]:

    vpr_x = (window_coordinates[0].x() + window_coordinates[1].x() + window_coordinates[2].x() + window_coordinates[3].x()) / 4
    vpr_y = (window_coordinates[0].y() + window_coordinates[1].y() + window_coordinates[2].y() + window_coordinates[3].y()) / 4
    vpr_z = (window_coordinates[0].z() + window_coordinates[1].z() + window_coordinates[2].z() + window_coordinates[3].z()) / 4

    return [vpr_x, vpr_y, vpr_z]

def get_vpn(window_coordinates : List[Point3D], vpr : List[List[float]]) -> List[float]:
    
    wc_list_0 = [window_coordinates[0].x(), window_coordinates[0].y(), window_coordinates[0].z()]
    wc_list_1 = [window_coordinates[1].x(), window_coordinates[1].y(), window_coordinates[1].z()]

    v = matrix_subtraction(wc_list_0, vpr)
    u = matrix_subtraction(vpr, wc_list_1)

    c_x = v[1]*u[2] - v[2]*u[1]
    c_y = v[2]*u[0] - v[0]*u[2]
    c_z = v[0]*u[1] - v[1]*u[0]

    return [c_x, c_y, c_z]

def angle_with_vpn(vpn : List[float]):
    # rotação em x
    teta_x = degrees(atan(vpn[1]/vpn[2]))
    
    # rotação em y
    teta_y = degrees(atan(vpn[0]/vpn[2]))

    return teta_x, teta_y

def parallel_projection(window_coordinates : List[Point3D]) -> List[List[float]]:

    vpr = get_vpr(window_coordinates)

    trans = generate_translation_matrix(-vpr[0], -vpr[1], - vpr[2])
  

    vpn = get_vpn(window_coordinates, vpr)

    teta_x, teta_y = angle_with_vpn(vpn)

    rot_x = generate_rx_rotation_matrix(teta_x)
    rot_y = generate_ry_rotation_matrix(teta_y)


    transform = matrix_multiplication(trans, rot_x)
    transform = matrix_multiplication(transform, rot_y)
    
    return transform

    # temp_x, temp_y, temp_z = 0, 0, 0

    # for coord in window_coordinates:
    #     t = matrix_multiplication(get_w_homogen(coord), trans)
    #     temp_x += t[0][0]
    #     temp_y += t[0][1]
    #     temp_z += t[0][1]

    # vrpt = matrix_multiplication([[temp_x/4, temp_y/4, temp_z/4, 1]], trans)


