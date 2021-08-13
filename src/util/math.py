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