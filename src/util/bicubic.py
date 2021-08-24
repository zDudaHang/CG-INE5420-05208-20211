from typing import List
from src.model.point import Point3D
# from src.util.math import matrix_multiplication
from numpy import dot

BEZIER_MATRIX = [
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
]


class BicubicSurfaceCurve():
    def __init__(self, x: List[List[float]], y: List[List[float]], z: List[List[float]]):
        self.x = x
        self.y = y
        self.z = z

def get_bicubic_GB(p_list: List[Point3D]):

    gb_x = [
        [p.x() for idx, p in enumerate(p_list) if idx < 4],
        [p.x() for idx, p in enumerate(p_list) if 3 < idx < 8],
        [p.x() for idx, p in enumerate(p_list) if 7 < idx < 12],
        [p.x() for idx, p in enumerate(p_list) if idx > 11]
    ]
    

    gb_y = [
        [p.y() for idx, p in enumerate(p_list) if idx < 4],
        [p.y() for idx, p in enumerate(p_list) if 3 < idx < 8],
        [p.y() for idx, p in enumerate(p_list) if 7 < idx < 12],
        [p.y() for idx, p in enumerate(p_list) if idx > 11]
    ]

    gb_z = [
        [p.z() for idx, p in enumerate(p_list) if idx < 4],
        [p.z() for idx, p in enumerate(p_list) if 3 < idx < 8],
        [p.z() for idx, p in enumerate(p_list) if 7 < idx < 12],
        [p.z() for idx, p in enumerate(p_list) if idx > 11]
    ]


    return BicubicSurfaceCurve(gb_x, gb_y, gb_z)


def blending_function_bicubic(s:float, t: float, gb: List[List[float]]) -> float:

    param_s = [[pow(s, 3), pow(s, 2), s, 1]]

    param_t = [
        [pow(t, 3)],
        [pow(t, 2)], 
        [t],
        [1]
    ]

    blending = dot(param_s, BEZIER_MATRIX)
    blending = dot(blending, gb)
    blending = dot(blending, BEZIER_MATRIX)
    blending = dot(blending, param_t)

    return blending

