from src.model.point import Point3D

class PointClipper():
    def clip(point: Point3D, window_min : Point3D = Point3D(-1, -1), window_max : Point3D = Point3D(1, 1)) -> bool:
        return point.between(window_min, window_max)
