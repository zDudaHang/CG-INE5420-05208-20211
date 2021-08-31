from src.util.math import concat_transformation_matrixes
from typing import List
from src.model.point import Point3D
from src.util.curves import ForwardDifferenceValues
from numpy import array, dot, transpose

BEZIER_MATRIX = [
    [-1,  3, -3, 1],
    [ 3, -6,  3, 0],
    [-3,  3,  0, 0],
    [ 1,  0,  0, 0]
]

BSPLINE_MATRIX = [
    [-1/6, 1/2, -1/2, 1/6],
    [ 1/2,  -1,  1/2,   0],
    [-1/2,   0,  1/2,   0],
    [ 1/6, 2/3,  1/6,   0]
]

TRANSPOSED_BSPLINE_MATRIX = [
    [-1/6, 1/2, -1/2, 1/6],
    [ 1/2,  -1,    0, 2/3],
    [-1/2, 1/2,  1/2, 1/6],
    [ 1/6,   0,    0,   0]
]

class BicubicSurfaceGeometryMatrix():
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


    return BicubicSurfaceGeometryMatrix(gb_x, gb_y, gb_z)

def get_bicubic_geometry_matrix(points: List[Point3D]) -> BicubicSurfaceGeometryMatrix:
    
    gb_x = [[0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0]]
    gb_y = [[0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0]]
    gb_z = [[0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0]]

    for i in range(0, 4):
        for j in range(0, 4):
            index = i + j * 4
            point = points[index]
            gb_x[i][j] = point.x()
            gb_y[i][j] = point.y()
            gb_z[i][j] = point.z()

    return BicubicSurfaceGeometryMatrix(gb_x, gb_y, gb_z)

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

class SurfaceForwardDifferenceValues:
    def __init__(self, x: List[List[float]], y: List[List[float]], z: List[List[float]]):
        self.x = x
        self.y = y
        self.z = z

    def transpose(self):
        self.x = transpose(self.x)
        self.y = transpose(self.y)
        self.z = transpose(self.z)

    def to_fwd_diff(self) -> ForwardDifferenceValues:
        return ForwardDifferenceValues(x=self.x[0][0], derivx=self.x[0][1:], y=self.y[0][0], derivy=self.y[0][1:], z=self.z[0][0], derivz=self.z[0][1:])
    
    def update(self):

        # Linha1 <- Linha1 + Linha2
        # DDx[0][0] = DDx[0][0]+ DDx[1][0]; 
        # DDx[0][1] = DDx[0][1]+ DDx[1][1]; 
        # DDx[0][2] = DDx[0][2]+ DDx[1][2]; 
        # DDx[0][3] = DDx[0][3]+ DDx[1][3];

        for i in range(0, 4):
            self.x[0][i] += self.x[1][i]
            self.y[0][i] += self.y[1][i]
            self.z[0][i] += self.z[1][i]
        
        # Linha2 <- Linha2 + Linha3
        # DDx[1][0] = DDx[1][0] + DDx[2][0]; 
        # DDx[1][1] = DDx[1][1] + DDx[2][1]; 
        # DDx[1][2] = DDx[1][2] + DDx[2][2]; 
        # DDx[1][3] = DDx[1][3] + DDx[2][3];

        for i in range(0, 4):
            self.x[1][i] += self.x[2][i]
            self.y[1][i] += self.y[2][i]
            self.z[1][i] += self.z[2][i]
        
        # Linha3 <- Linha3 + Linha4
        # DDx[2][0] = DDx[2][0] + DDx[3][0]; 
        # DDx[2][1] = DDx[2][1] + DDx[3][1]; 
        # DDx[2][2] = DDx[2][2] + DDx[3][2]; 
        # DDx[2][3] = DDx[2][3] + DDx[3][3];

        for i in range(0, 4):
            self.x[2][i] += self.x[3][i]
            self.y[2][i] += self.y[3][i]
            self.z[2][i] += self.z[3][i]


def generate_surface_initial_values(delta_matrix_s: array, delta_matrix_t, gb: BicubicSurfaceGeometryMatrix) -> SurfaceForwardDifferenceValues:
    # Cx = M * Gx * M^T
    c_x = concat_transformation_matrixes([BSPLINE_MATRIX, gb.x, TRANSPOSED_BSPLINE_MATRIX])
    c_y = concat_transformation_matrixes([BSPLINE_MATRIX, gb.y, TRANSPOSED_BSPLINE_MATRIX])
    c_z = concat_transformation_matrixes([BSPLINE_MATRIX, gb.z, TRANSPOSED_BSPLINE_MATRIX])

    # DDx = delta_s * Cx * delta_t^T
    DD_x = concat_transformation_matrixes([delta_matrix_s, c_x, delta_matrix_t])
    DD_y = concat_transformation_matrixes([delta_matrix_s, c_y, delta_matrix_t])
    DD_z = concat_transformation_matrixes([delta_matrix_s, c_z, delta_matrix_t])

    return SurfaceForwardDifferenceValues(DD_x, DD_y, DD_z)