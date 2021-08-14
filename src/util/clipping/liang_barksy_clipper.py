from typing import Optional
from src.model.point import Point3D
from src.model.graphic_object import Line
from copy import deepcopy

class LiagnBarksyClipper():
    def __init__(self, line: Line, window_min: Point3D = Point3D(-1, -1), window_max: Point3D = Point3D(1, 1)):

        coordinates = line.coordinates

        self.delta_x = coordinates[1].x() - coordinates[0].x()
        self.delta_y = coordinates[1].y() - coordinates[0].y()

        self.x1 = coordinates[0].x()
        self.y1 = coordinates[0].y()

        self.p = [
            -self.delta_x,
            self.delta_x,
            -self.delta_y,
            self.delta_y
        ]

        self.q = [
            self.x1 - window_min.x(),
            window_max.x() - self.x1,
            self.y1 - window_min.y(),
            window_max.y() - self.y1
        ]

        self.is_not_inside = False

        for i in range(len(self.p)):
            if self.p[i] == 0 and self.q[i] < 0:
                self.is_inside = True
                # Encontramos uma reta fora dos limites

        self.old_line = line

    def clip(self) -> Optional[Line]:

        if self.is_not_inside:
            return None
        
        negativos = [i for i in range(len(self.p)) if self.p[i] < 0]
        positivos = [i for i in range(len(self.p)) if self.p[i] > 0]

        r = [0] * len(negativos)

        i = 0

        for index in negativos:
            r[i] = self.q[index] / self.p[index]
            i += 1

        c1 = max([0] + r)
        
        i = 0
        for index in positivos:
            r[i] = self.q[index] / self.p[index]
            i += 1

        c2 = min([1] + r)

        if c1 > c2:
            return None

        line = deepcopy(self.old_line)

        x1 = self.x1 + c1 * self.delta_x
        y1 = self.y1 + c1 * self.delta_y

        x2 = self.x1 + c2 * self.delta_x
        y2 = self.y1 + c2 * self.delta_y

        line.coordinates = [Point3D(x1, y1), Point3D(x2, y2)]

        return line