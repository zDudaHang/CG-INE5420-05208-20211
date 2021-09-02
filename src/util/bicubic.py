from src.util.math import concat_transformation_matrixes
from typing import List
from src.model.point import Point3D
from numpy import array, dot

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

def generate_surface_initial_values(delta_matrix_s: array, delta_matrix_t: array, gb: BicubicSurfaceGeometryMatrix):
    # Cx = M * Gx * M^T
    c_x = concat_transformation_matrixes([BSPLINE_MATRIX, gb.x, TRANSPOSED_BSPLINE_MATRIX])
    c_y = concat_transformation_matrixes([BSPLINE_MATRIX, gb.y, TRANSPOSED_BSPLINE_MATRIX])
    c_z = concat_transformation_matrixes([BSPLINE_MATRIX, gb.z, TRANSPOSED_BSPLINE_MATRIX])

    # DDx = delta_s * Cx * delta_t^T
    DD_x = concat_transformation_matrixes([delta_matrix_s, c_x, delta_matrix_t])
    DD_y = concat_transformation_matrixes([delta_matrix_s, c_y, delta_matrix_t])
    DD_z = concat_transformation_matrixes([delta_matrix_s, c_z, delta_matrix_t])

    return DD_x, DD_y, DD_z

def update_DD_values(DDx: array, DDy: array, DDz: array):
    #   row1 <- row1 + row2
    DDx[0][0] =  DDx[0][0]+DDx[1][0]; DDx[0][1] = DDx[0][1]+DDx[1][1]; DDx[0][2] = DDx[0][2]+DDx[1][2]; DDx[0][3] = DDx[0][3]+DDx[1][3]
    DDy[0][0] =  DDy[0][0]+DDy[1][0]; DDy[0][1] = DDy[0][1]+DDy[1][1]; DDy[0][2] = DDy[0][2]+DDy[1][2]; DDy[0][3] = DDy[0][3]+DDy[1][3]
    DDz[0][0] =  DDz[0][0]+DDz[1][0]; DDz[0][1] = DDz[0][1]+DDz[1][1]; DDz[0][2] = DDz[0][2]+DDz[1][2]; DDz[0][3] = DDz[0][3]+DDz[1][3]
    
    # row2 <- row2 + row3
    DDx[1][0] =  DDx[1][0]+DDx[2][0]; DDx[1][1] = DDx[1][1]+DDx[2][1]; DDx[1][2] = DDx[1][2]+DDx[2][2]; DDx[1][3] = DDx[1][3]+DDx[2][3]
    DDy[1][0] =  DDy[1][0]+DDy[2][0]; DDy[1][1] = DDy[1][1]+DDy[2][1]; DDy[1][2] = DDy[1][2]+DDy[2][2]; DDy[1][3] = DDy[1][3]+DDy[2][3]
    DDz[1][0] =  DDz[1][0]+DDz[2][0]; DDz[1][1] = DDz[1][1]+DDz[2][1]; DDz[1][2] = DDz[1][2]+DDz[2][2]; DDz[1][3] = DDz[1][3]+DDz[2][3]
    
    # row3 <- row3 + row4 
    DDx[2][0] =  DDx[2][0]+DDx[3][0]; DDx[2][1] = DDx[2][1]+DDx[3][1]; DDx[2][2] = DDx[2][2]+DDx[3][2]; DDx[2][3] = DDx[2][3]+DDx[3][3]
    DDy[2][0] =  DDy[2][0]+DDy[3][0]; DDy[2][1] = DDy[2][1]+DDy[3][1]; DDy[2][2] = DDy[2][2]+DDy[3][2]; DDy[2][3] = DDy[2][3]+DDy[3][3]
    DDz[2][0] =  DDz[2][0]+DDz[3][0]; DDz[2][1] = DDz[2][1]+DDz[3][1]; DDz[2][2] = DDz[2][2]+DDz[3][2]; DDz[2][3] = DDz[2][3]+DDz[3][3]

    return DDx, DDy, DDz