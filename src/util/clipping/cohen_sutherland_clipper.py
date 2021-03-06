from src.model.point import Point3D
from src.model.graphic_object import Line
from copy import deepcopy

class CohenSutherlandLineClipper():

    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    def __init__(self, line: Line, window_min: Point3D = Point3D(-1, -1), window_max: Point3D = Point3D(1, 1)):

        self.coordinates = line.coordinates

        self.x_min = window_min.x() 
        self.y_min = window_min.y()
        self.x_max = window_max.x()
        self.y_max = window_max.y()

        self.old_line = line


    def region_code(self, ponto: Point3D):
        # Coordenadas do ponto
        x = ponto.x()
        y = ponto.y()
        
        rc = self.INSIDE
        
        if x < self.x_min:
            rc |= self.LEFT
        elif x > self.x_max:
            rc |= self.RIGHT
        if y < self.y_min:
            rc |= self.BOTTOM
        elif y > self.y_max:
            rc |= self.TOP

        return rc
    
    def cohenSutherlandClip(self):

        ponto_1 = self.coordinates[0]
        ponto_2 = self.coordinates[1]
        
        rc_point_1 = self.region_code(ponto_1)
        rc_point_2 = self.region_code(ponto_2)

        point_1 = ponto_1
        point_2 = ponto_2

        line = deepcopy(self.old_line)

        while True:

            if rc_point_1 == 0 and rc_point_2 == 0:
                line.coordinates = [Point3D(point_1.x(),point_1.y()), Point3D(point_2.x(), point_2.y())]
                return line
            elif (rc_point_1 & rc_point_2) != 0:
                #COMPLETAMENTE FORA da window
                return None
            else:
                new_x = 1
                new_y = 1

                if rc_point_1 != 0:
                    rc_out = rc_point_1
                else:
                    rc_out = rc_point_2

                if rc_out & self.TOP:

                    new_x = point_1.x() + (point_2.x() - point_1.x()) * \
                                    (self.y_max - point_1.y()) / (point_2.y() - point_1.y())
                    new_y = self.y_max
    
                elif rc_out & self.BOTTOM:
                    
                    new_x = point_1.x() + (point_2.x() - point_1.x()) * \
                                    (self.y_min - point_1.y()) / (point_2.y() - point_1.y())
                    new_y = self.y_min
    
                elif rc_out & self.RIGHT:
                    
                    new_y = point_1.y() + (point_2.y() - point_1.y()) * \
                                    (self.x_max - point_1.x()) / (point_2.x() - point_1.x())
                    new_x = self.x_max
    
                elif rc_out & self.LEFT:

                    new_y = point_1.y() + (point_2.y() - point_1.y()) * \
                                    (self.x_min - point_1.x()) / (point_2.x() - point_1.x())
                    new_x = self.x_min
    
    
                if rc_out == rc_point_1:
                    point_1 = Point3D(new_x, new_y)
                    rc_point_1 = self.region_code(point_1)
    
                else:
                    point_2 = Point3D(new_x, new_y)
                    rc_point_2 = self.region_code(point_2)