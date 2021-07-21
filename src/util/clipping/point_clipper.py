from src.model.point import Point2D

class PointClipper():
    def clip(point: Point2D) -> bool:
        return point.between(Point2D(-1, -1), Point2D(1, 1))
