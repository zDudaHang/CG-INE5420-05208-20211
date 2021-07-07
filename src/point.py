
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
