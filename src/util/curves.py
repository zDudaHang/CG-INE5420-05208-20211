from typing import List
from src.model.point import Point3D
from src.util.math import matrix_multiplication

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

def get_GB(p0: Point3D, p1: Point3D, p2: Point3D, p3: Point3D) -> BezierGeometryMatrix:
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
    blending = matrix_multiplication(matrix_t, BEZIER_MATRIX)
    return matrix_multiplication(blending, gb)[0][0]


class BSpline:
    def __init__(self, x: List[List[float]], y: List[List[float]]):
        self.x = x
        self.y = y

def get_GB_Spline(p0: Point3D, p1: Point3D, p2: Point3D, p3: Point3D):
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

    return BSpline(g_x, g_y)

def forward_differences(d: float, gb: List[List[float]]):
    
    matrix_e = [
        [0, 0, 0, 1],
        [pow(d, 3), pow(d, 2), d, 0],
        [6*pow(d, 3), 2*pow(d, 2), 0, 0],
        [6*pow(d, 3), 0, 0, 0]
    ]

    c_x = matrix_multiplication(BSPLINE_MATRIX, gb.x)
    c_y = matrix_multiplication(BSPLINE_MATRIX, gb.y)


    fwdd_x = matrix_multiplication(matrix_e, c_x)
    fwdd_y = matrix_multiplication(matrix_e, c_y)


    return fwdd_x, fwdd_y