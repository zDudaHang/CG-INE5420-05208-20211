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
        return f'({self.x()},{self.y()})'

    def to_QPointF(self) -> QPointF:
        return QPointF(self.x(), self.y())

    def __add__(self, other: Tuple):
        return Point2D(self.x() + other[0], self.y() + other[1])
    
    def __eq__(self, o: object) -> bool:
        return self.coordinates == o.coordinates