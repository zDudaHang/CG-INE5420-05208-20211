from typing import Tuple
from PyQt5.QtCore import QPointF

class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.coordinates = [[x, y, 1]]

    def get_x(self) -> float:
        return self.coordinates[0][0]

    def get_y(self) -> float:
        return self.coordinates[0][1]

    def __str__(self) -> str:
        return f'({self.get_x()},{self.get_y()})'

    def to_QPointF(self) -> QPointF:
        return QPointF(self.get_x(), self.get_y())

    def __add__(self, other: Tuple):
        return Point2D(self.get_x() + other[0], self.get_y() + other[1])
    
    def __eq__(self, o: object) -> bool:
        print('__eq__')
        print(self)
        print(o)
        return self.coordinates == o.coordinates