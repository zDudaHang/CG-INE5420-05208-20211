from typing import Tuple
from PyQt5.QtCore import QPointF

class Point3D:
    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.coordinates = [[x, y, z, 1]]

    def x(self) -> float:
        return self.coordinates[0][0]

    def y(self) -> float:
        return self.coordinates[0][1]
    
    def z(self) -> float:
        return self.coordinates[0][2]

    def __str__(self) -> str:
        return f'({self.x()},{self.y()},{self.z()})'

    def to_QPointF(self) -> QPointF:
        return QPointF(self.x(), self.y())

    def __add__(self, other: Tuple):
        if len(other) == 2:
            return Point3D(self.x() + other[0], self.y() + other[1])
        elif len(other) == 3:
            return Point3D(self.x() + other[0], self.y() + other[1], self.z() + other[2])
    
    def __eq__(self, o: object) -> bool:
        if (isinstance(o, Point3D)):
            return self.coordinates == o.coordinates
        return False
    
    def __ne__(self, o: object) -> bool:
        if (isinstance(o, Point3D)):
            return self.coordinates != o.coordinates
        return False

    def between(self, min: object, max: object) -> bool:
        if (isinstance(min, Point3D) and isinstance(max, Point3D)):
            return min.x() <= self.x() <= max.x() and min.y() <= self.y() <= max.y()
        return False