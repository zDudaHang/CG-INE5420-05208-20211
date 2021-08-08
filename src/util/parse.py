from typing import Union, List
from src.model.point import Point3D

def parse(text: str) -> Union[None, List[Point3D]]:   
    text += ','
    l : List[tuple] = list(eval(text))
    l_points : List[Point3D] = []

    for t in l:
        if len(t) < 3:
            return None
        l_points.append(Point3D(t[0], t[1], t[2]))

    return l_points