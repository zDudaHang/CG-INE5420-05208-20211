from src.model.point import Point2D

class PointClipper():
    def clip(point: Point2D, window_min : Point2D = Point2D(-1, -1), window_max : Point2D = Point2D(1, 1)) -> bool:
        return point.between(window_min, window_max)