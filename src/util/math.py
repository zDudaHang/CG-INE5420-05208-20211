from typing import List
import numpy as np

def angle_between_vectors(u: np.array, v: np.array) -> float:
    unit_u = u /  np.linalg.norm(u)
    unit_v = v / np.linalg.norm(v)

    dot_product = np.dot(unit_u, unit_v)

    angle = np.degrees(np.arccos(dot_product))

    cross = np.cross(u, v)
    
    if (cross < 0):
        angle = -angle
    
    return angle

def concat_transformation_matrixes(matrixes: List[np.array]) -> np.array:
    final = matrixes[0]

    for m in matrixes[1:]:
        final = np.dot(final, m)

    return final

def matrix_multiplication(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    result = []
    # Populate the result matrix with zeros
    for i in range(0, len(a)):
        result.append([])
        for j in range(0, len(b[0])):
            result[i].append(0)

    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]

    return result