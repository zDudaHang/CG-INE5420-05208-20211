from typing import Tuple
from PyQt5.QtCore import QPointF

class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.coordinates = [[x, y, 1]]

    def x(self) -> float:
        return self.coordinates[0][0]

    def y(self) -> float:
        return self.coordinates[0][1]

    def __str__(self) -> str:
        return f'({round(self.x(), 2)},{round(self.y(),2)})'

    def to_QPointF(self) -> QPointF:
        return QPointF(self.x(), self.y())

    def __add__(self, other: Tuple):
        return Point2D(self.x() + other[0], self.y() + other[1])
    
    def __eq__(self, o: object) -> bool:
        if (isinstance(o, Point2D)):
            return self.coordinates == o.coordinates
        return False
    
    def __ne__(self, o: object) -> bool:
        if (isinstance(o, Point2D)):
            return self.coordinates != o.coordinates
        return False

    def between(self, min: object, max: object) -> bool:
        if (isinstance(min, Point2D) and isinstance(max, Point2D)):
            return min.x() <= self.x() <= max.x() and min.y() <= self.y() <= max.y()
        return False