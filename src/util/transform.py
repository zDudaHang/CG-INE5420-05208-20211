from src.model.enum.RotateAxisOptionsEnum import RotateAxisOptionsEnum
from typing import List
from math import sin, cos, radians, degrees, atan

from numpy import void

from src.model.point import Point3D

from numpy import array, dot

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

def generate_translation_matrix(dx: float, dy: float, dz: float = 0) -> array:
    return array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]])

def generate_scaling_matrix(sx: float, sy: float, sz: float = 1) -> array:
    return array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]])

def generate_rz_rotation_matrix(angleGraus: float) -> array:
    angle = radians(angleGraus)
    return array([
            [cos(angle), sin(angle), 0, 0],
            [-sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

def generate_ry_rotation_matrix(angleGraus: float) -> array:
    angle = radians(angleGraus)
    return[
            [cos(angle), 0, -sin(angle), 0],
            [0, 1, 0, 0],
            [sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]]

def generate_rx_rotation_matrix(angleGraus: float) -> array:
    angle = radians(angleGraus)
    return array([
            [1, 0, 0, 0],
            [0, cos(angle), sin(angle), 0],
            [0, -sin(angle), cos(angle), 0],
            [0, 0, 0, 1]])

def translate_object(object_coordinates: List[Point3D], d: Point3D) -> List[Point3D]:
    t = generate_translation_matrix(d.x(), d.y(), d.z())

    for coord in object_coordinates:
        coord.coordinates = dot(coord.coordinates, t)
    return object_coordinates

def translate_matrix_for_rotated_window(d: Point3D, angle: float, center: Point3D, axis_option: RotateAxisOptionsEnum) -> array:
    # First, align the window with the world (-angle)
    r_align_with_world = generate_rotate_operation_matrix(center, -angle, axis_option)

    # Move the window
    t = generate_translation_matrix(d.x(), d.y(), d.z())

    # Then rotate the window back (angle)
    r_rotate_back = generate_rotate_operation_matrix(center, angle, axis_option)

    r = dot(r_align_with_world, t)
    return dot(r, r_rotate_back)

def translate_window(object_coordinates: List[Point3D], d: Point3D, angle: float, center: Point3D, axis_option: RotateAxisOptionsEnum) -> List[Point3D]:
    final = translate_matrix_for_rotated_window(d, angle, center, axis_option)
    
    for coord in object_coordinates:
        coord.coordinates = dot(coord.coordinates, final)
    return object_coordinates

def rotate_window(object_coordinates: List[Point3D], angle: float, center: Point3D, axis_option : RotateAxisOptionsEnum) -> List[Point3D]:
    final = generate_rotate_operation_matrix(center, angle, axis_option)
    
    for coord in object_coordinates:
        coord.coordinates = dot(coord.coordinates, final)
    return object_coordinates

def scale_window(object_coordinates: List[Point3D], center: Point3D, sx: float, sy: float) -> List[Point3D]:
    final = generate_scale_operation_matrix(center, sx, sy, 1)

    for coord in object_coordinates:
        coord.coordinates = dot(coord.coordinates, final)
    return object_coordinates

def generate_scale_operation_matrix(center: Point3D, sx: float, sy: float, sz: float) -> array:
    t1 = generate_translation_matrix(-center.x(), -center.y(), -center.z())
    scale = generate_scaling_matrix(sx, sy, sz)
    t2 = generate_translation_matrix(center.x(), center.y(), center.z())

    r = dot(t1, scale)
    return dot(r, t2)

def generate_rotate_operation_matrix(d: Point3D, angle: float, axis_option : RotateAxisOptionsEnum) -> array:
    t1 = generate_translation_matrix(-d.x(), -d.y(), -d.z())
    rot = array([])
    if axis_option == RotateAxisOptionsEnum.X:
        rot = generate_rx_rotation_matrix(angle)
    elif axis_option == RotateAxisOptionsEnum.Y:
        rot = generate_ry_rotation_matrix(angle)
    else:
        rot = generate_rz_rotation_matrix(angle)
    t2 = generate_translation_matrix(d.x(), d.y(), d.z())

    r = dot(t1, rot)
    return dot(r, t2)

def generate_scn_matrix(center: Point3D, height_w: float, width_w: float, angle: float) -> array:
    t = generate_translation_matrix(-center.x(), -center.y(), -center.z())
    r = generate_rz_rotation_matrix(-angle)
    s = generate_scaling_matrix(1/(width_w/2), 1/(height_w/2))

    temp = dot(t, r)
    return dot(temp, s)


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

    v = dot(wc_list_0, vpr)
    
    u = dot(vpr, wc_list_1)
 
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

    #vpn = get_vpn(window_coordinates, vpr)
    vpn = [2, 1, 2]
    
    teta_x, teta_y = angle_with_vpn(vpn)

    rot_x = generate_rx_rotation_matrix(teta_x)
    rot_y = generate_ry_rotation_matrix(teta_y)


    transform = dot(trans, rot_x)
    transform = dot(transform, rot_y)
    
    return transform
