from typing import List
from src.model.point import Point2D
from src.util.math import matrix_multiplication

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]

class BezierGeometryMatrix():
    def __init__(self, x: List[List[float]], y: List[List[float]]):
        self.x = x
        self.y = y

def get_GB(p0: Point2D, p1: Point2D, p2: Point2D, p3: Point2D) -> BezierGeometryMatrix:
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