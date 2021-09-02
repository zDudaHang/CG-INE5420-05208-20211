from PyQt5.QtGui import QPainter
from typing import Callable, List
from src.model.point import Point3D
from numpy import array, dot

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

BSPLINE_MATRIX = [
    [-1/6, 1/2, -1/2, 1/6],
    [1/2, -1, 1/2, 0],
    [-1/2, 0, 1/2, 0],
    [1/6, 2/3, 1/6, 0]
]

class BezierGeometryMatrix():
    def __init__(self, x: List[List[float]], y: List[List[float]]):
        self.x = x
        self.y = y

def get_GB_bezier(p0: Point3D, p1: Point3D, p2: Point3D, p3: Point3D) -> BezierGeometryMatrix:
    gb_x = [
        [p0.x()], 
        [p1.x()], 
        [p2.x()], 
        [p3.x()]
    ]

    gb_y = [
        [p0.y()], 
        [p1.y()], 
        [p2.y()], 
        [p3.y()]
    ]

    return BezierGeometryMatrix(gb_x, gb_y)

def blending_function(t: float, gb: List[List[float]]) -> float:
    matrix_t = [[pow(t, 3), pow(t, 2), t, 1]]
    blending = dot(matrix_t, BEZIER_MATRIX)
    return dot(blending, gb)[0][0]


class BSplineGeometryMatrix:
    def __init__(self, x: List[List[float]], y: List[List[float]], z: List[List[float]]):
        self.x = x
        self.y = y
        self.z = z

def get_GB_spline(p0: Point3D, p1: Point3D, p2: Point3D, p3: Point3D):
    g_x = [
        [p0.x()], 
        [p1.x()], 
        [p2.x()], 
        [p3.x()]
    ]

    g_y = [
        [p0.y()], 
        [p1.y()], 
        [p2.y()], 
        [p3.y()]
    ]

    g_z = [
        [p0.z()], 
        [p1.z()], 
        [p2.z()], 
        [p3.z()]
    ]

    return BSplineGeometryMatrix(g_x, g_y, g_z)

def generate_delta_matrix(delta: float) -> array:
    delta2 = pow(delta, 2)
    delta3 = pow(delta, 3)
                        
    return array([
        [0, 0, 0, 1],
        [delta3, delta2, delta, 0],
        [6*delta3, 2*delta2, 0, 0],
        [6*delta3, 0, 0, 0]
    ])

class ForwardDifferenceValues:
    def __init__(self, x: float, derivx: List[float], y: float, derivy: List[float], z: float, derivz: List[float]):
        self.x = x
        self.derivx = derivx

        self.y = y
        self.derivy = derivy

        self.z = z
        self.derivz = derivz

    def __str__(self) -> str:
        return f'x={self.x}, dx={self.derivx[0]}, d2x={self.derivx[1]}, d3x={self.derivx[2]}'
    
    def update(self):
        self.x += self.derivx[0]; self.derivx[0] += self.derivx[1]; self.derivx[1] += self.derivx[2]
        self.y += self.derivy[0]; self.derivy[0] += self.derivy[1]; self.derivy[1] += self.derivy[2]
        self.z += self.derivz[0]; self.derivz[0] += self.derivz[1]; self.derivz[1] += self.derivz[2]

def generate_curve_initial_values(delta_matrix: array, gb: BSplineGeometryMatrix):
    c_x = dot(BSPLINE_MATRIX, gb.x)
    c_y = dot(BSPLINE_MATRIX, gb.y)
    c_z = dot(BSPLINE_MATRIX, gb.z)

    Dx = dot(delta_matrix, c_x)
    Dy = dot(delta_matrix, c_y)
    Dz = dot(delta_matrix, c_z)

    # return ForwardDifferenceValues(initial_x[0][0], initial_x[1:], initial_y[0][0], initial_y[1:], initial_z[0][0], initial_z[1:])
    return Dx, Dy, Dz

def fwd_diff(n: int, x: float, Dx: float, D2x: float, D3x: float, y: float, Dy: float, D2y: float, D3y: float, z: float, Dz: float, D2z: float, D3z: float, drawLine: Callable[[QPainter, float, float, float, float, Point3D, Point3D, Point3D], None], painter: QPainter, viewport_min: Point3D, viewport_max: Point3D, viewport_origin: Point3D):
    i = 1
    x_old = x
    y_old = y
    z_old = z
    while i < n:
        i += 1
        # values.update()
        x = x + Dx;  Dx = Dx + D2x;  D2x = D2x + D3x
        y = y + Dy;  Dy = Dy + D2y;  D2y = D2y + D3y
        z = z + Dz;  Dz = Dz + D2z;  D2z = D2z + D3z

        drawLine(painter, x_old, x, y_old, y, viewport_min, viewport_max, viewport_origin, z_old, z)

        x_old = x
        y_old = y
        z_old = z

