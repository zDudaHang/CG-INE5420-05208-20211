from src.model.graphic_object import WireFrame, apply_matrix_in_object, apply_matrix_in_point
from src.util.math import concat_transformation_matrixes
from typing import List
from math import sin, cos, radians, degrees, atan

from src.model.point import Point3D

from numpy import array, dot, linalg, cross

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

def translate_matrix_for_rotated_window(d: Point3D, angle: float, center: Point3D) -> array:
    # First, align the window with the world (-angle)
    r_align_with_world = generate_rotate_operation_matrix(center, -angle)

    # Move the window
    t = generate_translation_matrix(d.x(), d.y(), d.z())

    # Then rotate the window back (angle)
    r_rotate_back = generate_rotate_operation_matrix(center, angle)

    return concat_transformation_matrixes([r_align_with_world, t, r_rotate_back])

def translate_window(object_coordinates: List[Point3D], d: Point3D, angle: float, center: Point3D) -> List[Point3D]:
    final = translate_matrix_for_rotated_window(d, angle, center)
    
    for coord in object_coordinates:
        coord.coordinates = dot(coord.coordinates, final)
    return object_coordinates

def rotate_window(object_coordinates: List[Point3D], angle: float, center: Point3D) -> List[Point3D]:
    final = generate_rotate_operation_matrix(center, angle)
    
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
    return concat_transformation_matrixes([t1, scale, t2])

def generate_rotate_operation_matrix(d: Point3D, angle: float) -> array:
    t1 = generate_translation_matrix(-d.x(), -d.y(), -d.z())
    rot = generate_rz_rotation_matrix(angle)
    t2 = generate_translation_matrix(d.x(), d.y(), d.z())

    return concat_transformation_matrixes([t1, rot, t2])

def generate_scn_matrix(center: Point3D, height_w: float, width_w: float, angle: float) -> array:
    t = generate_translation_matrix(-center.x(), -center.y(), -center.z())
    r = generate_rz_rotation_matrix(-angle)
    s = generate_scaling_matrix(1/(width_w/2), 1/(height_w/2))

    return concat_transformation_matrixes([t, r, s])


def get_w_homogen(window_coordinates : Point3D) -> List[List[float]]:
    return [[window_coordinates.x(), window_coordinates.y(), window_coordinates.z(), 1]]

def get_vpn(window_coordinates : List[Point3D], vpr : List[List[float]]) -> List[float]:
    
    wc_list_0 = [window_coordinates[0].x(), window_coordinates[0].y(), window_coordinates[0].z()]
    wc_list_1 = [window_coordinates[1].x(), window_coordinates[1].y(), window_coordinates[1].z()]

    v = dot(wc_list_0, vpr)
    
    u = dot(vpr, wc_list_1)
 
    c_x = v[1]*u[2] - v[2]*u[1]
    c_y = v[2]*u[0] - v[0]*u[2]
    c_z = v[0]*u[1] - v[1]*u[0]

    return [c_x, c_y, c_z]

def angle_with_vpn(vpn : array):
    # rotação em x
    teta_x = degrees(atan(vpn[1]/vpn[2]))
    
    # rotação em y
    teta_y = degrees(atan(vpn[0]/vpn[2]))
    
    return teta_x, teta_y

def parallel_projection(window: WireFrame):

    print('parallel_projection:')

    vpr = window.center
    
    print(f'vpr: {vpr.__str__()}')

    t = generate_translation_matrix(-vpr.x(), -vpr.y(), -vpr.z())

    t_inv = linalg.inv(t)

    # window = apply_matrix_in_object(window, t)

    vpn2 = find_VPN(window.center)

    vpn2 = apply_matrix_in_point(vpn2, t)

    print(f'new VPN {vpn2}')

    # rotação em x
    teta_x2 = degrees(atan(vpn2.y()/vpn2.z()))
    
    # rotação em y
    teta_y2 = degrees(atan(vpn2.x()/vpn2.z()))

    print(f'theta_x2={teta_x2}')
    print(f'teta_y2={teta_y2}')

    #      x, y, z
    vpn = [2, 1, 2]

    teta_x, teta_y = angle_with_vpn(vpn)

    print(f'theta_x={teta_x}')
    print(f'teta_y={teta_y}')

    rot_x = generate_rx_rotation_matrix(teta_x)
    rot_y = generate_ry_rotation_matrix(teta_y)

    # window = apply_matrix_in_object(window, concat_transformation_matrixes([rot_x, rot_y, t_inv]))

    return concat_transformation_matrixes([t, rot_x, rot_y, t_inv])

def find_VPN(window_center: Point3D) -> Point3D:
    # Pegar dois vetores que estao no plano da window e realizar o produto vetorial para obter um vetor ortogonal ao plano
    # u sera um vetor unitario com 

    u = array([window_center.x() + 1, window_center.y(), window_center.z()])
    v = array([window_center.x(), window_center.y() + 1, window_center.z()])

    print('Vectors:')
    print(u)
    print(v)

    unit_u = u / linalg.norm(u)
    unit_v = v / linalg.norm(v)

    print('Unit vectors:')
    print(unit_u)
    print(unit_v)

    n = cross(unit_u, unit_v)

    print('Normal:')
    print(n)    

    # rotação em x => y / z
    teta_x = degrees(atan(n[1]/n[2]))
    
    # rotação em y => x / z
    teta_y = degrees(atan(n[0]/n[2]))

    print(f'theta_x={teta_x},theta_y={teta_y}')

    return Point3D(n[0],n[1],n[2])

def perspective_projection(window_coordinates : List[Point3D], focal_distance: float) ->  array:
    t = generate_translation_matrix(0, 0, -focal_distance)

    per = array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/focal_distance, 0]])

    # Determine VPR, translate it to origin, rotate on x and y axes to align on z axis
    p = parallel_projection(window_coordinates)

    return concat_transformation_matrixes([p, t, per])

def generate_perspective_matrix(focal_distance: float) -> array:
    return array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/focal_distance, 0]])
