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

def vector_subtraction(u, v):
    result = []
    for i in range(len(u)):
        result.append(u[i] - v[i])
    return result